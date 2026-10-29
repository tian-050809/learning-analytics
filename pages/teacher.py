import pandas as pd
import streamlit as st
import os
from datetime import datetime

from rules import process_data, diagnose_student, generate_suggestions
from llm_explain import call_real_llm
from db import save_suggestion, get_suggestions
from styles import page_header, metric_card

DATA_FILE = "data/teacher_uploaded.csv"

def render(user):
    page_header("教师工作台", "导入真实数据 · 规则诊断 · 大模型深度分析")
    
    # --- 大模型 API 配置区 ---
    with st.expander("🔧 配置大模型 API（使用真实大模型必填）", expanded=False):
        api_key = st.text_input("API Key", type="password", help="填入 DeepSeek 或 OpenAI 的 Key")
        base_url = st.text_input("Base URL", value="https://api.deepseek.com", help="DeepSeek填 https://api.deepseek.com")
        model_name = st.text_input("模型名称", value="deepseek-chat", help="DeepSeek填 deepseek-chat")
        st.session_state["llm_config"] = {"key": api_key, "url": base_url, "model": model_name}
    
    # --- 数据导入区 ---
    st.subheader("1. 数据导入")
    if not os.path.exists("data"): os.makedirs("data")
        
    if not os.path.exists(DATA_FILE):
        st.info("尚无教学数据，请上传 CSV 文件（字段需包含: student_id, task_id, score, max_score, completed, knowledge_point）")
        uploaded = st.file_uploader("上传成绩/行为记录 CSV", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded)
            df.to_csv(DATA_FILE, index=False)
            st.success("数据导入成功！")
            st.rerun()
        return
    
    # 读取真实数据
    df = pd.read_csv(DATA_FILE)
    clean_df = process_data(df)
    
    # --- 班级分析 ---
    st.subheader("2. 班级概览")
    c1, c2, c3 = st.columns(3)
    with c1: metric_card("班级总记录", len(clean_df))
    with c2: metric_card("平均正确率", f"{clean_df['correct_rate'].mean():.1%}")
    with c3: metric_card("平均完成率", f"{clean_df['completed'].mean():.1%}")
    
    st.markdown("---")
    st.subheader("3. 个体诊断与真实 AI 分析")
    
    students = clean_df[["student_id", "student_name"]].drop_duplicates().values.tolist()
    if not students:
        st.warning("数据为空")
        return
        
    sid = st.selectbox("选择学生", students, format_func=lambda x: f"{x[0]} · {x[1]}")[0]
    stu_df = clean_df[clean_df["student_id"] == sid]
    
    diag = diagnose_student(stu_df)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown("##### 规则诊断结论")
        st.info(f"**{diag['main_diagnosis']}**")
        st.write(f"- 正确率：{diag['overall_c']:.1%}")
        st.write(f"- 完成率：{diag['overall_m']:.1%}")
        if diag['weak_kps']:
            st.write("**薄弱知识点：**")
            for w in diag['weak_kps']: st.write(f"  - {w['kp']} ({w['avg_correct']:.1%})")

    with col2:
        st.markdown("##### AI 学情深度解释")
        if st.button("调用大模型生成解释", type="primary"):
            config = st.session_state.get("llm_config", {})
            if not config.get("key"):
                st.error("请在上方展开“配置大模型 API”并填入 Key！")
            else:
                with st.spinner("AI 正在分析数据，请稍候..."):
                    cls_data = {"avg_correct": round(clean_df['correct_rate'].mean(), 3), "avg_completion": round(clean_df['completed'].mean(), 3)}
                    data, err = call_real_llm(config["key"], config["url"], config["model"], diag, cls_data)
                    
                    if err:
                        st.error(f"大模型调用失败：{err}")
                    else:
                        st.success("分析完成")
                        st.write("**观察到的事实：**")
                        for f in data.get("facts", []): st.write(f"- {f}")
                        st.write("**可能的原因：**")
                        for c in data.get("causes", []): st.write(f"- {c}")
    
    st.markdown("---")
    st.subheader("4. 生成并审核教学建议")
    suggestions = generate_suggestions(diag)
    
    for i, s in enumerate(suggestions):
        with st.expander(f"建议 {i+1}: {s['target']} ({s['kp']})", expanded=True):
            st.write(f"**目标：** {s['goal']}")
            st.write(f"**活动：** {s['activity']}")
            mod = st.text_area("教师审核修改：", value=s['activity'], key=f"mod_{sid}_{i}")
            if st.button("保存并发布", key=f"save_{sid}_{i}"):
                save_suggestion(sid, s['rule'], s['activity'], mod, user['username'], datetime.now().strftime("%Y-%m-%d"))
                st.success("已发布至学生端！")
