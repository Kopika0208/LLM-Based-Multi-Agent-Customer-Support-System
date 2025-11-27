import streamlit as st
from agents.orchestrator_agent import OrchestratorAgent

# Initialize orchestrator
orchestrator = OrchestratorAgent()

# --- Page config ---
st.set_page_config(page_title="🟢 Multi-Agent AI Customer Support Bot", layout="wide")

# --- Sidebar: conversation history ---
st.sidebar.title("💬 Conversations")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display past questions in sidebar
for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
    st.sidebar.write(f"{i+1}. {user_msg}")

st.sidebar.button("New chat", on_click=lambda: st.session_state.chat_history.clear())

# --- Main area: feature cards ---
st.title("🟢 Multi-Agent AI Customer Support Bot")
st.write("Ask any question about orders, refunds, or policies.")

# --- Chat area ---
chat_container = st.container()
with chat_container:
    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**AI:** {bot_msg}")
        st.markdown("---")

# --- Chat input ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask anything ...", "")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Get response from orchestrator
    bot_response = orchestrator.handle_query(user_input, "user_1")
    # Add to chat history
    st.session_state.chat_history.append((user_input, bot_response))

