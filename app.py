
import streamlit as st
import openai
import os

st.set_page_config(page_title="Horizon Compass GPT", layout="wide")

# Sidebar
st.sidebar.title("🧭 Horizon Compass GPT")
st.sidebar.markdown("Explore Horizon’s brand + performance insights and interact with a GPT-based strategy assistant.")

# Load secrets
api_key = os.getenv("OPENAI_API_KEY")
org_id = os.getenv("OPENAI_ORG_ID")
project_id = os.getenv("OPENAI_PROJECT_ID")  # Optional, may not be required depending on account setup

if not api_key or not org_id:
    st.error("Missing OpenAI credentials. Please set OPENAI_API_KEY and OPENAI_ORG_ID in Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client with project-based authentication
client = openai.OpenAI(
    api_key=api_key,
    organization=org_id,
    project=project_id if project_id else None
)

# Load research from file
try:
    with open("research.txt", "r", encoding="utf-8") as f:
        research_text = f.read()
except FileNotFoundError:
    st.error("Could not load research.txt. Please upload it to your GitHub repo.")
    st.stop()

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🤖 Ask Horizon GPT")
    st.caption("This GPT assistant uses Horizon’s proprietary Brand + Performance research to answer your strategic questions.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are Horizon GPT, a strategic research assistant for media planning. Your answers should be based on Horizon Media’s proprietary Brand + Performance research."}
        ]

    user_input = st.text_input("Ask a strategy question:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": f"{user_input}\n\nResearch Context:\n{research_text}"})
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.messages[1:]:
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

with col2:
    st.header("📊 Compass Tool")
    st.write("Click below to explore the Horizon Compass Tool and test allocation inputs.")
    st.markdown(
        f'<a href="https://huggingface.co/spaces/Kbhorizon/BATool" target="_blank">'
        f'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Compass_rose_en.svg/800px-Compass_rose_en.svg.png" width="300"/>'
        f'</a>',
        unsafe_allow_html=True
    )
