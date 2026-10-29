import streamlit as st
from db import register_user, verify_user

def login_page():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<h2 style='text-align: center; color: #4f46e5; margin-top: 50px;'>学情分析与教学决策系统</h2>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["账号登录", "注册账号"])
        with tab1:
            u = st.text_input("用户名", key="login_u")
            p = st.text_input("密码", type="password", key="login_p")
            if st.button("立即登录", type="primary", use_container_width=True):
                user = verify_user(u, p)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else: st.error("用户名或密码错误")
        with tab2:
            ru = st.text_input("新用户名", key="reg_u")
            rp = st.text_input("新密码", type="password", key="reg_p")
            role = st.selectbox("角色", ["teacher", "student"], format_func=lambda x: "教师" if x == "teacher" else "学生")
            sid = st.text_input("学生ID（学生必填，如 S001）")
            if st.button("注册", type="primary", use_container_width=True):
                if role == "student" and not sid: st.warning("请填写学生ID")
                else:
                    ok, msg = register_user(ru, rp, role, sid)
                    if ok: st.success("注册成功")
                    else: st.error(msg)
