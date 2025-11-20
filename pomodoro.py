import streamlit as st
import time

# --- Constants ---
W = 25 * 60
S = 5 * 60
L = 15 * 60
CYCLES = 4

# --- Utility Functions ---

def format_time(s):
    return f"{int(s // 60):02d}:{int(s % 60):02d}"

def get_time(phase):
    if phase == "work":
        return W
    if phase == "short_break":
        return S
    return L


# --- Control Functions ---

def start_pause():
    st.session_state.running = not st.session_state.running
    st.rerun()

def move_next():
    current = st.session_state.phase
    cycles = st.session_state.cycles

    if current == "work":
        cycles += 1
        st.session_state.cycles = cycles
        next_p = "long_break" if cycles % CYCLES == 0 else "short_break"
    else:
        next_p = "work"

    new_time = get_time(next_p)
    st.session_state.phase = next_p
    st.session_state.time_remaining = new_time
    st.session_state.total_duration = new_time
    st.session_state.running = False

    st.rerun()


# --- Main App ---

def pomodoro_app():
    # Initialize state
    if "phase" not in st.session_state:
        st.session_state.phase = "work"
        st.session_state.time_remaining = W
        st.session_state.total_duration = W
        st.session_state.running = False
        st.session_state.cycles = 0

    st.title("📚 Pomodoro Timer")

    # Display text
    p_title = st.session_state.phase.replace("_", " ").title()
    st.subheader(f"{p_title} | Cycle: {st.session_state.cycles}")

    # Timer Display
    timer_ph = st.empty()
    timer_html = f"<h1 style='font-size: 5rem; text-align: center;'>{format_time(st.session_state.time_remaining)}</h1>"
    timer_ph.markdown(timer_html, unsafe_allow_html=True)

    # Progress bar
    progress_value = (st.session_state.total_duration - st.session_state.time_remaining) / st.session_state.total_duration
    st.progress(progress_value)

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        st.button("Pause" if st.session_state.running else "Start", on_click=start_pause, use_container_width=True)
    with col2:
        st.button("Next", on_click=move_next, use_container_width=True)

    # Timer countdown
    if st.session_state.running and st.session_state.time_remaining > 0:
        time.sleep(1)
        st.session_state.time_remaining -= 1
        st.rerun()

    # Auto next-phase
    if st.session_state.running and st.session_state.time_remaining <= 0:
        st.session_state.running = False
        st.toast(f"{p_title} finished!")
        move_next()


if __name__ == "__main__":
    pomodoro_app()
