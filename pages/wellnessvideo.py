import streamlit as st
import random
import sys
import os

# --- 1. IMPORT FIX ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tab 

# --- 2. PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Acad&Me - Wellness")

# --- 3. INJECT LAYOUT ---
tab.render_css()
tab.render_top_buttons()
tab.render_navbar()

# --- 4. VIDEO PAGE CONTENT ---
vids = [
    "https://www.youtube.com/watch?v=tybOi4hjZFQ",      
    "https://www.youtube.com/watch?v=WPPPFqsECz0",      
    "https://www.youtube.com/watch?v=h2aWYjSA1Jc",      
    "https://www.youtube.com/watch?v=oBu-pQG6sTY",      
    "https://www.youtube.com/watch?v=TXU591OYOHA",      
    "https://www.youtube.com/watch?v=mWdb6qg2IOc",      
    "https://www.youtube.com/watch?v=poZBpvLTHNw",      
    "https://www.youtube.com/watch?v=6p_yaNFSYao",      
    "https://www.youtube.com/watch?v=goqqLfrXzhI",      
    "https://www.youtube.com/watch?v=nJzWpHLGWlY",      
    "https://www.youtube.com/watch?v=WfPqlTRFnLU"       
]

if 'last_video' not in st.session_state:
    st.session_state.last_video = vids[0]

# Add spacing
st.write("")
st.write("")

col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    # --- CSS INJECTION ---
    st.markdown("""
        <style>
        .quote-box {
            background-color: white;
            border: 1px solid black;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
            padding: 15px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 20px;
            font-weight: 700;
            color: black;
            max-width: 600px;
            margin: 0 auto 20px auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- UPDATED BANNER ---
    # Replaced the previous text with "Wellness Corner" and applied the .quote-box class
    st.markdown('<div class="quote-box">Wellness Corner 🌿</div>', unsafe_allow_html=True)
    
    # Video Player
    st.video(st.session_state.last_video)
    
    st.write("")
    
    # Center the button
    b1, b2, b3 = st.columns([1, 1, 1])
    with b2:
        if st.button("Play", use_container_width=True):
            randvid = random.choice(vids)
            # Try not to repeat the same video
            while len(vids) > 1 and randvid == st.session_state.last_video:
                randvid = random.choice(vids)
            st.session_state.last_video = randvid
            st.rerun()