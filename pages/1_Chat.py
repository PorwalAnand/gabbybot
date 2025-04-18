import streamlit as st
from chatbot import get_response
import datetime

# Page config and styling
st.set_page_config(page_title="Chat with Gabby", layout="wide")

st.markdown("""
    <style>
    body, .stApp {
        background-color: #f7f0ec;
        color: #2e2e2e;
    }
    .stChatMessage, .markdown-text-container, .stMarkdown, p {
        color: #2e2e2e !important;
        font-size: 1.05rem;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stTextInput input {
        color: #2e2e2e !important;
        background-color: white !important;
    }
    .stTextInput > div > div > input {
        border: 1px solid #ff4c5b;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: transparent !important;
        color: #2e2e2e !important;
        font-size: 0.85rem;
        border: none !important;
        text-align: left !important;
        padding: 4px 0px;
    }
    .sidebar-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# === State Initialization ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

# === Sidebar Controls ===
with st.sidebar:
    st.markdown("### 🌟 Session Controls")
    if st.button("🧘‍♀️ Start New Chat"):
        if st.session_state.chat_history:
            st.session_state.all_chats[st.session_state.active_chat_id] = st.session_state.chat_history
        st.session_state.chat_history = []
        st.session_state.active_chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.rerun()

    if st.session_state.all_chats:
        st.markdown("### 🗂️ Chat History")
        for chat_id in sorted(st.session_state.all_chats.keys(), reverse=True):
            col1, col2 = st.columns([8, 2])
            with col1:
                if st.button(chat_id, key=f"load_{chat_id}"):
                    st.session_state.chat_history = st.session_state.all_chats[chat_id]
                    st.session_state.active_chat_id = chat_id
                    st.rerun()
            with col2:
                delete_label = "🗑️"
                if st.button(delete_label, key=f"delete_{chat_id}"):
                    del st.session_state.all_chats[chat_id]
                    if chat_id == st.session_state.active_chat_id:
                        st.session_state.chat_history = []
                        st.session_state.active_chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.rerun()

# === Initial Welcome Message ===
if not st.session_state.chat_history:
    welcome_message = """Hey there, beautiful. I’m so glad you’re here.  
Whether you're feeling anxious, stuck, ready to manifest, or just need a loving nudge from the Universe — I’ve got you 💫  

I’m here to be your inner guide, your spiritual coach, your steady breath. Let’s tune into some high-vibe energy, choose love over fear, and create space for miracles ✨  

Ready to begin? You can say something like:  
• “I’m super anxious”  
• “I can’t sleep”  
• “I want to manifest something amazing”  
• “Help me trust the Universe”  

I’ll be right here with some big love and real tools to support you ❤️  
Your presence is your power. Let’s begin."""
    st.session_state.chat_history.append(("assistant", welcome_message))

# === Display Current Chat ===
st.title("💫 Chat with Gabby")

for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)

# === Chat Input + Response ===
prompt = st.chat_input("What’s on your heart today?")

if prompt:
    st.session_state.chat_history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_response(prompt, st.session_state.chat_history)
        st.markdown(response)

    st.session_state.chat_history.append(("assistant", response))
