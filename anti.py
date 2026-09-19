import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import sqlite3
import os
from datetime import datetime
from html import escape
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="NER Logistics Intelligence (SIH 26002)",
    page_icon=os.path.join("public", "assets", "ner-smart-logistics-icon.png"),
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOGIN SYSTEM
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "login_page" not in st.session_state:
    st.session_state.login_page = "home"

USER_USERNAME = os.getenv("NER_USER_USERNAME", "user")
USER_PASSWORD = os.getenv("NER_USER_PASSWORD", "user2026")
ADMIN_USERNAME = os.getenv("NER_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("NER_ADMIN_PASSWORD", "admin2026")


# ---------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------

LOGIN_CSS = """
<style>
.stApp { background: radial-gradient(circle at top, #182c3d 0%, #080d12 58%, #05080b 100%) !important; }
.login-shell { max-width: 980px; margin: 2.5rem auto 1rem; padding: 0 1rem; }
.login-card { background: rgba(10, 15, 20, .98); border: 1px solid rgba(220, 230, 225, .18); border-radius: 14px; box-shadow: 0 24px 70px rgba(0,0,0,.5); overflow: hidden; }
.login-rule { height: 4px; background: linear-gradient(90deg, #df7d25 0 33%, #f4f1e9 33% 66%, #388451 66%); }
.login-heading { padding: 1.5rem 2rem .25rem; color: #f4f7f5; text-align: center; }
.login-heading h1 { font: 800 clamp(1.65rem, 4vw, 2.4rem) 'Manrope', sans-serif; margin: 0; letter-spacing: -.02em; }
.login-heading p { color: #b9c7c8; margin: .55rem 0 0; }
.login-official { color: #d9b27a; font: 600 .78rem 'Inter', sans-serif; letter-spacing: .1em; text-transform: uppercase; }
.login-caption { color: #a7b5b7; font-size: .84rem; text-align: center; padding: 0 2rem 1rem; }
.login-demo { margin-top: .8rem; padding: .55rem .75rem; border: 1px dashed rgba(216,173,111,.5); border-radius: 6px; background: rgba(216,173,111,.08); color: #e6d4b8; font-size: .78rem; line-height: 1.5; }
.login-shell [data-testid="stHorizontalBlock"] { gap: 1rem; }
.login-shell [data-testid="stHorizontalBlock"] > div { background: #17242c; border: 1px solid rgba(180, 202, 194, .16); border-radius: 10px; padding: 1rem 1.2rem; }
.login-shell [data-testid="stTextInput"] label { color: #d6e1dd !important; }
.login-shell [data-testid="stTextInput"] input { background: #0c141a !important; color: #f5f8f6 !important; border-color: #52666c !important; }
.login-shell .stButton > button { background: #172b3a !important; border-color: #62806f !important; color: #f3f7f4 !important; }
.login-shell .stButton > button:hover { background: #23465a !important; border-color: #d9b27a !important; }
.login-footer { color: #88999d; text-align: center; font-size: .76rem; padding: 1rem 0 0; }
</style>
"""

st.markdown(LOGIN_CSS, unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown('<div class="login-shell"><div class="login-card"><div class="login-rule"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="login-heading">
            <div class="login-official">भारत सरकार · Government of India</div>
            <h1>NER Smart Logistics</h1>
            <p>Accessibility and field operations platform for the North Eastern Region</p>
        </div>
        <div class="login-caption">Choose your secure access route to continue.</div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Field Official")
        st.write("Submit route conditions, evidence, and location updates.")
        st.markdown(f'<div class="login-demo"><b>Demo access</b><br>Username: <code>{escape(USER_USERNAME)}</code><br>Password: <code>{escape(USER_PASSWORD)}</code></div>', unsafe_allow_html=True)
        if st.button("Continue as Field Official", use_container_width=True):
            st.session_state.login_page = "user"
    with col2:
        st.subheader("Administrator")
        st.write("Review submissions, publish notices, and manage operations.")
        st.markdown(f'<div class="login-demo"><b>Demo access</b><br>Username: <code>{escape(ADMIN_USERNAME)}</code><br>Password: <code>{escape(ADMIN_PASSWORD)}</code></div>', unsafe_allow_html=True)
        if st.button("Continue as Administrator", use_container_width=True):
            st.session_state.login_page = "admin"


    # -----------------------------------------------------
    if st.session_state.login_page == "user":
        st.markdown("---")
        st.subheader("Field Official Login")

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Sign in as Field Official", use_container_width=True):
            if username == USER_USERNAME and password == USER_PASSWORD:

                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.rerun()

            else:
                st.error("❌ Invalid username or password")


    # -----------------------------------------------------
    if st.session_state.login_page == "admin":
        st.markdown("---")
        st.subheader("Administrator Login")

        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("Sign in as Administrator", use_container_width=True):
            if (
                admin_username == ADMIN_USERNAME
                and admin_password == ADMIN_PASSWORD
            ):

                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.rerun()

            else:
                st.error("❌ Invalid admin credentials")


    st.markdown('<div class="login-footer">Official operations portal · Secure access · Government of India</div></div></div>', unsafe_allow_html=True)
    st.stop()
# =========================================================
# PORTAL STYLE AND DESIGN TOKENS
# =========================================================

COMMAND_CENTER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg-base: #07090b;
    --bg-surface: #101316;
    --bg-card: rgba(16, 19, 22, 0.96);
    --bg-card-hover: rgba(25, 29, 32, 1);
    --border-dim: rgba(205, 214, 209, 0.15);
    --border-neon: rgba(205, 214, 209, 0.26);
    --border-glow: 0 0 0 rgba(0, 0, 0, 0);
    --accent-cyan: #d8e5df;
    --accent-blue: #c1d1df;
    --accent-emerald: #8fc5a4;
    --accent-amber: #d8ad6f;
    --accent-rose: #dd9994;
    --text-primary: #f4f5f2;
    --text-secondary: #c8cfcc;
    --text-muted: #9aa4a4;
}

/* Background & Core Typography */
.stApp {
    background: linear-gradient(180deg, #07090b 0%, #0d1012 100%) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Subtle surface texture */
.stApp::before {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    z-index: 999;
    pointer-events: none;
    opacity: 0.7;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1012 0%, #080a0c 100%) !important;
    border-right: 1px solid var(--border-dim) !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-family: 'Manrope', sans-serif !important;
    text-transform: none !important;
    letter-spacing: 0.02em !important;
    color: var(--text-primary) !important;
}

/* Top Command Header */
.command-header {
    background: linear-gradient(135deg, rgba(22, 24, 26, 0.98) 0%, rgba(9, 11, 13, 0.99) 100%);
    border: 1px solid var(--border-neon);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.18), inset 0 1px 0 rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 22px 28px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(8px);
}

.command-header::after {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-amber), var(--accent-emerald), transparent);
}

.header-top-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.76rem;
    color: var(--accent-blue);
    letter-spacing: 0.12em;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.header-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: 0.02em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 14px;
    text-shadow: none;
}

.header-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: var(--text-secondary);
    letter-spacing: 0.01em;
    margin-top: 6px;
    margin-bottom: 0;
}

.status-beacon {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #10b981;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}

.beacon-dot {
    width: 8px;
    height: 8px;
    background: #3f8f7d;
    border-radius: 50%;
    box-shadow: 0 0 0 rgba(0,0,0,0);
    animation: pulse-beacon 2s infinite;
}

@keyframes pulse-beacon {
    0% { transform: scale(0.9); opacity: 0.8; }
    50% { transform: scale(1.15); opacity: 1; }
    100% { transform: scale(0.9); opacity: 0.8; }
}

/* KPI Telemetry Grid */
.telemetry-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.18);
    position: relative;
    transition: all 0.25s ease;
    backdrop-filter: blur(10px);
}

.telemetry-card:hover {
    border-color: rgba(167,214,198,0.45);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
}

.telemetry-card::before {
    content: "";
    position: absolute;
    top: 0; left: 15%; width: 70%; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}

.telemetry-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.telemetry-value {
    font-family: 'Manrope', sans-serif;
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 6px 0 2px 0;
    text-shadow: none;
}

.telemetry-badge {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
}

.badge-cyan { background: rgba(0, 242, 254, 0.12); color: var(--accent-cyan); border: 1px solid rgba(0, 242, 254, 0.3); }
.badge-rose { background: rgba(244, 63, 94, 0.12); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.3); }
.badge-amber { background: rgba(245, 158, 11, 0.12); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-emerald { background: rgba(16, 185, 129, 0.12); color: var(--accent-emerald); border: 1px solid rgba(16, 185, 129, 0.3); }

/* Tactical Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(11, 17, 32, 0.8) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 10px !important;
    padding: 6px 8px !important;
    gap: 8px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.04em !important;
    text-transform: none !important;
    color: var(--text-secondary) !important;
    padding: 10px 18px !important;
    border-radius: 8px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    border-color: rgba(56, 189, 248, 0.2) !important;
    background: rgba(56, 189, 248, 0.05) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(93,118,109,0.08), rgba(93,118,109,0.04)) !important;
    border: 1px solid var(--border-neon) !important;
    color: var(--accent-cyan) !important;
    box-shadow: none !important;
}

/* Glass Panels & HUD Frames */
.hud-glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
    margin-bottom: 18px;
    backdrop-filter: blur(12px);
    position: relative;
}

