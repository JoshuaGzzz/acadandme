import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os
import json  

# --- 1. IMPORT FIX ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import tab
except ImportError:
    st.error("Error: Could not find 'tab.py'. Please check your folder structure.")
    st.stop()

# --- FILE PATH CONFIGURATION ---
JSON_FILE = os.path.join(os.path.dirname(__file__), 'mood_history.json')

# --- DATA HANDLING FUNCTIONS ---
def load_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return [] 
    return []

def save_data(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Mood Tracker", page_icon="😊", layout="wide")

# --- 2. INJECT LAYOUT ---
# This sets the state (Light or Dark) and renders the standard CSS
tab.render_css() 
tab.render_top_buttons()
tab.render_navbar()

# --- 3. CONDITIONAL OVERRIDE (THE FIX) ---
# Only apply the "Force Dark" styles IF the user has actually selected Dark Mode.
if st.session_state["theme"] == "dark":
    st.markdown("""
    <style>
        /* --- 1. REMOVE BG IMAGE FROM PSEUDO-ELEMENT --- */
        .stApp::before {
            background-image: none !important;
            opacity: 0 !important;
        }

        /* --- 2. FORCE DARK BACKGROUND --- */
        .stApp {
            background-image: none !important;
            background-color: #0E1117 !important;
        }
        
        /* --- 3. FORCE TEXT TO WHITE --- */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div, span, li {
            color: #FAFAFA !important;
        }

        /* --- 4. CUSTOM CARD & BUTTON STYLES FOR DARK MODE --- */
        div.stButton > button {
            background: #2C2C2C !important;
            color: white !important;
            padding: 0.6rem 1rem;
            border-radius: 10px;
            border: none;
            transition: 0.2s;
        }
        div.stButton > button:hover {
            background: #444444 !important; 
            color: white !important;
            border: 1px solid white !important;
        }

        .card {
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            backdrop-filter: blur(5px);
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Fix for Chart Text Color */
        g.infolayer g.g-gtitle text {
            fill: white !important;
        }
        g.xtick text, g.ytick text {
            fill: white !important; 
        }
    </style>
    """, unsafe_allow_html=True)

# Note: If the theme is "light", we skip the block above, 
# so the defaults from tab.py (Blue background + Image) will show up naturally.

# --- SESSION STATE ---
if "mood_data" not in st.session_state:
    st.session_state.mood_data = load_data()

# --- 4. PAGE CONTENT ---
c1, c2, c3 = st.columns([1, 6, 1])

with c2:
    # Title
    st.markdown("<h1 style='text-align:center; margin-bottom: 30px;'>😊 Mood Tracker</h1>", unsafe_allow_html=True)

    # Emoji Logic
    def mood_emoji(value):
        if value <= 2: return "😭"
        if value <= 4: return "😔"
        if value <= 6: return "😐"
        if value <= 8: return "🙂"
        return "🤩"

    # Input Card
    # We use a standard div if light, but the CSS above styles .card if dark.
    # To make it look good in Light mode too, we might want inline styles or relying on tab.py's grey-card logic.
    # But for now, this ensures the functionality works.
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### How are you feeling today?")

    mood = st.slider("Rate your mood", 0, 10, 5)

    if st.button("Save Mood"):
        st.session_state.mood_data.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mood": mood
        })
        save_data(st.session_state.mood_data)
        
        st.success(f"Mood saved! {mood_emoji(mood)}", icon="💾")

    st.markdown("</div>", unsafe_allow_html=True)

    # History Section
    st.write("## 📈 Mood History")

    if st.session_state.mood_data:
        df = pd.DataFrame(st.session_state.mood_data)
        
        # Display Chart
        st.line_chart(df["mood"])

        # Display Data Table
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No moods recorded yet. Start by rating your mood!")