import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ==========================================
# 1. THEME & CONFIGURATION
# ==========================================
THEME_CONFIG = {
    "BG_IMAGE_URL": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2528&auto=format&fit=crop", 
    "FONT_HEADER": "'Playfair Display', serif",
    "FONT_BODY": "'Inter', sans-serif",
}

DATA_FILE = "tasks.json"
st.set_page_config(page_title="Aura-Schedule", layout="centered", initial_sidebar_state="collapsed")

# ==========================================
# 2. THE "CINEMATIC" CSS
# ==========================================
def set_custom_styles():
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:wght@700&display=swap');

        .stApp {{ background-color: #0F0F13; }}
        [data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none; }}

        /* Header Layout */
        .header-container {{ margin-top: 60px; margin-bottom: 40px; text-align: left; }}
        .aura-greeting {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 3.8rem;
            color: #FFFFFF;
            margin: 0;
            letter-spacing: -1px;
        }}
        .aura-date {{
            font-family: {THEME_CONFIG['FONT_BODY']};
            font-size: 0.85rem;
            color: #555;
            letter-spacing: 5px;
            text-transform: uppercase;
            margin-top: 5px;
        }}

        /* Date Strip */
        .date-strip {{ display: flex; justify-content: space-between; margin-bottom: 50px; padding: 0 10px; }}
        .date-item {{ text-align: center; color: #222; }}
        .date-item.active {{ color: #FFF; border-bottom: 1px solid #FFF; padding-bottom: 10px; }}
        .date-day {{ font-size: 0.65rem; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; letter-spacing: 1px; }}
        .date-num {{ font-size: 1.5rem; font-family: {THEME_CONFIG['FONT_HEADER']}; }}

        /* Premium Task Cards */
        .task-card {{
            background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('{THEME_CONFIG['BG_IMAGE_URL']}');
            background-size: cover;
            background-position: center;
            border-radius: 30px;
            padding: 35px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.03);
        }}
        .task-title {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 2.4rem;
            color: #FFFFFF;
            margin-bottom: 25px;
            line-height: 1.2;
        }}
        .time-row {{
            display: flex;
            justify-content: space-between;
            border-top: 1px solid rgba(255,255,255,0.08);
            padding-top: 20px;
        }}
        .time-label {{ color: #444; text-transform: uppercase; font-size: 0.6rem; letter-spacing: 2px; font-weight: 600; }}
        .time-val {{ color: #999; font-size: 1.2rem; margin-top: 4px; font-weight: 300; }}

        /* Delete Button - Floating right */
        .stButton>button {{
            background-color: transparent !important;
            border: 1px solid #222 !important;
            color: #444 !important;
            border-radius: 50% !important;
            width: 35px;
            height: 35px;
            font-size: 0.8rem !important;
        }}
        .stButton>button:hover {{ color: #ff4b4b !important; border-color: #ff4b4b !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 3. SMART DATA HANDLING (PREVENTS KEYERROR)
# ==========================================
def handle_data():
    """Migrates old task formats and loads schedule."""
    tasks = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            tasks = json.load(f)
    
    # Auto-migration logic for old data
    for t in tasks:
        if "start" not in t or "end" not in t:
            raw_time = t.get("time", "00:00 - 00:00")
            parts = raw_time.split(" - ")
            t["start"] = parts[0] if len(parts) > 0 else "00:00"
            t["end"] = parts[1] if len(parts) > 1 else "00:00"
    
    if not tasks:
        tasks = [{"id": 1, "title": "New Beginning", "start": "09:00", "end": "10:00", "phase": "Setup"}]
    
    return tasks

def render_ui():
    set_custom_styles()
    if 'tasks' not in st.session_state:
        st.session_state.tasks = handle_data()
    
    now = datetime.now()

    # --- Header ---
    st.markdown(f"""
    <div class='header-container'>
        <div class='aura-greeting'>Hello, Moon</div>
        <div class='aura-date'>{now.strftime('%d %B %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Date Strip ---
    date_html = "<div class='date-strip'>"
    for i in range(-2, 3):
        d = now + timedelta(days=i)
        cls = "active" if i == 0 else ""
        date_html += f"<div class='date-item {cls}'><div class='date-day'>{d.strftime('%a')}</div><div class='date-num'>{d.strftime('%d')}</div></div>"
    date_html += "</div>"
    st.markdown(date_html, unsafe_allow_html=True)

    # --- Task Cards ---
    for idx, t in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([12, 1])
        with col1:
            st.markdown(f"""
            <div class='task-card'>
                <div class='task-title'>{t['title']}</div>
                <div class='time-row'>
                    <div><div class='time-label'>Start</div><div class='time-val'>{t['start']}</div></div>
                    <div style='text-align:right;'><div class='time-label'>End</div><div class='time-val'>{t['end']}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write(" ") # Spacing
            if st.button("✕", key=f"del_{idx}"):
                st.session_state.tasks.pop(idx)
                with open(DATA_FILE, "w") as f: json.dump(st.session_state.tasks, f)
                st.rerun()

    # --- Form ---
    with st.expander("+ Add Item"):
        with st.form("new_task"):
            title = st.text_input("Task Title")
            s_time = st.time_input("Start", value=datetime.now())
            e_time = st.time_input("End", value=datetime.now())
            if st.form_submit_button("Add Task"):
                st.session_state.tasks.append({
                    "id": len(st.session_state.tasks)+1, 
                    "title": title, 
                    "start": s_time.strftime('%H:%M'), 
                    "end": e_time.strftime('%H:%M')
                })
                with open(DATA_FILE, "w") as f: json.dump(st.session_state.tasks, f)
                st.rerun()

if __name__ == "__main__":
    render_ui()
