import streamlit as st
from streamlit_calendar import calendar
import json, os

#setting page config at mismong calendar
st.set_page_config(page_title="Calendar To-Do", page_icon="📅", layout="wide", initial_sidebar_state="collapsed")

# Spawning json file (when refreshing andiyan pa din ang tasks)
if os.path.exists("events.json"):
    with open("events.json", "r") as f:
        st.session_state["events"] = json.load(f)

st.title("Calendar To-Do Integration ng mga legends")

# 1. Session sate 
if "events" not in st.session_state:
    st.session_state["events"] = []

# 2. Falsing session state to prevent repeated true 
if "show_form" not in st.session_state:
    st.session_state["show_form"] = False
if "show_delete" not in st.session_state:
    st.session_state["show_delete"] = False

# buttons ng mga legends
col1, col2 = st.columns(2)
with col1:
    if st.button("Add a Task ➕"):
        st.session_state["show_form"] = not st.session_state["show_form"]
with col2:
    if st.button("Delete a Task ❌"):
        st.session_state["show_delete"] = not st.session_state["show_delete"]

# Add event 
if st.session_state["show_form"]:
    with st.container(border=True): 
        st.subheader("New Event Details")
        with st.form("date_form"): #using form
            task_name = st.text_input("Enter the task name:")
            user_date = st.date_input("Event Date")
            submitted = st.form_submit_button("Save")

            if submitted and task_name:
                new_event = { #uses dictionary to save it
                    "title": task_name,
                    "start": user_date.strftime("%Y-%m-%d")
                }
                st.session_state["events"].append(new_event) #append to session state
                with open("events.json", "w") as f: #update json file for refreshing page
                    json.dump(st.session_state["events"], f, indent=4)
                st.session_state["show_form"] = False 
                st.rerun()
                st.toast("Event added successfully!", icon="✅")
                
# Delete form
if st.session_state["show_delete"]:
    with st.container(border=True):
        st.subheader("Delete Event")

        with st.form("delete_form"):
            titles = [e["title"] for e in st.session_state["events"]] #dropdown ng events

            if titles:
                selected = st.selectbox("Select event to delete:", titles) #select an event
                delete_submitted = st.form_submit_button("Delete")

                if delete_submitted:
                    st.session_state["events"] = [ #tanggal sa dictionary
                        e for e in st.session_state["events"] if e["title"] != selected
                    ]

                    with open("events.json", "w") as f: #json update ng malupit 
                        json.dump(st.session_state["events"], f, indent=4)


                    st.session_state["show_delete"] = False
                    st.rerun()
                    st.toast("Event deleted successfully!", icon="🗑️")
            else:
                st.info("No events to delete.")

calendar_options = {
    "initialView": "dayGridMonth",
    "selectable": True
}

calendar(
    events=st.session_state["events"],
    options=calendar_options,
    key="my_calender"
)

