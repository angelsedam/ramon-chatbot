import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(page_title="Job Chatbot", page_icon="🤖")

st.title("🤖 Ramon Chatbot")

st.session_state.setdefault("past", [])
st.session_state.setdefault("generated", [])


def on_input_change():
    prompt = st.session_state.user_input

    st.session_state.past.append(prompt)

    try:
        res = requests.post(
            "https://dev-job-chatbot-ai-api-771147684746.us-central1.run.app/query",
            json={"prompt": prompt},
            timeout=100
        )
        res.raise_for_status()
        result = res.json()
        bot_response = result.get("answer", "🤖 I did not found an answer.")
    except Exception as e:
        bot_response = f"⚠️ Error: {e}"

    st.session_state.generated.append({'type': 'normal', 'data': bot_response})

def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()


chat_placeholder = st.empty()
with chat_placeholder.container():
    for i in range(len(st.session_state.generated)):
        message(st.session_state.past[i], is_user=True, key=f"{i}_user")
        message(
            st.session_state.generated[i]['data'],
            key=f"{i}",
            allow_html=True
        )
    st.button("🗑️ Clean chat", on_click=on_btn_click)

with st.container():
    st.text_input("Write your questions:", key="user_input", on_change=on_input_change, label_visibility="collapsed")
