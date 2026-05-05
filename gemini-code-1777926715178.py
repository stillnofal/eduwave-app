import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ==========================================
# 1. THEME & CONFIGURATION (THE "SKIN")
# ==========================================
THEME_CONFIG = {
    # Replace this URL later with your Pinterest image link
    "BG_IMAGE_URL": "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?q=80&w=1000&auto=format&fit=crop", 
    "FONT_HEADER": "'Playfair Display', serif",
    "FONT_BODY": "'Inter', sans-serif",
    "ACCENT_COLOR": "#E5E5E5"
}

DATA_FILE = "tasks.json"

# Set Streamlit page config to look more like an app
st.set_page_config(page_title="Aura-Schedule", layout="centered", initial_sidebar_state="collapsed")

# ==========================================
# 2. STYLING (THE "BONES")
# ==========================================
def set_custom_styles():
    """Injects custom CSS to override Streamlit's default UI and create a premium mobile feel."""
    
    css = f"""
    <style>
        /* Import premium fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

        /* Global Typography & Background */
        html, body, [class*="css"]  {{
            font-family: {THEME_CONFIG['FONT_BODY']};
            background-color: #0F0F13; /* Deep cinematic black */
            color: #FFFFFF;
        }}

        /* Hide Streamlit elements */
        #MainMenu, header, footer {{visibility: hidden;}}

        /* Header Styling */
        .aura-greeting {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0px;
            color: #FFFFFF;
        }}
        .aura-date {{
            font-size: 1.2rem;
            font-weight: 300;
            color: #A0A0A0;
            margin-bottom: 30px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        /* The Pinterest-Ready Card Container */
        .task-card {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{THEME_CONFIG['BG_IMAGE_URL']}');
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s ease;
        }}
        
        .task-card:hover {{
            transform: scale(1.02);
        }}

        /* Card Internal Typography */
        .task-title {{
            font-family: {THEME_CONFIG['FONT_HEADER']};
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0 0 8px 0;
            color: #FFFFFF;
        }}
        
        .task-time {{
            font-size: 0.9rem;
            color: #CCCCCC;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
        }}
        
        .task-phase {{
            font-size: 0.8rem;
            font-style: italic;
            color: {THEME_CONFIG['ACCENT_COLOR']};
            opacity: 0.8;
        }}

        /* Date Strip Styling */
        .date-strip {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .date-item {{
            text-align: center;
            opacity: 0.5;
        }}
        .date-item.active {{
            opacity: 1;
            font-weight: 600;
            color: {THEME_CONFIG['ACCENT_COLOR']};
        }}
        .date-day {{ font-size: 0.8rem; text-transform: uppercase; }}
        .date-num {{ font-size: 1.4rem; font-family: {THEME_CONFIG['FONT_HEADER']}; }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ==========================================
# 3. FUNCTIONAL LOGIC (STATE MANAGEMENT)
# ==========================================
def handle_data():
    """Loads tasks from the local JSON file or creates a default list."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        # Default starter schedule
        default_tasks = [
            {"id": 1, "title": "Deep Work", "time": "09:00 - 11:30", "phase": "Focus Phase"},
            {"id": 2, "title": "Break", "time": "11:30 - 12:00", "phase": "Recovery"}
        ]
        save_data(default_tasks)
        return default_tasks

def save_data(tasks):
    """Saves the current schedule to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# ==========================================
# 4. UI RENDERING
# ==========================================
def render_ui():
    """Builds the actual frontend components."""
    
    # Init state
    if 'tasks' not in st.session_state:
        st.session_state.tasks = handle_data()

    now = datetime.now()

    # --- HEADER ---
    st.markdown("<p class='aura-greeting'>Hello, Moon 👋</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='aura-date'>{now.strftime('%d %B, %Y')}</p>", unsafe_allow_html=True)

    # --- DYNAMIC DATE STRIP ---
    date_html = "<div class='date-strip'>"
    for i in range(-2, 3):
        target_date = now + timedelta(days=i)
        active_class = "active" if i == 0 else ""
        date_html += f"""
        <div class='date-item {active_class}'>
            <div class='date-day'>{target_date.strftime('%a')}</div>
            <div class='date-num'>{target_date.strftime('%d')}</div>
        </div>
        """
    date_html += "</div>"
    st.markdown(date_html, unsafe_allow_html=True)

    # --- TASK CARDS ---
    if not st.session_state.tasks:
        st.info("Your schedule is empty. Enjoy the silence.")
    else:
        for idx, task in enumerate(st.session_state.tasks):
            # Using columns to put a "delete" button next to the beautiful card
            col1, col2 = st.columns([8, 1])
            with col1:
                card_html = f"""
                <div class='task-card'>
                    <p class='task-title'>• {task['title']}</p>
                    <p class='task-time'>⏱ {task['time']}</p>
                    <p class='task-phase'>{task['phase']}</p>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
            with col2:
                # Add a bit of vertical space so the button aligns nicely
                st.write("") 
                st.write("")
                if st.button("✕", key=f"del_{task['id']}"):
                    st.session_state.tasks.pop(idx)
                    save_data(st.session_state.tasks)
                    st.rerun()

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    # --- ADD TASK FORM ---
    with st.expander("+ Add New Schedule Item"):
        with st.form("add_task_form", clear_on_submit=True):
            new_title = st.text_input("Title (e.g., Python Study)")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                start_time = st.time_input("Start Time")
            with col_t2:
                end_time = st.time_input("End Time")
            new_phase = st.text_input("Phase / Subtext (e.g., Module 3)")
            
            submitted = st.form_submit_button("Save to Schedule")
            
            if submitted and new_title:
                time_str = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                new_id = max([t['id'] for t in st.session_state.tasks], default=0) + 1
                
                new_task = {
                    "id": new_id,
                    "title": new_title,
                    "time": time_str,
                    "phase": new_phase
                }
                st.session_state.tasks.append(new_task)
                save_data(st.session_state.tasks)
                st.rerun()

    # --- BOTTOM NAVIGATION MOCKUP ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    nav_cols = st.columns(4)
    with nav_cols[0]: st.markdown("<div style='text-align:center; opacity:1;'>🏠<br><small>HOME</small></div>", unsafe_allow_html=True)
    with nav_cols[1]: st.markdown("<div style='text-align:center; opacity:0.5;'>📅<br><small>CALENDAR</small></div>", unsafe_allow_html=True)
    with nav_cols[2]: st.markdown("<div style='text-align:center; opacity:0.5;'>⭐<br><small>SAVED</small></div>", unsafe_allow_html=True)
    with nav_cols[3]: st.markdown("<div style='text-align:center; opacity:0.5;'>🔔<br><small>ALERTS</small></div>", unsafe_allow_html=True)

# ==========================================
# 5. EXECUTION
# ==========================================
if __name__ == "__main__":
    set_custom_styles()
    render_ui()