.hud-panel-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    text-transform: none;
    letter-spacing: 0.02em;
    color: var(--accent-cyan);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Map HUD Wrapper */
.map-hud-frame {
    border: 1px solid var(--border-neon);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 25px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(0, 242, 254, 0.08);
    position: relative;
}

.map-hud-header {
    background: rgba(11, 17, 32, 0.95);
    border-bottom: 1px solid var(--border-dim);
    padding: 10px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: var(--text-secondary);
}

/* Tactical Alert Banner */
.tactical-alert-container {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid var(--accent-rose);
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.35);
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 22px;
    animation: alert-glow 3s infinite;
}

@keyframes alert-glow {
    0% { border-color: rgba(244, 63, 94, 0.4); }
    50% { border-color: rgba(244, 63, 94, 1); box-shadow: 0 0 30px rgba(244, 63, 94, 0.5); }
    100% { border-color: rgba(244, 63, 94, 0.4); }
}

.alert-header-row {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Manrope', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #b35d57;
    margin-bottom: 8px;
}

.alert-meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-secondary);
    background: rgba(0, 0, 0, 0.3);
    padding: 10px 14px;
    border-radius: 6px;
    margin-top: 8px;
    margin-bottom: 12px;
}

/* Portal buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(26,35,38,0.95) 0%, rgba(17,26,29,0.97) 100%) !important;
    color: var(--text-primary) !important;
    border: 1px solid rgba(168,191,182,0.28) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    text-transform: none !important;
    padding: 10px 20px !important;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.18) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    border-color: rgba(167,214,198,0.5) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 5px 14px rgba(0, 0, 0, 0.22) !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #b98c4b 0%, #9a6d2d 100%) !important;
    color: #fff !important;
    border: none !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 14px rgba(155,109,45,0.22) !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #c5975b 0%, #a77b3a 100%) !important;
    box-shadow: 0 8px 18px rgba(155,109,45,0.26) !important;
}

/* Metric Widgets Styling */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--text-secondary) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}

/* Responsive Overrides */
@media (max-width: 768px) {
    .header-title { font-size: 1.3rem; }
    .command-header { padding: 16px; }
    .telemetry-value { font-size: 1.3rem; }
    .alert-meta-grid { grid-template-columns: 1fr; }
}

