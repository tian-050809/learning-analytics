import streamlit as st
from styles import page_header

def metric_card(label, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def badge(text, color="blue"):
    return f'<span class="badge badge-{color}">{text}</span>'

def panel_start():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

def panel_end():
    st.markdown('</div>', unsafe_allow_html=True)

def evidence_item(text):
    st.markdown(f'<div class="evidence-item">{text}</div>', unsafe_allow_html=True)

def cause_item(text):
    st.markdown(f'<div class="cause-item">{text}</div>', unsafe_allow_html=True)

def gap_item(text):
    st.markdown(f'<div class="gap-item">{text}</div>', unsafe_allow_html=True)

def correct_color(rate):
    if rate >= 0.8:
        return "green"
    if rate >= 0.6:
        return "amber"
    return "red"
