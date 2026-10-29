import streamlit as st

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
:root { --primary: #4f46e5; --bg: #f4f6fb; --ink: #0f172a; }
html, body, [class*="css"] { font-family: 'Noto Sans SC', sans-serif !important; }
.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] { background: #0b1220; }
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

.brand-box { display: flex; align-items: center; gap: 12px; padding: 10px 0 20px 0; }
.brand-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #6366f1, #06b6d4); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.user-box { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px; margin-bottom: 20px; }

.metric-card {
    background: #fff; padding: 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    border: 1px solid #e2e8f0; position: relative; overflow: hidden;
}
.metric-card::before { content: ""; position: absolute; left: 0; top: 0; width: 4px; height: 100%; background: linear-gradient(180deg, #6366f1, #06b6d4); }
.metric-label { font-size: 0.8rem; color: #64748b; font-weight: 600; margin-bottom: 8px; }
.metric-value { font-size: 2rem; font-weight: 800; color: #0f172a; }

.page-title { font-size: 1.8rem; font-weight: 900; background: linear-gradient(90deg, #4f46e5, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0; }
.page-sub { font-size: 0.9rem; color: #64748b; margin-top: 4px; margin-bottom: 20px; }
</style>
"""
def inject_css(): st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
def page_header(title, subtitle=""):
    st.markdown(f'<div class="page-title">{title}</div><div class="page-sub">{subtitle}</div>', unsafe_allow_html=True)
def metric_card(label, value):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
