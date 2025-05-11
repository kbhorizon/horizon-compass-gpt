
import streamlit as st
import openai
import os

st.set_page_config(page_title="Horizon GPT", layout="wide")

# Sidebar
st.sidebar.title("Horizon GPT Research Assistant")
st.sidebar.markdown("Use this space to explore brand vs performance research and the Horizon Compass tool.")

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.warning("API key not found. Please add it to Hugging Face secrets.")
    st.stop()

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Research Input")
    research_text = st.text_area("Paste relevant research here:", height=300)

    st.header("Ask a Question")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are Horizon GPT, a strategic research assistant for media planning."}
        ]

    user_input = st.text_input("Your question:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages + [{"role": "user", "content": research_text}]
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.messages[1:]:
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

with col2:
    st.header("Compass Tool")
    st.components.v1.iframe("https://huggingface.co/spaces/Kbhorizon/BATool", height=600, scrolling=True)
