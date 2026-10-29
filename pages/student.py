import streamlit as st
import pandas as pd
import os
from rules import process_data
from db import get_suggestions
from styles import page_header, metric_card

DATA_FILE = "data/teacher_uploaded.csv"

def render(user):
    page_header("学生端", "我的学习诊断与教师建议")
    
    if not os.path.exists(DATA_FILE):
        st.warning("老师尚未上传班级数据，请耐心等待。")
        return
        
    if not user.get("student_id"):
        st.warning("当前账号未关联学生ID，请联系教师。")
        return
        
    df = process_data(pd.read_csv(DATA_FILE))
    stu_df = df[df["student_id"] == user["student_id"]]
    
    if stu_df.empty:
        st.info("未在老师上传的数据中找到你的学号记录。")
        return
        
    c1, c2 = st.columns(2)
    with c1: metric_card("我的正确率", f"{stu_df['correct_rate'].mean():.1%}")
    with c2: metric_card("我的完成率", f"{stu_df['completed'].mean():.1%}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📚 知识点掌握情况")
    kp_stats = stu_df.groupby("knowledge_point")["correct_rate"].mean().reset_index()
    for _, row in kp_stats.iterrows():
        st.progress(min(max(row['correct_rate'], 0.0), 1.0), text=f"{row['knowledge_point']} - 正确率 {row['correct_rate']:.1%}")
        
    st.markdown("---")
    st.subheader("💡 教师专属建议")
    suggs = get_suggestions(user["student_id"])
    if not suggs:
        st.info("暂无教师发布的建议。")
    else:
        for s in suggs:
            st.success(f"**内容：** {s['modified_text']}\n\n*发布人：{s['teacher_name']}*")
