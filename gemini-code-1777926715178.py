import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ==========================================
# 1. THEME & CONFIGURATION
# ==========================================
THEME_CONFIG = {
    # 💡 REPLACE THIS URL with your Pinterest image link
    "BG_IMAGE_URL": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2528&auto=format&fit=crop", 
    "FONT_HEADER": "'Playfair Display', serif",
    "FONT_BODY": "'Inter', sans-serif",
}

DATA_FILE = "tasks.json"
st.set_page_config(page_title="Aura-Schedule", layout="centered", initial_sidebar_state="collapsed")

# ==========================================
# 2. REFINED PREMIUM CSS
# ==========================================
def set_custom_styles():
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

        /* Background & Global */
        .stApp {{
            background-color: #0F0F13;
        }}
        
        [data-testid="stHeader"], [data-testid="stToolbar"] {{
            display: none;
        }}

        /* Typography - Making it "Designy" */
        .aura-greeting {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 3.5rem; /* Much larger, like Savee.jpg */
            font-weight: 700;
            margin-bottom: -10px;
            color: #FFFFFF;
            line-height: 1;
        }}
        
        .aura-date {{
            font-family: {THEME_CONFIG['FONT_BODY']};
            font-size: 1rem;
            font-weight: 400;
            color: #666666;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 40px;
        }}

        /* Date Strip Fix */
        .date-strip {{
            display: flex;
            justify-content: space-between;
            margin: 20px 0 40px 0;
            padding-bottom: 20px;
        }}
        .date-item {{
            text-align: center;
            color: #444444;
        }}
        .date-item.active {{
            color: #FFFFFF;
            border-bottom: 2px solid #FFFFFF;
            padding-bottom: 5px;
        }}
        .date-day {{ font-size: 0.7rem; text-transform: uppercase; font-weight: 600; }}
        .date-num {{ font-size: 1.5rem; font-family: {THEME_CONFIG['FONT_HEADER']}; }}

        /* Card Refinement */
        .task-card {{
            background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{THEME_CONFIG['BG_IMAGE_URL']}');
            background-size: cover;
            background-position: center;
            border-radius: 30px; /* More rounded like the screenshot */
            padding: 30px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        .task-title {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 2rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
        }}
        
        .task-time {{
            font-size: 1rem;
            color: #888888;
            margin-top: 10px;
        }}
        
        .task-phase {{
            font-size: 0.9rem;
            color: #555555;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }}
        
        /* Buttons */
        .stButton>button {{
            background-color: transparent !important;
            border: 1px solid #333 !important;
            color: white !important;
            border-radius: 50% !important;
            width: 40px;
            height: 40px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 3. LOGIC & RENDER
# ==========================================
def handle_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return [{"id": 1, "title": "Deep Work", "time": "09:00 - 11:30", "phase": "Focus Phase"}]

def render_ui():
    set_custom_styles()
    tasks = handle_data()
    now = datetime.now()

    # Header
    st.markdown(f"<div class='aura-greeting'>Hello, Moon</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='aura-date'>{now.strftime('%d %b, %Y')}</div>", unsafe_allow_html=True)

    # Date Strip
    date_html = "<div class='date-strip'>"
    for i in range(-2, 3):
        d = now + timedelta(days=i)
        cls = "date-item active" if i == 0 else "date-item"
        date_html += f"<div class='{cls}'><div class='date-day'>{d.strftime('%a')}</div><div class='date-num'>{d.strftime('%d')}</div></div>"
    date_html += "</div>"
    st.markdown(date_html, unsafe_allow_html=True)

    # Render Cards
    for t in tasks:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            <div class='task-card'>
                <div class='task-title'>• {t['title']}</div>
                <div class='task-time'>⏱ {t['time']}</div>
                <div class='task-phase'>{t['phase']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write(" ") # Spacing
            st.button("✕", key=f"del_{t['id']}")

if __name__ == "__main__":
    render_ui()