/* Government portal surfaces */
.portal-reveal {
    position: fixed;
    inset: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #07111f;
    animation: portal-reveal-hide 2.2s ease forwards;
    pointer-events: none;
}
.portal-reveal::before, .portal-reveal::after {
    content: "";
    position: absolute;
    top: 0;
    width: 50%;
    height: 100%;
    background: linear-gradient(135deg, #0e2940, #07111f);
    animation: portal-door-open 1.6s cubic-bezier(.77,0,.18,1) .35s forwards;
}
.portal-reveal::before { left: 0; transform-origin: left; border-right: 1px solid #49c5b6; }
.portal-reveal::after { right: 0; transform-origin: right; border-left: 1px solid #49c5b6; }
.portal-reveal-content { position: relative; z-index: 1; text-align: center; color: #ecf7f4; }
.portal-reveal-mark { font-size: 2.8rem; color: #f4c95d; }
.portal-reveal-content strong { display: block; margin-top: 12px; font: 700 1rem 'Rajdhani', sans-serif; letter-spacing: 2px; text-transform: uppercase; }
@keyframes portal-door-open { to { transform: scaleX(0); } }
@keyframes portal-reveal-hide { 0%, 76% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }
.notice-rail { border: 1px solid rgba(168,191,182,0.20); border-left: 5px solid #a7d6c6; background: linear-gradient(135deg, rgba(18,28,31,0.95), rgba(13,20,22,0.98)); border-radius: 10px; padding: 14px 18px; margin: 0 0 20px; box-shadow: 0 8px 18px rgba(0,0,0,0.14); }
.notice-kicker { color: #a7d6c6; font: 700 .72rem 'Inter', sans-serif; letter-spacing: 0.08em; }
.notice-title { color: #edf3f0; font: 700 1.05rem 'Manrope', sans-serif; margin: 6px 0 8px; }
.notice-body { color: #c7d0cd; font-size: .9rem; margin: 0; line-height: 1.6; }
.notice-entry { padding: 12px 14px; border: 1px solid rgba(168,191,182,0.14); background: rgba(17,27,30,0.9); border-radius: 8px; margin-bottom: 10px; }
.notice-entry-label { color: #a7d6c6; font: 700 .72rem 'Inter', sans-serif; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; }
.notice-entry-title { color: #edf3f0; font: 700 1rem 'Manrope', sans-serif; margin-bottom: 6px; }
.notice-entry-body { color: #c7d0cd; font-size: .88rem; line-height: 1.5; margin: 0; }
.updates-heading { color: #eefcf9; font: 700 1rem 'Rajdhani', sans-serif; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 8px; }
.official-footer { border-top: 1px solid rgba(73, 197, 182, .35); margin-top: 34px; padding: 26px 4px 12px; color: #9bb4b5; }
.official-footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr 1.2fr; gap: 22px; }
.official-footer h3 { color: #f4c95d; font: 700 .86rem 'Rajdhani', sans-serif; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 9px; }
.official-footer p, .official-footer li { font-size: .78rem; line-height: 1.6; }
.official-footer ul { list-style: none; padding: 0; margin: 0; }
.footer-bottom { border-top: 1px solid rgba(155, 180, 181, .18); margin-top: 20px; padding-top: 12px; font-size: .7rem; display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
@media (max-width: 768px) { .official-footer-grid { grid-template-columns: 1fr 1fr; } }

/* Government portal surfaces */
.stApp { background: linear-gradient(180deg, #07090b 0%, #0d1012 100%) !important; color: #f4f5f2 !important; }
.block-container { max-width: 1440px; padding-top: 3.5rem !important; }
.stApp [data-testid="stHorizontalBlock"]:has(.govt-search) { background: #10151a; border: 1px solid rgba(205,214,209,.16); border-bottom: 0; border-radius: 8px 8px 0 0; padding: 18px 22px 12px; margin-top: 4px; }
.govt-header-shell { background: #10151a; border: 1px solid rgba(205,214,209,.16); border-radius: 0 0 8px 8px; box-shadow: 0 8px 20px rgba(0,0,0,.22); overflow: hidden; margin-bottom: 18px; }
.govt-header-rule { height: 3px; background: linear-gradient(90deg, #d58b43 0 33%, #d7ddd9 33% 66%, #649b73 66%); border-bottom: 1px solid rgba(255,255,255,.08); }
.govt-header-content { display: grid; grid-template-columns: 1.25fr 1fr 1.25fr; gap: 20px; align-items: center; padding: 16px 22px; }
.govt-identity { display: flex; align-items: center; gap: 12px; color: #f2f4f1; }
.govt-ministry { font: 700 1.02rem 'Manrope', sans-serif; line-height: 1.25; }
.govt-country { color: #abb8b8; font-size: .82rem; margin-top: 4px; }
.govt-brand-center { text-align: center; color: #e4ebe7; }
.govt-center-note { text-align: center; color: #d8ad6f; font: 700 .92rem 'Manrope', sans-serif; line-height: 1.35; }
.govt-center-note span { color: #aebcba; font: 400 .74rem 'Inter', sans-serif; }
.govt-search { display: flex; justify-content: flex-end; align-items: center; gap: 8px; }
.govt-search-label { display: none; }
.govt-search input { min-width: 210px; background: #080c10 !important; border: 1px solid #526168 !important; color: #f2f4f1 !important; }
.govt-search input::placeholder { color: #9da9ad !important; opacity: 1; }
.govt-search [data-testid="stTextInput"] > div { background: transparent !important; }
.portal-nav { display: flex; gap: 24px; padding: 9px 22px; background: #171e24; color: #e8eeeb; font-size: .82rem; flex-wrap: wrap; }
.portal-nav span { opacity: .92; }
.portal-updates { display: flex; align-items: center; gap: 14px; background: #eee9df; border: 1px solid #d8d1c5; color: #243746; padding: 10px 14px; margin: 0 0 18px; font-size: .88rem; }
.portal-updates strong { color: #a85b18; white-space: nowrap; }
.portal-updates a { margin-left: auto; color: #1e5e78; font-weight: 700; white-space: nowrap; }
.gateway { position: fixed; inset: 0; z-index: 1000; display: flex; align-items: center; justify-content: center; background: #132d46; pointer-events: none; animation: gateway-hide 2.4s ease forwards; }
.gateway-panel { width: min(560px, 82vw); text-align: center; color: #ffffff; padding: 34px; border-top: 4px solid #e67e22; border-bottom: 4px solid #39824d; background: rgba(9, 28, 45, .96); }
.gateway-panel strong { display: block; font: 700 1.15rem 'Manrope', sans-serif; margin: 10px 0 6px; }
.gateway-panel span { color: #c6d2d8; font-size: .86rem; }
.gateway-skip { pointer-events: auto; margin-top: 18px; padding: 7px 16px; border: 1px solid rgba(255,255,255,.5); border-radius: 3px; background: transparent; color: #fff; cursor: pointer; }
@keyframes gateway-hide { 0%, 72% { opacity: 1; visibility: visible; } 100% { opacity: 0; visibility: hidden; } }
@media (max-width: 800px) { .govt-header-content { grid-template-columns: 1fr auto; } .govt-brand-center { display: none; } .govt-search input { min-width: 0; width: 42px; } .portal-nav { gap: 14px; } .portal-updates { align-items: flex-start; flex-wrap: wrap; } .portal-updates a { margin-left: 0; } }
</style>
"""

st.markdown(COMMAND_CENTER_CSS, unsafe_allow_html=True)

if "gateway_skipped" not in st.session_state:
    st.session_state.gateway_skipped = False

govt_header_left, govt_header_center, govt_header_right = st.columns([1.25, 1, 1.25])
with govt_header_left:
    st.image(
        os.path.join("public", "assets", "ministry-of-education.png"),
        width=230,
    )
with govt_header_center:
    st.markdown(
        """
        <div class="govt-center-note">North Eastern Region<br><span>Smart logistics and field operations</span></div>
        """,
        unsafe_allow_html=True,
    )
with govt_header_right:
    st.markdown('<div class="govt-search">', unsafe_allow_html=True)
    portal_search = st.text_input(
        "Search this website...",
        placeholder="Search this website...",
        label_visibility="collapsed",
        key="portal_search",
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="govt-header-shell">
        <div class="govt-header-rule"></div>
        <div class="portal-nav">
            <span>Home</span><span>About the Platform</span><span>Field Updates</span>
            <span>Regional Insights</span><span>Resources</span><span>Contact</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
if not st.session_state.gateway_skipped:
    st.markdown(
        """
        <div class="gateway" aria-label="Opening North Eastern Region government portal">
            <div class="gateway-panel">
                <div style="font-size: 2rem; color: #e67e22;">भारत सरकार</div>
                <strong>North Eastern Region Operations Portal</strong>
                <span>Connecting field information with timely regional decisions</span><br>
                <button class="gateway-skip" onclick="this.closest('.gateway').remove()">Skip introduction</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# AI MODEL CACHING & TRAINING
# XGBOOST RISK PREDICTOR (PRESERVED BACKEND)
# =========================================================

@st.cache_resource
def load_trained_risk_model():
    np.random.seed(42)
    n_samples = 1500

    data = {
        "rainfall_mm": np.random.uniform(10, 350, n_samples),
        "soil_moisture": np.random.uniform(20, 95, n_samples),
        "slope_degrees": np.random.uniform(5, 65, n_samples),
        "historical_landslide_freq": np.random.poisson(1, n_samples),
    }

    df = pd.DataFrame(data)

    risk_rule = (
        (df["rainfall_mm"] > 180).astype(int) * 0.4
        + (df["soil_moisture"] > 80).astype(int) * 0.3
        + (df["slope_degrees"] > 40).astype(int) * 0.3
    )

    df["disruption_risk"] = (
        risk_rule
        + np.random.normal(0, 0.1, n_samples)
        > 0.5
    ).astype(int)

    X = df[
        [
            "rainfall_mm",
            "soil_moisture",
            "slope_degrees",
            "historical_landslide_freq",
        ]
    ]

    y = df["disruption_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)
    return model

# Load trained AI model
ml_risk_model = load_trained_risk_model()

# =========================================================
# SQLITE DATABASE (PRESERVED BACKEND)
# =========================================================

DB_NAME = "field_reports.db"
IMAGE_FOLDER = "field_report_images"
DOCUMENT_FOLDER = "field_report_documents"
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

ANNOUNCEMENTS = [
    {
        "label": "PRIORITY NOTICE",
        "title": "Monsoon corridor readiness review is now active",
        "body": "Field teams are requested to submit route conditions and geo-tagged evidence before 18:00 IST.",
        "tone": "priority",
    },
    {
        "label": "SERVICE UPDATE",
        "title": "NER logistics intelligence desk is online",
        "body": "Live field submissions are being reviewed by the regional operations desk.",
        "tone": "info",
    },
]

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS field_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT,
            description TEXT,
            latitude REAL,
            longitude REAL,
            report_time TEXT,
            image_path TEXT,
            submitted_by TEXT DEFAULT 'field-official',
            category TEXT DEFAULT 'Field incident',
            state TEXT DEFAULT 'Assam',
            district TEXT DEFAULT '',
            document_path TEXT DEFAULT '',
            status TEXT DEFAULT 'Pending',
            reviewed_by TEXT,
            reviewed_time TEXT
        )
    """)
    existing_columns = {
        row[1] for row in cursor.execute("PRAGMA table_info(field_reports)").fetchall()
    }
    migrations = {
        "submitted_by": "TEXT DEFAULT 'field-official'",
        "category": "TEXT DEFAULT 'Field incident'",
        "state": "TEXT DEFAULT 'Assam'",
        "district": "TEXT DEFAULT ''",
        "document_path": "TEXT DEFAULT ''",
        "status": "TEXT DEFAULT 'Pending'",
        "reviewed_by": "TEXT",
        "reviewed_time": "TEXT",
    }
    for column, definition in migrations.items():
        if column not in existing_columns:
            cursor.execute(f"ALTER TABLE field_reports ADD COLUMN {column} {definition}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            label TEXT NOT NULL,
            published INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)
    if cursor.execute("SELECT COUNT(*) FROM announcements").fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO announcements (title, body, label, created_at) VALUES (?, ?, ?, ?)",
            [(item["title"], item["body"], item["label"], datetime.now().isoformat()) for item in ANNOUNCEMENTS],
        )
    conn.commit()
    conn.close()

init_database()

# =========================================================
# ALERT NOTIFICATION SYSTEM (PRESERVED BACKEND)
# =========================================================

def get_latest_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            id,
            incident_type,
            description,
            latitude,
            longitude,
            report_time,
            image_path
        FROM field_reports
        ORDER BY id DESC
        LIMIT 1
    """)
    report = cursor.fetchone()
    conn.close()
    return report

def get_latest_report_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM field_reports")
    result = cursor.fetchone()
    conn.close()
    if result and result[0] is not None:
        return result[0]
    return 0

# =========================================================
# INITIALIZE NOTIFICATION STATE
# =========================================================

if "last_seen_report_id" not in st.session_state:
    st.session_state.last_seen_report_id = get_latest_report_id()

if "new_report_alert" not in st.session_state:
    st.session_state.new_report_alert = None

# =========================================================
# LIVE ALERT CHECK (MODERNIZED TACTICAL HUD UI)
# =========================================================

@st.fragment(run_every=5)
def live_alert_notification():
    latest_report = get_latest_report()
    if latest_report is None:
        return

    (
        report_id,
        report_type,
        report_description,
        report_latitude,
        report_longitude,
        report_time,
        report_image
    ) = latest_report

    if report_id > st.session_state.last_seen_report_id:
        st.session_state.last_seen_report_id = report_id
        st.session_state.new_report_alert = {
            "id": report_id,
            "type": report_type,
            "description": report_description,
            "lat": report_latitude,
            "lon": report_longitude,
            "time": report_time
        }

    if st.session_state.new_report_alert:
        alert = st.session_state.new_report_alert
        st.markdown(
            f"""
            <div class="tactical-alert-container">
                <div class="alert-header-row">
                    <span style="font-size: 1.4rem;">🚨</span>
                    <span>TACTICAL INCIDENT DISPATCH • REPORT #{alert['id']}</span>
                    <span style="margin-left: auto; font-size: 0.75rem; background: rgba(244,63,94,0.3); border: 1px solid #f43f5e; padding: 2px 8px; border-radius: 4px; font-family: 'JetBrains Mono', monospace;">PRIORITY HAZARD</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">
                    {alert['type']}
                </div>
                <div class="alert-meta-grid">
                    <div>📍 <b>COORDINATES:</b> {alert['lat']:.6f}, {alert['lon']:.6f}</div>
                    <div>🕒 <b>TIMESTAMP:</b> {alert['time']}</div>
                    <div>📡 <b>STATUS:</b> BROADCAST ACTIVE</div>
                </div>
                <div style="font-size: 0.92rem; color: #cbd5e1; margin-bottom: 8px;">
                    <b>Field Intelligence:</b> {alert['description']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        ack_col1, ack_col2 = st.columns([1, 4])
        with ack_col1:
            if st.button("✅ ACKNOWLEDGE ALERT", key=f"mark_alert_{alert['id']}"):
                st.session_state.new_report_alert = None
                st.rerun()

# Execute top alert check
live_alert_notification()

# =========================================================
# SAVE FIELD REPORT (PRESERVED BACKEND)
# =========================================================

def save_field_report(
    incident_type,
    description,
    latitude,
    longitude,
    report_time,
    image_file,
    submitted_by="field-official",
    category="Field incident",
    state="Assam",
    district="",
    document_file=None,
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    image_path = ""
    document_path = ""

    if image_file is not None and image_file.size > 0:
        original_name = image_file.name
        extension = original_name.rsplit(".", 1)[1].lower() if "." in original_name else "jpg"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        image_filename = f"incident_{timestamp}.{extension}"
        image_path = os.path.join(IMAGE_FOLDER, image_filename)

        with open(image_path, "wb") as file:
            file.write(image_file.getvalue())

    if document_file is not None and document_file.size > 0:
        original_name = document_file.name
        extension = original_name.rsplit(".", 1)[1].lower() if "." in original_name else "pdf"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        document_filename = f"field_document_{timestamp}.{extension}"
        document_path = os.path.join(DOCUMENT_FOLDER, document_filename)
        with open(document_path, "wb") as file:
            file.write(document_file.getvalue())

    cursor.execute("""
        INSERT INTO field_reports
        (
            incident_type,
            description,
            latitude,
            longitude,
            report_time,
            image_path,
            submitted_by,
            category,
            state,
            district,
            document_path,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        incident_type,
        description,
        latitude,
        longitude,
        report_time,
        image_path,
        submitted_by,
        category,
        state,
        district,
        document_path,
        "Pending"
    ))

    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id, image_path


def fetch_announcements():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT label, title, body FROM announcements WHERE published = 1 ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def publish_announcement(label, title, body):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO announcements (title, body, label, published, created_at) VALUES (?, ?, ?, 1, ?)",
        (title.strip(), body.strip(), label.strip(), datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def fetch_field_reports(status=None, search="", state=None, district=None, category=None):
    conn = sqlite3.connect(DB_NAME)
    query = """
         SELECT id, incident_type, description, latitude, longitude, report_time,
             image_path, submitted_by, category, state, district, document_path, status
        FROM field_reports
        WHERE 1 = 1
    """
    params = []
    if status and status != "All":
        query += " AND status = ?"
        params.append(status)
    if state and state != "All":
        query += " AND state = ?"
        params.append(state)
    if district and district != "All":
        query += " AND district = ?"
        params.append(district)
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    if search.strip():
        query += " AND (incident_type LIKE ? OR description LIKE ? OR submitted_by LIKE ? OR state LIKE ? OR district LIKE ? OR category LIKE ?)"
        needle = f"%{search.strip()}%"
        params.extend([needle, needle, needle, needle, needle, needle])
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def update_report_status(report_id, status, reviewer):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "UPDATE field_reports SET status = ?, reviewed_by = ?, reviewed_time = ? WHERE id = ?",
        (status, reviewer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), report_id),
    )
    conn.commit()
    conn.close()


def update_report_description(report_id, description):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE field_reports SET description = ? WHERE id = ?", (description, report_id))
    conn.commit()
    conn.close()


def delete_report(report_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM field_reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()

# =========================================================
# CITY COORDINATES
# =========================================================

CITY_COORDS = {
    "Guwahati": [26.1445, 91.7362],
    "Shillong": [25.5788, 91.8933],
    "Imphal": [24.8074, 93.9384],
    "Agartala": [23.8315, 91.2868],
    "Aizawl": [23.7271, 92.7176],
    "Itanagar": [27.0844, 93.6053],
    "Kohima": [25.6751, 94.1086],
    "Gangtok": [27.3389, 88.6065],
    "Bareilly": [28.3670, 79.4304]
}

# =========================================================
# OPENWEATHER API KEY
# =========================================================

WEATHER_API_KEY = "8588811be768c6415d90e64a77e7c41c"

# =========================================================
# API 1 — LIVE WEATHER (PRESERVED BACKEND)
# =========================================================

def fetch_live_weather(lat, lon):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"] * 3.6,
                "condition": data["weather"][0]["description"],
                "city": data.get("name", "Unknown"),
                "visibility": data.get("visibility", 0) / 1000
            }
        elif response.status_code == 401:
            st.error("❌ OpenWeather API key is invalid or not activated.")
        elif response.status_code == 404:
            st.error("❌ Weather location not found.")
        else:
            st.error(f"❌ Weather API Error: {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("⏱️ Weather API request timed out.")
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Weather connection error: {e}")
    except Exception as e:
        st.error(f"⚠️ Weather data error: {e}")
    return None

# =========================================================
# API 2 — PREDICTIVE DISRUPTION (PRESERVED BACKEND)
# =========================================================

def fetch_predictive_disruptions(lat, lon):
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&hourly=precipitation_probability,precipitation,windspeed_10m"
            "&forecast_days=1"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        res = response.json()

        if "hourly" in res:
            precip_prob = res["hourly"].get("precipitation_probability", [0])
            precip = res["hourly"].get("precipitation", [0])
            winds = res["hourly"].get("windspeed_10m", [0])

            max_prob = max(precip_prob) if precip_prob else 0
            max_precip = max(precip) if precip else 0.0
            max_wind = max(winds) if winds else 0.0

            disruption_risk = "Low"
            alerts = []

            if max_precip > 15.0 or max_prob > 80:
                disruption_risk = "High"
                alerts.append("🚨 **High Landslide & Flash Flood Risk** predicted in next 24h.")
            elif max_precip > 5.0 or max_prob > 50:
                disruption_risk = "Moderate"
                alerts.append("⚠️ **Moderate Waterlogging Risk** along mountain passes.")

            if max_wind > 35.0:
                alerts.append("💨 **High Wind Hazard:** Risk of fallen trees/debris.")

            if not alerts:
                alerts.append("✅ **Clear Driving Conditions:** Minimal weather blockage risk.")

            return disruption_risk, max_prob, max_precip, alerts

    except Exception as e:
        st.error(f"Predictive Engine Error: {e}")

    return "Unknown", 0, 0.0, ["Unable to calculate predictive risk."]

# =========================================================
# API 3 — ELEVATION (PRESERVED BACKEND)
# =========================================================

def fetch_elevation_profile(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        res = response.json()
        elevation = res.get("elevation", [0])
        if elevation:
            return elevation[0]
    except Exception:
        pass
    return 500

# =========================================================
# API 4 — OSRM ROUTING (PRESERVED BACKEND)
# =========================================================

def fetch_osrm_routes(start_lat, start_lon, end_lat, end_lon):
    osrm_url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        "?overview=full&geometries=geojson&alternatives=true"
    )
    try:
        response = requests.get(osrm_url, timeout=10)
        response.raise_for_status()
        res = response.json()
        if res.get("routes"):
            routes_data = []
            for route in res["routes"]:
                routes_data.append({
                    "geometry": route["geometry"],
                    "distance_km": route["distance"] / 1000,
                    "duration_min": route["duration"] / 60
                })
            return routes_data
    except Exception as e:
        st.error(f"Routing API Error: {e}")
    return []

# =========================================================
# API 5 — REROUTING (PRESERVED BACKEND)
# =========================================================

def fetch_rerouted_route(start_lat, start_lon, via_lat, via_lon, end_lat, end_lon):
    osrm_url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{via_lon},{via_lat};{end_lon},{end_lat}"
        "?overview=full&geometries=geojson"
    )
    try:
        response = requests.get(osrm_url, timeout=15)
        if response.status_code != 200:
            st.error(f"❌ Rerouting API Error: {response.status_code}")
            return None
        data = response.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            st.error("❌ No rerouted route found.")
            return None

        route = data["routes"][0]
        return {
            "geometry": route["geometry"],
            "distance_km": route["distance"] / 1000,
            "duration_min": route["duration"] / 60
        }
    except requests.exceptions.Timeout:
        st.error("⏱️ Rerouting API timed out.")
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Rerouting connection error: {e}")
    except Exception as e:
        st.error(f"⚠️ Rerouting error: {e}")
    return None

# =========================================================
# MULTILINGUAL UI DICTIONARY (PRESERVED)
# =========================================================

LANGUAGES = {
    "English": {
        "title": "NER Smart Logistics & Accessibility Intelligence",
        "subtitle": "Ministry of Development of North Eastern Region (MDoNER) • Field Operations Dashboard",
        "analyze": "Review corridor and risk conditions",
        "primary_route": "Primary Route",
        "alt_route": "Alternate Route",
        "cargo": "Cargo Category",
        "fleet": "Live Fleet Tracking"
    },
    "Hindi (हिन्दी)": {
        "title": "पूर्वोत्तर स्मार्ट लॉजिस्टिक्स एवं सुगम मार्ग प्लेटफॉर्म",
        "subtitle": "पूर्वोत्तर क्षेत्र विकास मंत्रालय (MDoNER) • संचालन डैशबोर्ड",
        "analyze": "मार्ग और जोखिम की स्थिति देखें",
        "primary_route": "मुख्य मार्ग",
        "alt_route": "वैकल्पिक मार्ग",
        "cargo": "सामग्री श्रेणी",
        "fleet": "लाइव वाहन ट्रैकिंग"
    },
    "Assamese (অসমীয়া)": {
        "title": "উত্তৰ-পূৰ্বাঞ্চল স্মাৰ্ট লজিষ্টিক আৰু পথাৰ যোগাযোগ প্লেটফৰ্ম",
        "subtitle": "MDoNER • অপাৰেশন ড্যাশবোর্ড",
        "analyze": "পথ আৰু বিপদাশংকা পৰিস্থিতি চাওক",
        "primary_route": "মুখ্য পথ",
        "alt_route": "বিকল্প পথ",
        "cargo": "পৰিবহণ সামগ্ৰী",
        "fleet": "লাইভ বাহন ট্রেকিং"
    }
}

# =========================================================
# SIDEBAR CONTROLS (MISSION CONTROL DECK)
# =========================================================

st.sidebar.image(
    os.path.join("public", "assets", "ner-smart-logistics-icon.png"),
    width=150,
)
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0 16px 0; border-bottom: 1px solid rgba(167,214,198,0.18); margin-bottom: 15px;">
        <div style="font-family: 'Manrope', sans-serif; font-size: 1.12rem; font-weight: 800; color: #d8e5df; letter-spacing: 0.08em;">
            Operations Desk
        </div>
        <div style="font-family: 'Inter', sans-serif; font-size: 0.72rem; color: #9aa4a4; letter-spacing: 0.08em;">
            Regional logistics overview
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

lang_choice = st.sidebar.selectbox(
    "🌐 System Interface Language",
    ["English", "Hindi (हिन्दी)", "Assamese (অসমীয়া)"],
    key="sidebar_lang_select"
)

txt = LANGUAGES[lang_choice]

st.sidebar.markdown(
    """
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.88rem; font-weight: 700; color: #38bdf8; letter-spacing: 1.2px; text-transform: uppercase; margin: 16px 0 8px 0;">
        📍 Corridor Coordinates
    </div>
    """,
    unsafe_allow_html=True
)

source = st.sidebar.selectbox(
    "Source District Hub",
    list(CITY_COORDS.keys()),
    index=0,
    key="source_district_select"
)

destination = st.sidebar.selectbox(
    "Destination District Hub",
    list(CITY_COORDS.keys()),
    index=1,
    key="destination_district_select"
)

st.sidebar.markdown(
    """
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.88rem; font-weight: 700; color: #38bdf8; letter-spacing: 1.2px; text-transform: uppercase; margin: 16px 0 8px 0;">
        🔄 Tactical Override
    </div>
    """,
    unsafe_allow_html=True
)

enable_rerouting = st.sidebar.checkbox(
    "Dynamic Blockage Reroute",
    value=False,
    key="enable_rerouting"
)

reroute_city = None
if enable_rerouting:
    reroute_options = [
        city for city in CITY_COORDS.keys()
        if city not in [source, destination]
    ]
    reroute_city = st.sidebar.selectbox(
        "Reroute Via Intermediate Node",
        reroute_options,
        key="reroute_city_select"
    )

st.sidebar.markdown(
    """
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.88rem; font-weight: 700; color: #38bdf8; letter-spacing: 1.2px; text-transform: uppercase; margin: 16px 0 8px 0;">
        📦 Fleet & Payload Profiling
    </div>
    """,
    unsafe_allow_html=True
)

cargo_type = st.sidebar.selectbox(
    "Essential Payload Type",
    [
        "Medicines & Vaccines",
        "Food Supplies",
        "Agricultural Produce",
        "Construction Materials"
    ],
    key="cargo_type_select"
)

vehicle = st.sidebar.selectbox(
    "Transport Carrier Class",
    [
        "Heavy Duty Truck",
        "Mini Freight Carrier",
        "4x4 Emergency Van"
    ],
    key="vehicle_type_select"
)

analyze_clicked = st.sidebar.button(
    txt["analyze"],
    key="analyze_button",
    type="primary"
)
# =========================================================
# HELP & SUPPORT
# =========================================================

st.sidebar.markdown("---")
st.sidebar.markdown("## 🆘 Help & Support")

st.sidebar.caption("Need help? We're here to assist you.")

# Contact Support
st.sidebar.markdown(
    '<a href="tel:+91XXXXXXXXXX">'
    '<button style="width:100%; padding:10px; cursor:pointer;">'
    '📞 Contact Support'
    '</button>'
    '</a>',
    unsafe_allow_html=True
)

# Report an Issue
if st.sidebar.button("🐛 Report an Issue", use_container_width=True):
    st.session_state["show_issue_form"] = True

if st.session_state.get("show_issue_form", False):

    st.sidebar.markdown("### 🐛 Report an Issue")

    issue_type = st.sidebar.selectbox(
        "Issue Type",
        [
            "🗺️ Map Problem",
            "🚨 Alert Problem",
            "🔄 Route/Rerouting Problem",
            "📈 Risk Review Problem",
            "🌐 Website Problem",
            "📌 Other"
        ],
        key="issue_type"
    )

    issue_description = st.sidebar.text_area(
        "Describe the issue",
        placeholder="Tell us what went wrong...",
        key="issue_description"
    )

    if st.sidebar.button("🚀 Submit Issue", use_container_width=True):

        if issue_description.strip():
            st.sidebar.success("✅ Issue reported successfully!")
            st.session_state["show_issue_form"] = False
        else:
            st.sidebar.warning("⚠️ Please describe the issue first.")
# =========================================================
# TOP GOVERNMENT PORTAL HEADER
# =========================================================

st.markdown(
    f"""
    <div class="command-header">
        <div class="header-top-meta">
            <span>GOVERNMENT OF INDIA • MINISTRY OF DEVELOPMENT OF NORTH EASTERN REGION</span>
            <div class="status-beacon">
                <span class="beacon-dot"></span>
                <span>SYSTEM ACTIVE • SIH 26002</span>
            </div>
        </div>
        <h1 class="header-title">
            <span>🚚</span> {txt["title"]}
        </h1>
        <p class="header-subtitle">
            {txt["subtitle"]} | Regional corridor monitoring and operational routing support
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# OFFICIAL UPDATES / ANNOUNCEMENTS
# =========================================================

announcement_rows = fetch_announcements()
if announcement_rows:
    latest_label, latest_title, latest_body = announcement_rows[0]
    st.markdown(
        f"""
        <div class="portal-updates" role="status">
            <strong>Latest Updates</strong>
            <span>{escape(latest_title)}</span>
            <a href="#portal-notices">View All Updates →</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

if portal_search.strip():
    search_term = portal_search.strip().lower()
    matching_notices = [
        row for row in announcement_rows
        if search_term in " ".join(row).lower()
    ]
    matching_reports = fetch_field_reports(search=portal_search.strip())
    st.markdown('<div id="portal-notices"></div>', unsafe_allow_html=True)
    with st.expander(f"Search results for '{escape(portal_search.strip())}'", expanded=True):
        if matching_notices:
            st.write(f"{len(matching_notices)} matching announcement(s)")
            for item_label, item_title, item_body in matching_notices:
                st.markdown(f"**{escape(item_label)}**: {escape(item_title)}")
                st.caption(escape(item_body))
        if matching_reports:
            st.write(f"{len(matching_reports)} matching field submission(s)")
            for report in matching_reports[:5]:
                st.markdown(f"**#{report[0]} · {escape(report[1])} · {escape(report[12])}**")
                st.caption(escape(report[2]))
        if not matching_notices and not matching_reports:
            st.info("No matching announcements or field submissions were found.")

if announcement_rows:
    notice_label, notice_title, notice_body = announcement_rows[0]
    st.markdown(
        f"""
        <div class="notice-rail" role="status">
            <div class="notice-kicker">📢 {escape(notice_label)} • OFFICIAL UPDATE</div>
            <div class="notice-title">{escape(notice_title)}</div>
            <p class="notice-body">{escape(notice_body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander(f"View all {len(announcement_rows)} portal notices"):
        for item_label, item_title, item_body in announcement_rows:
            st.markdown(
                f"""
                <div class="notice-entry">
                    <div class="notice-entry-label">{escape(item_label)}</div>
                    <div class="notice-entry-title">{escape(item_title)}</div>
                    <div class="notice-entry-body">{escape(item_body)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.image(
        os.path.join("public", "assets", "govt-header-reference.png"),
        use_container_width=True,
    )

# =========================================================
# TOP KPI TELEMETRY METRICS
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>🛣️</span> Monitored NER Routes
            </div>
            <div class="telemetry-value">24</div>
            <span class="telemetry-badge badge-cyan">HIGHWAY RADAR ACTIVE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>⚠️</span> Active Disruptions
            </div>
            <div class="telemetry-value" style="color: #ff4d6d;">07</div>
            <span class="telemetry-badge badge-rose">SEVERITY LEVEL 2</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>🌧️</span> Weather Hazard Alerts
            </div>
            <div class="telemetry-value" style="color: #f59e0b;">03</div>
            <span class="telemetry-badge badge-amber">PRECIPITATION ADVISORY</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        """
        <div class="telemetry-card">
            <div class="telemetry-label">
                <span>🚛</span> GPS Supply Fleets
            </div>
            <div class="telemetry-value" style="color: #10b981;">156</div>
            <span class="telemetry-badge badge-emerald">100% ENCRYPTED TELEMETRY</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# =========================================================
# ROUTE COMPUTATION & API CALLS (PRESERVED BACKEND)
# =========================================================

start_lat, start_lon = CITY_COORDS[source]
end_lat, end_lon = CITY_COORDS[destination]

routes = fetch_osrm_routes(start_lat, start_lon, end_lat, end_lon)

rerouted_route = None
if enable_rerouting and reroute_city:
    via_lat, via_lon = CITY_COORDS[reroute_city]
    rerouted_route = fetch_rerouted_route(start_lat, start_lon, via_lat, via_lon, end_lat, end_lon)

dest_weather = fetch_live_weather(end_lat, end_lon)
risk_level, max_prob, max_precip, pred_alerts = fetch_predictive_disruptions(end_lat, end_lon)
dest_elevation = fetch_elevation_profile(end_lat, end_lon)

# =========================================================
# MAIN COMMAND CENTER TABS
# =========================================================

tab_labels = [
    "🗺️ Corridor Map",
    "🚛 Fleet Tracking",
    "📸 Incident Reports",
    "📊 Readiness Matrix",
    "📈 Risk Review",
]
if st.session_state.role == "admin":
    tab_labels.append("🛡️ Admin Operations")
tab_views = st.tabs(tab_labels)
tab_map, tab_fleet, tab_report, tab_district, tab_ai = tab_views[:5]
tab_admin = tab_views[5] if len(tab_views) == 6 else None

# =========================================================
# TAB 1 — STRATEGIC GIS MAP & TACTICAL WEATHER
# =========================================================

with tab_map:
    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            f"""
            <div class="map-hud-frame">
                <div class="map-hud-header">
                    <span><b>🛰️ ROUTE MAP:</b> {source} ➔ {destination}</span>
                    <span><b>STATUS:</b> Live corridor view</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Folium Tactical Dark Map
        m = folium.Map(
            location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2],
            zoom_start=6,
            tiles="CartoDB dark_matter"
        )

        # City Markers
        for city, coords in CITY_COORDS.items():
            folium.CircleMarker(
                location=coords,
                radius=6,
                color="#00f2fe",
                fill=True,
                fill_color="#00f2fe",
                fill_opacity=0.8,
                popup=f"District Hub: {city}",
                tooltip=city
            ).add_to(m)

        # Landslide Road Blockage Marker
        folium.Marker(
            location=[26.1158, 91.7086],
            popup="🚧 Landslide Road Blockage (Route A12)",
            tooltip="Active Disruption Point",
            icon=folium.Icon(color="red", icon="exclamation-sign")
        ).add_to(m)

        # Primary Strategic Route (Cyan Glow)
        if routes:
            folium.GeoJson(
                routes[0]["geometry"],
                name="Primary Route",
                style_function=lambda feature: {
                    "color": "#00f2fe",
                    "weight": 5,
                    "opacity": 0.85
                }
            ).add_to(m)

            # Alternate Route
            if len(routes) > 1:
                folium.GeoJson(
                    routes[1]["geometry"],
                    name="Alternate Route",
                    style_function=lambda feature: {
                        "color": "#3f8f7d",
                        "weight": 4,
                        "dashArray": "6,6",
                        "opacity": 0.9
                    }
                ).add_to(m)

        # Source & Destination Markers
        folium.Marker(
            location=[start_lat, start_lon],
            popup=f"Origin: {source}",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)

        folium.Marker(
            location=[end_lat, end_lon],
            popup=f"Destination: {destination}",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(m)

        # Rerouted Track (Tactical Amber)
        if enable_rerouting and rerouted_route:
            folium.GeoJson(
                rerouted_route["geometry"],
                name="🔄 Live Rerouted Route",
                style_function=lambda feature: {
                    "color": "#f59e0b",
                    "weight": 6,
                    "opacity": 0.95
                },
                tooltip=f"Dynamic Detour via {reroute_city}"
            ).add_to(m)

            via_lat, via_lon = CITY_COORDS[reroute_city]
            folium.Marker(
                location=[via_lat, via_lon],
                popup=f"🔄 Waypoint Reroute: {reroute_city}",
                tooltip=f"Detour Hub: {reroute_city}",
                icon=folium.Icon(color="orange", icon="random")
            ).add_to(m)

        st_folium(m, width="100%", height=460, key="main_route_map")

        # Telemetry Metadata Strip
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 10px 16px; margin-top: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94a3b8; display: flex; flex-wrap: wrap; gap: 14px; justify-content: space-between;">
                <span>📍 <b>CORRIDOR:</b> <span style="color: #f8fafc;">{source} ➔ {destination}</span></span>
                <span>📦 <b>PAYLOAD:</b> <span style="color: #38bdf8;">{cargo_type}</span></span>
                <span>🚛 <b>CARRIER:</b> <span style="color: #38bdf8;">{vehicle}</span></span>
                <span>⛰️ <b>DESTINATION ELEVATION:</b> <span style="color: #10b981;">{dest_elevation} m MSL</span></span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Weather & Predictive Intelligence Column
    with right:
        st.markdown(
            """
            <div class="hud-glass-card">
                <div class="hud-panel-title">
                    <span>🌤️</span> Live Destination Atmospheric Telemetry
                </div>
            """,
            unsafe_allow_html=True
        )

        if dest_weather:
            wcol1, wcol2 = st.columns(2)
            with wcol1:
                st.metric("🌡️ Temperature", f"{dest_weather['temperature']:.1f} °C")
                st.metric("💧 Humidity", f"{dest_weather['humidity']}%")
            with wcol2:
                st.metric("🌡️ Feels Like", f"{dest_weather['feels_like']:.1f} °C")
                st.metric("💨 Wind Speed", f"{dest_weather['wind_speed']:.1f} km/h")

            st.markdown(
                f"""
                <div style="background: rgba(56, 189, 248, 0.1); border-left: 3px solid #38bdf8; padding: 8px 12px; border-radius: 4px; font-size: 0.85rem; margin-top: 10px;">
                    <b>Atmospheric Condition:</b> {dest_weather['condition'].title()}<br>
                    <span style="font-size: 0.76rem; color: #94a3b8;">Station: {dest_weather['city']} • Barometer: {dest_weather['pressure']} hPa • Visibility: {dest_weather['visibility']:.1f} km</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Atmospheric weather telemetry offline.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Predictive Disruption HUD Card
        st.markdown(
            """
            <div class="hud-glass-card">
                <div class="hud-panel-title">
                    <span>🔮</span> Corridor Risk Review
                </div>
            """,
            unsafe_allow_html=True
        )

        risk_color = "#10b981" if risk_level == "Low" else ("#f59e0b" if risk_level == "Moderate" else "#ff4d6d")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(0,0,0,0.3); border: 1px solid {risk_color}; padding: 10px 14px; border-radius: 8px; margin-bottom: 12px;">
                <span style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; font-weight: 700; text-transform: uppercase;">Disruption Vulnerability</span>
                <span style="font-family: 'Orbitron', monospace; font-size: 1.1rem; font-weight: 800; color: {risk_color};">{risk_level.upper()} RISK</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        p1, p2 = st.columns(2)
        with p1:
            st.metric("🌧️ Rain Probability", f"{max_prob}%")
        with p2:
            st.metric("🌧️ Max Precipitation", f"{max_precip:.1f} mm")

        for alert in pred_alerts:
            st.markdown(f"<div style='font-size: 0.85rem; color: #cbd5e1; margin-top: 6px;'>{alert}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 — LIVE FLEET GPS TRACKING TELEMETRY
# =========================================================

with tab_fleet:
    st.markdown(
        f"""
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>🚛</span> {txt["fleet"]}
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0 0 16px 0;">
                High-frequency real-time telemetry tracking of essential supply carriers navigating North Eastern transit corridors.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    simulated_lat = start_lat + (end_lat - start_lat) * 0.45
    simulated_lon = start_lon + (end_lon - start_lon) * 0.45

    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("Transponder ID", "TRK-NER-9082")
    col_f2.metric("Telemetry Velocity", "38 km/h")
    col_f3.metric("Transponder Status", "🟢 100% Encrypted Signal")

    st.write("")

    f_map = folium.Map(
        location=[simulated_lat, simulated_lon],
        zoom_start=9,
        tiles="CartoDB dark_matter"
    )

    folium.Marker(
        location=[simulated_lat, simulated_lon],
        popup=f"TRK-NER-9082 ({cargo_type})",
        tooltip="TRK-NER-9082 (Active Transponder)",
        icon=folium.Icon(color="orange", icon="truck", prefix="fa")
    ).add_to(f_map)

    st_folium(f_map, width="100%", height=380, key="fleet_tracking_map")

# =========================================================
# TAB 3 — GEO-TAGGED FIELD INCIDENT DISPATCH TERMINAL
# =========================================================

with tab_report:
    st.markdown(
        """
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>📸</span> Incident Field Dispatch & Geo-Surveillance Terminal
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0;">
                Upload real-time geo-tagged photographic evidence and incident telemetry from field personnel to update regional corridor intelligence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    rep_col1, rep_col2 = st.columns(2)

    with rep_col1:
        incident_type = st.selectbox(
            "Incident Classification",
            [
                "Landslide / Mudslide",
                "Flash Flood / Waterlogging",
                "Bridge Damage",
                "Heavy Traffic Congestion"
            ],
            key="incident_type_select"
        )
        incident_category = st.selectbox(
            "Update Category",
            ["Road condition", "Farmer support", "Survey / inspection", "Emergency response"],
            key="incident_category_select",
        )
        report_state = st.selectbox(
            "State",
            ["Assam", "Arunachal Pradesh", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tripura", "Uttar Pradesh"],
            key="report_state_select",
        )
        report_district = st.selectbox(
            "District / Hub",
            list(CITY_COORDS.keys()),
            key="report_district_select",
        )

        st.markdown(
            """
            <div style="font-size: 0.85rem; color: #38bdf8; font-family: 'JetBrains Mono', monospace; margin: 8px 0 4px 0;">
                📍 TARGET ACQUISITION: Click anywhere on the map to pinpoint coordinates
            </div>
            """,
            unsafe_allow_html=True
        )

        report_map = folium.Map(
            location=[start_lat, start_lon],
            zoom_start=7,
            tiles="CartoDB dark_matter"
        )

        if "report_lat" in st.session_state:
            folium.Marker(
                [st.session_state.report_lat, st.session_state.report_lon],
                tooltip="Selected Incident Target",
                popup=f"Lat: {st.session_state.report_lat:.6f}<br>Lon: {st.session_state.report_lon:.6f}",
                icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")
            ).add_to(report_map)

        map_data = st_folium(
            report_map,
            width="100%",
            height=340,
            key="incident_report_map",
            returned_objects=["last_clicked"]
        )

        if map_data and map_data.get("last_clicked"):
            st.session_state.report_lat = map_data["last_clicked"]["lat"]
            st.session_state.report_lon = map_data["last_clicked"]["lng"]

        inc_lat = st.session_state.get("report_lat", start_lat)
        inc_lon = st.session_state.get("report_lon", start_lon)

        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 8px; padding: 10px 14px; margin: 10px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">
                <span style="color: #00f2fe;">TARGET GPS LOCK:</span>
                <span style="color: #ffffff; margin-left: 10px;">LAT: <b>{inc_lat:.6f}</b></span>
                <span style="color: #ffffff; margin-left: 10px;">LON: <b>{inc_lon:.6f}</b></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        notes = st.text_area(
            "Tactical Situation Report / Ground Observations",
            placeholder="Document road accessibility, blockage severity, estimated clearance timeframe, and ground conditions...",
            key="incident_notes",
            height=110
        )

    with rep_col2:
        st.markdown(
            """
            <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 6px;">
                📷 Optical Surveillance & Photo Evidence
            </div>
            """,
            unsafe_allow_html=True
        )

        img_file = st.file_uploader(
            "Transference Dropzone (Photo Upload)",
            type=["jpg", "jpeg", "png"],
            key="incident_image_upload"
        )
        document_file = st.file_uploader(
            "Supporting document (optional)",
            type=["pdf", "doc", "docx"],
            key="incident_document_upload",
        )

        st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem; font-weight: bold;'>— OR LIVE OPTICAL RECONNAISSANCE —</div>", unsafe_allow_html=True)

        cam_file = None
        if not st.session_state.get("camera_attempted", False):
            if st.button("Open camera", key="open_incident_camera"):
                st.session_state.camera_attempted = True
                st.rerun()
        elif not st.session_state.get("camera_finished", False):
            cam_file = st.camera_input(
                "Activate Optical Camera Sensor",
                key="incident_camera"
            )
            if cam_file is None:
                st.session_state.camera_finished = True
                st.info("Camera was not used. You can continue with an uploaded image.")
        else:
            st.caption("Camera permission was declined or the camera was closed. Upload an image instead.")

        if img_file:
            st.markdown("<b>Captured Surveillance Evidence:</b>", unsafe_allow_html=True)
            st.image(img_file, caption="Uploaded Field Evidence", width=340)
        elif cam_file:
            st.markdown("<b>Live Camera Optical Frame:</b>", unsafe_allow_html=True)
            st.image(cam_file, caption="Live Reconnaissance Capture", width=340)

    st.write("")

    # SUBMIT REPORT BUTTON (PRESERVED BACKEND)
    if st.button("📤 TRANSMIT FIELD INTELLIGENCE DOSSIER", type="primary", key="submit_incident_report"):
        selected_image = img_file if img_file is not None else cam_file

        if selected_image is None:
            st.warning("⚠️ Please provide photographic evidence (upload or capture).")
        elif not notes.strip():
            st.warning("⚠️ Please enter tactical situation report details.")
        else:
            report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                report_id, saved_image_path = save_field_report(
                    incident_type,
                    notes,
                    inc_lat,
                    inc_lon,
                    report_time,
                    selected_image,
                    submitted_by=st.session_state.role or "field-official",
                    category=incident_category,
                    state=report_state,
                    district=report_district,
                    document_file=document_file,
                )

                st.session_state.last_seen_report_id = report_id
                st.session_state.new_report_alert = {
                    "id": report_id,
                    "type": incident_type,
                    "description": notes,
                    "lat": inc_lat,
                    "lon": inc_lon,
                    "time": report_time
                }

                st.success(f"✅ Field Intelligence Dossier #{report_id} transmitted and indexed!")
            except Exception as e:
                st.error(f"❌ Intelligence transmission failed: {e}")

    # SUBMITTED FIELD REPORTS ARCHIVE
    st.write("")
    st.markdown(
        """
        <div class="hud-panel-title" style="margin-top: 20px;">
            <span>🗄️</span> Declassified Field Incident Archives
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, incident_type, description, latitude, longitude, report_time, image_path,
                   category, status
            FROM field_reports
            WHERE status = 'Approved'
            ORDER BY id DESC
        """)
        reports = cursor.fetchall()
        conn.close()

        if reports:
            for rep in reports:
                r_id, r_type, r_desc, r_lat, r_lon, r_time, r_img, r_category, r_status = rep
                with st.expander(f"📋 DOSSIER #{r_id} • {r_type} • {r_time}"):
                    dc1, dc2 = st.columns([1, 1])
                    with dc1:
                        st.markdown(
                            f"""
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1; line-height: 1.8;">
                                📍 <b>LATITUDE:</b> {r_lat:.6f}<br>
                                📍 <b>LONGITUDE:</b> {r_lon:.6f}<br>
                                🕒 <b>LOGGED TIME:</b> {r_time}<br>
                                ⚠️ <b>CLASSIFICATION:</b> <span style="color: #f59e0b;">{r_type}</span><br>
                                🗂️ <b>CATEGORY:</b> {r_category}<br>
                                ✅ <b>PUBLIC STATUS:</b> {r_status}<br>
                                📝 <b>SUMMARY:</b> {r_desc}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with dc2:
                        if r_img and os.path.exists(r_img):
                            st.image(r_img, caption=f"Optical Evidence #{r_id}", width=340)
                        else:
                            st.caption("No optical image record attached.")
        else:
            st.info("No field reports currently logged in the intelligence database.")
    except Exception as e:
        st.error(f"❌ Archive query error: {e}")

# =========================================================
# TAB 4 — DISTRICT READINESS MATRIX
# =========================================================

with tab_district:
    st.markdown(
        """
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>📊</span> Regional Corridor Readiness & Bottleneck Matrix
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0 0 16px 0;">
                Comprehensive strategic accessibility status across key North Eastern logistics hubs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    accessibility_data = [
        {
            "District Hub": "Guwahati",
            "Readiness Status": "🟢 Fully Accessible",
            "Active Vulnerabilities / Bottlenecks": "None Detected",
            "Strategic Evacuation Route": "NH-27"
        },
        {
            "District Hub": "Shillong",
            "Readiness Status": "🟡 Partially Disrupted",
            "Active Vulnerabilities / Bottlenecks": "Landslide on NH-6 (Km 42)",
            "Strategic Evacuation Route": "SH-1 Alternative Pass"
        },
        {
            "District Hub": "Imphal",
            "Readiness Status": "🔴 Severely Restricted",
            "Active Vulnerabilities / Bottlenecks": "Bridge Structural Degradation near Jiribam",
            "Strategic Evacuation Route": "NH-37 (Armed Escort Bypass)"
        },
        {
            "District Hub": "Agartala",
            "Readiness Status": "🟢 Fully Accessible",
            "Active Vulnerabilities / Bottlenecks": "None Detected",
            "Strategic Evacuation Route": "NH-8"
        },
        {
            "District Hub": "Aizawl",
            "Readiness Status": "🟡 Partially Disrupted",
            "Active Vulnerabilities / Bottlenecks": "Heavy Mountain Fog & Low-Lying Waterlogging",
            "Strategic Evacuation Route": "NH-54 Hill Route"
        }
    ]

    st.table(pd.DataFrame(accessibility_data))

# =========================================================
# TAB 5 — ROUTE RISK REVIEW
# =========================================================

with tab_ai:
    st.markdown(
        """
        <div class="hud-glass-card">
            <div class="hud-panel-title">
                <span>📈</span> Route Risk Review
            </div>
            <p style="color: #94a3b8; font-size: 0.92rem; margin: 0 0 16px 0;">
                Scenario review for rainfall, slope, and soil conditions affecting route safety and delivery continuity.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    ai_c1, ai_c2 = st.columns(2)

    with ai_c1:
        ml_rain = st.slider(
            "🌧️ Simulated Rainfall (mm/24h)",
            0.0, 350.0, 150.0,
            key="ml_rain_slider"
        )
        ml_moisture = st.slider(
            "💧 Soil Moisture Saturation (%)",
            10.0, 100.0, 75.0,
            key="ml_soil_slider"
        )

    with ai_c2:
        ml_slope = st.slider(
            "⛰️ Corridor Slope Incline (Degrees)",
            0.0, 70.0, 35.0,
            key="ml_slope_slider"
        )
        ml_freq = st.number_input(
            "🪨 Historical Landslide Frequency",
            min_value=0, max_value=10, value=1,
            key="ml_freq_slider"
        )

    ml_input_df = pd.DataFrame(
        [[ml_rain, ml_moisture, ml_slope, ml_freq]],
        columns=[
            "rainfall_mm",
            "soil_moisture",
            "slope_degrees",
            "historical_landslide_freq"
        ]
    )

    ml_pred = ml_risk_model.predict(ml_input_df)[0]
    ml_prob = ml_risk_model.predict_proba(ml_input_df)[0][1] * 100

    risk_accent = "#ff3366" if ml_pred == 1 else "#10b981"
    risk_title = "CRITICAL DISRUPTION RISK" if ml_pred == 1 else "ROUTE STABLE"
    risk_desc = "Current conditions indicate a high likelihood of slope instability or waterlogging." if ml_pred == 1 else "Current corridor indicators remain within a manageable operational range."

    st.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid {risk_accent}; border-radius: 12px; padding: 20px; margin-top: 14px; box-shadow: 0 0 20px {risk_accent}33;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.25rem; font-weight: 800; color: {risk_accent};">
                    {risk_title}
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.45rem; font-weight: 800; color: #ffffff;">
                    {ml_prob:.1f}% PROBABILITY
                </div>
            </div>
            <div style="width: 100%; height: 10px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; overflow: hidden; margin-bottom: 12px;">
                <div style="width: {ml_prob}%; height: 100%; background: linear-gradient(90deg, #10b981, #f59e0b, #ff3366); transition: width 0.5s ease;"></div>
            </div>
            <div style="font-size: 0.9rem; color: #94a3b8;">
                {risk_desc}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# ADMIN OPERATIONS CONSOLE
# =========================================================

if tab_admin is not None:
    with tab_admin:
        st.markdown(
            """
            <div class="hud-glass-card">
                <div class="hud-panel-title"><span>🛡️</span> Regional Review & Publishing Desk</div>
                <p style="color: #94a3b8; font-size: .92rem; margin: 0;">Review incoming field intelligence, correct records, and publish verified updates to the public portal.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        admin_status = st.selectbox("Filter by review status", ["All", "Pending", "Approved", "Rejected"], key="admin_status_filter")
        admin_search = st.text_input("Search location, category, description, or submitter", key="admin_report_search")
        admin_state = st.selectbox("Filter by state", ["All", "Assam", "Arunachal Pradesh", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tripura", "Uttar Pradesh"], key="admin_state_filter")
        admin_district = st.selectbox("Filter by district / hub", ["All"] + list(CITY_COORDS.keys()), key="admin_district_filter")
        admin_category = st.selectbox("Filter by category", ["All", "Road condition", "Farmer support", "Survey / inspection", "Emergency response"], key="admin_category_filter")
        admin_rows = fetch_field_reports(admin_status, admin_search, admin_state, admin_district, admin_category)
        admin_metric1, admin_metric2, admin_metric3 = st.columns(3)
        admin_metric1.metric("Records in view", len(admin_rows))
        admin_metric2.metric("Pending review", len(fetch_field_reports("Pending")))
        admin_metric3.metric("Published updates", len(fetch_field_reports("Approved")))

        with st.expander("Publish a portal announcement"):
            announcement_label = st.selectbox(
                "Announcement type",
                ["Latest Update", "Important Notice", "Emergency Notice", "Service Update"],
                key="admin_announcement_label",
            )
            announcement_title = st.text_input("Announcement title", key="admin_announcement_title")
            announcement_body = st.text_area("Announcement details", key="admin_announcement_body")
            if st.button("Publish announcement", key="publish_announcement", type="primary"):
                if announcement_title.strip() and announcement_body.strip():
                    publish_announcement(announcement_label, announcement_title, announcement_body)
                    st.success("Announcement published to the portal.")
                    st.rerun()
                else:
                    st.warning("Enter both a title and announcement detail before publishing.")

        if not admin_rows:
            st.info("No field submissions match the current filters.")
        for admin_row in admin_rows:
            (
                admin_id, admin_type, admin_description, admin_lat, admin_lon,
                admin_time, admin_image, admin_submitter, admin_category,
                admin_state, admin_district, admin_document, admin_row_status,
            ) = admin_row
            with st.expander(f"#{admin_id} · {admin_type} · {admin_row_status} · {admin_time}"):
                st.caption(f"Submitted by {admin_submitter} · {admin_state} · {admin_district} · {admin_category} · {admin_lat:.5f}, {admin_lon:.5f}")
                edited_description = st.text_area("Description", admin_description, key=f"edit_description_{admin_id}")
                if admin_image and os.path.exists(admin_image):
                    st.image(admin_image, width=300)
                if admin_document and os.path.exists(admin_document):
                    with open(admin_document, "rb") as document_handle:
                        st.download_button(
                            "Download supporting document",
                            document_handle.read(),
                            file_name=os.path.basename(admin_document),
                            key=f"download_document_{admin_id}",
                        )
                action_col1, action_col2, action_col3 = st.columns(3)
                with action_col1:
                    if st.button("Approve / publish", key=f"approve_{admin_id}", type="primary"):
                        update_report_status(admin_id, "Approved", "admin")
                        st.rerun()
                with action_col2:
                    if st.button("Reject", key=f"reject_{admin_id}"):
                        update_report_status(admin_id, "Rejected", "admin")
                        st.rerun()
                with action_col3:
                    if st.button("Save / remove", key=f"save_{admin_id}"):
                        update_report_description(admin_id, edited_description.strip())
                        st.success("Record updated.")
                    if st.button("Delete record", key=f"delete_{admin_id}"):
                        delete_report(admin_id)
                        st.rerun()

# =========================================================
# AI ROUTE OPTIMIZATION ENGINE SUMMARY CARD
# =========================================================

st.write("")
st.markdown(
    """
    <div class="hud-panel-title" style="margin-top: 24px;">
        <span>�</span> Route Advisory
    </div>
    """,
    unsafe_allow_html=True
)

if routes:
    prim = routes[0]
    delay_mult = 1.45 if risk_level == "High" else (1.20 if risk_level == "Moderate" else 1.0)
    adjusted_duration = prim['duration_min'] * delay_mult

    sum_col1, sum_col2 = st.columns([2, 1])

    with sum_col1:
        st.markdown(
            f"""
            <div class="hud-glass-card">
                <div style="font-family: 'Inter', sans-serif; font-size: 1.02rem; font-weight: 700; color: #486c8a; margin-bottom: 10px;">
                    Strategic Corridor: {source} ➔ {destination}
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; font-family: 'Inter', sans-serif; font-size: 0.88rem;">
                    <div>📏 <b>DISTANCE:</b> <span style="color: #1f2a2a;">{prim['distance_km']:.2f} km</span></div>
                    <div>⏱️ <b>EST. TRANSIT:</b> <span style="color: #1f2a2a;">{prim['duration_min']:.0f} mins</span></div>
                    <div>⚠️ <b>RISK MULTIPLIER:</b> <span style="color: #b88438;">{delay_mult:.2f}x</span></div>
                    <div>🕒 <b>ADJUSTED ETA:</b> <span style="color: #3f8f7d;">{adjusted_duration:.0f} mins</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with sum_col2:
        if enable_rerouting and rerouted_route:
            st.markdown(
                f"""
                <div class="hud-glass-card" style="border-color: #f59e0b;">
                    <div style="font-family: 'Inter', sans-serif; font-size: 0.95rem; font-weight: 700; color: #b88438; margin-bottom: 8px;">
                        Dynamic Reroute (via {reroute_city})
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1;">
                        📏 <b>Detour Dist:</b> {rerouted_route['distance_km']:.2f} km<br>
                        ⏱️ <b>Detour Time:</b> {rerouted_route['duration_min']:.0f} mins
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif len(routes) > 1:
            alt = routes[1]
            st.markdown(
                f"""
                <div class="hud-glass-card" style="border-color: #10b981;">
                    <div style="font-family: 'Inter', sans-serif; font-size: 0.95rem; font-weight: 700; color: #3f8f7d; margin-bottom: 8px;">
                        Alternate Route Available
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1;">
                        📏 <b>Alt Dist:</b> {alt['distance_km']:.2f} km<br>
                        ⏱️ <b>Alt Time:</b> ~{alt['duration_min']:.0f} mins
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Single strategic route available for selected district pair.")
else:
    st.error("No valid corridor found between selected districts.")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <footer class="official-footer">
        <div class="official-footer-grid">
            <section>
                <h3>NER Logistics Intelligence</h3>
                <p>Official regional operations platform for safer, more accessible logistics across the North Eastern Region.</p>
                <p>Government of India<br>Ministry of Development of North Eastern Region</p>
            </section>
            <section>
                <h3>Important Links</h3>
                <ul><li>Department portal</li><li>Regional transport advisories</li><li>Citizen services</li><li>Open data catalogue</li></ul>
            </section>
            <section>
                <h3>Support</h3>
                <ul><li>Help and accessibility</li><li>Privacy policy</li><li>Terms and conditions</li><li>Sitemap</li></ul>
            </section>
            <section>
                <h3>Contact</h3>
                <p>Regional Operations Helpdesk<br>support@ner-logistics.gov.in<br>Mon-Fri, 09:00-18:00 IST</p>
                <p>Follow official updates: @NERLogistics</p>
            </section>
        </div>
        <div class="footer-bottom"><span>© 2026 Government of India. All rights reserved.</span><span>SIH Problem Statement 26002 · Last portal sync: live</span></div>
    </footer>
    """,
    unsafe_allow_html=True
)