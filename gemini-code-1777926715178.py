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

        /* Header Fix: No more overlapping */
        .header-container {{
            margin-top: 50px;
            margin-bottom: 50px;
        }}
        .aura-greeting {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 3.5rem;
            color: #FFFFFF;
            margin: 0;
            line-height: 1.1;
        }}
        .aura-date {{
            font-family: {THEME_CONFIG['FONT_BODY']};
            font-size: 0.9rem;
            color: #666;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-top: 10px;
        }}

        /* Date Strip - Clean & Minimal */
        .date-strip {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 60px;
        }}
        .date-item {{ text-align: center; color: #333; transition: 0.3s; }}
        .date-item.active {{ color: #FFF; }}
        .date-day {{ font-size: 0.7rem; text-transform: uppercase; font-weight: 600; margin-bottom: 5px; }}
        .date-num {{ font-size: 1.6rem; font-family: {THEME_CONFIG['FONT_HEADER']}; }}

        /* Savee.jpg Inspired Cards */
        .task-card {{
            background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url('{THEME_CONFIG['BG_IMAGE_URL']}');
            background-size: cover;
            background-position: center;
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.03);
        }}
        .task-title {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 2.2rem;
            color: #FFFFFF;
            margin-bottom: 20px;
        }}
        .time-row {{
            display: flex;
            justify-content: space-between;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 15px;
        }}
        .time-box {{ color: #888; font-size: 0.9rem; }}
        .time-label {{ color: #444; text-transform: uppercase; font-size: 0.65rem; letter-spacing: 1px; }}
        .time-val {{ color: #AAA; font-size: 1.1rem; margin-top: 2px; }}

        /* Custom Delete Button */
        .stButton>button {{
            background-color: rgba(255,255,255,0.05) !important;
            border: none !important;
            color: #444 !important;
            border-radius: 12px !important;
            transition: 0.2s;
        }}
        .stButton>button:hover {{ color: #ff4b4b !important; background-color: rgba(255,0,0,0.1) !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 3. LOGIC & DATA
# ==========================================
def handle_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return [{"id": 1, "title": "Deep Work", "start": "09:00", "end": "11:30", "phase": "Focus Phase"}]

def render_ui():
    set_custom_styles()
    if 'tasks' not in st.session_state: st.session_state.tasks = handle_data()
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
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"""
            <div class='task-card'>
                <div class='task-title'>{t['title']}</div>
                <div class='time-row'>
                    <div class='time-box'><div class='time-label'>Start</div><div class='time-val'>{t['start']}</div></div>
                    <div class='time-box' style='text-align:right;'><div class='time-label'>End</div><div class='time-val'>{t['end']}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write(" ") # Spacing
            if st.button("✕", key=f"del_{idx}"):
                st.session_state.tasks.pop(idx)
                with open(DATA_FILE, "w") as f: json.dump(st.session_state.tasks, f)
                st.rerun()

    # --- Add Task (Expander) ---
    with st.expander("+ New Task"):
        with st.form("new_task"):
            title = st.text_input("Task Title")
            s_time = st.time_input("Start")
            e_time = st.time_input("End")
            if st.form_submit_button("Add"):
                st.session_state.tasks.append({"id": len(st.session_state.tasks)+1, "title": title, "start": s_time.strftime('%H:%M'), "end": e_time.strftime('%H:%M'), "phase": ""})
                with open(DATA_FILE, "w") as f: json.dump(st.session_state.tasks, f)
                st.rerun()

if __name__ == "__main__":
    render_ui()
