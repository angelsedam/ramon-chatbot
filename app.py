import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
    page_title="Dexter a Dexcom Chatbot",
    page_icon="https://cdn.bfldr.com/Y1RQLUHX/at/84wptn4bvv4nzw7gcq53pp/dexcom-logo-green-cmyk.jpg?auto=webp&format=jpg"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #f7fffa;
        font-family: 'Segoe UI', sans-serif;
    }

    .main .block-container {
        max-width: 100%;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    .stTextInput > div > div > input {
        background-color: #333;
        color: #ffffff;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #ccc;
        caret-color: white;
    }

    input[type="text"]:focus {
        outline: 2px solid #00c0ff;
    }

    .stButton > button {
        background-color: #ffffff;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 0.5em 1em;
    }

    .stButton > button:hover {
        background-color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-top: 20px; margin-bottom: 40px;'>
        <img src='https://cdn.bfldr.com/Y1RQLUHX/at/gj44h4rwsx9446wcsrmmsmff/dexcom-logo-green-cmyk.eps?auto=webp&format=png&width=300&height=100' />
        <h1 style='color: #f7fffa;'>Dexter</h1>
        <p style='color:#cccccc; font-size: 0.9em;'>Your AI assistant for Dexcom documentation</p>
    </div>
""", unsafe_allow_html=True)


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
        bot_response = result.get("answer", "I did not find an answer.")
    except Exception as e:
        bot_response = f"⚠️ Error: {e}"

    st.session_state.generated.append({'type': 'normal', 'data': bot_response})
    st.session_state["user_input"] = ""  


chat_placeholder = st.empty()
with chat_placeholder.container():
    for i in range(len(st.session_state.generated)):
        message(st.session_state.past[i], is_user=True, key=f"{i}_user", avatar_style="thumbs")
        message(st.session_state.generated[i]['data'], key=f"{i}", avatar_style="bottts", allow_html=True)


with st.container():
    st.text_input("Write your questions:", key="user_input", on_change=on_input_change, label_visibility="collapsed")
