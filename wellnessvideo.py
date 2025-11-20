import streamlit as st
import random

st.set_page_config(layout="wide")

vids = [
    "https://www.youtube.com/watch?v=tybOi4hjZFQ",      # Guided Wim Hof Method Breathing
    "https://www.youtube.com/watch?v=WPPPFqsECz0",      # Kurzgesagt - An Antidote to Dissatisfaction (Gratitude)
    "https://www.youtube.com/watch?v=h2aWYjSA1Jc",      # Huberman Lab - Sleep Toolkit
    "https://www.youtube.com/watch?v=oBu-pQG6sTY",      # Yoga With Adriene - Day 1 Ease Into It
    "https://www.youtube.com/watch?v=TXU591OYOHA",      # Yoga With Adriene - 30 Days of Yoga Start Here
    "https://www.youtube.com/watch?v=mWdb6qg2IOc",      # Great Meditation - 10 Minute Morning Meditation
    "https://www.youtube.com/watch?v=poZBpvLTHNw",      # Move With Nicole - 20 Min Feel Good Yoga
    "https://www.youtube.com/watch?v=6p_yaNFSYao",      # The Honest Guys - Mindfulness Meditation
    "https://www.youtube.com/watch?v=goqqLfrXzhI",      # Boho Beautiful - Best 10 Min Guided Meditation
    "https://www.youtube.com/watch?v=nJzWpHLGWlY",      # Dr. Taz MD - Holistic Health Trends
    "https://www.youtube.com/watch?v=WfPqlTRFnLU"       # ZOE Science & Nutrition - What to Eat for Your Health
]

if 'last_video' not in st.session_state:
    st.session_state.last_video = None

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    if st.button("Stay Motivated!", use_container_width=True):
        randvid = random.choice(vids)
        while randvid == st.session_state.last_video:
            randvid = random.choice(vids)
        st.session_state.last_video = randvid      

        if st.session_state.last_video is not None:
            st.video(st.session_state.last_video)