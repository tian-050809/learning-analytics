import streamlit as st
from db import init_db
from styles import inject_css
from auth import login_page

st.set_page_config(page_title="学情分析系统", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_css()
init_db()

if "user" not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    login_page()
else:
    user = st.session_state.user
    with st.sidebar:
        st.markdown("""
        <div class="brand-box">
            <div class="brand-icon">📊</div>
            <div>
                <div style="font-weight:700; color:#fff;">学情分析系统</div>
                <div style="font-size:12px; color:#94a3b8;">智能决策支持</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="user-box"><div style="color:#fff;font-weight:600;">{user["username"]}</div><div>{"教师" if user["role"]=="teacher" else "学生"}</div></div>', unsafe_allow_html=True)
        if st.button("退出登录", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    if user["role"] == "teacher":
        from pages import teacher
        teacher.render(user)
    else:
        from pages import student
        student.render(user)
