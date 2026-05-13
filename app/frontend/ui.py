import streamlit as st
import requests
import time
from datetime import datetime

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Multi AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background Animation */
.stApp {
    background: linear-gradient(-45deg, #0f172a, #111827, #1e1b4b, #312e81);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    color: white;
}

/* Animated Gradient */
@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Main Container */
.main-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(14px);
    padding: 2rem;
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 8px 32px rgba(0,0,0,0.35);
    animation: fadeIn 1s ease;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(90deg,#60a5fa,#a78bfa,#f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* Input Box */
.stTextArea textarea {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    padding: 16px !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    color: white;
    border: none;
    padding: 0.9rem;
    border-radius: 16px;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s ease;
    box-shadow: 0px 5px 20px rgba(99,102,241,0.45);
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0px 10px 28px rgba(139,92,246,0.75);
}

/* Chat Bubble */
.user-msg {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    padding: 16px;
    border-radius: 20px 20px 5px 20px;
    margin: 10px 0;
    color: white;
    animation: fadeIn 0.5s ease;
}

.bot-msg {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 20px 20px 20px 5px;
    margin: 10px 0;
    color: white;
    animation: fadeIn 0.8s ease;
}

/* Glass Cards */
.glass {
    background: rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 18px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Fade Animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* Floating animation */
.float {
    animation: floating 3s ease-in-out infinite;
}

@keyframes floating {
    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-8px);
    }
    100% {
        transform: translateY(0px);
    }
}

/* Hide Streamlit Menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:

    st.markdown("## 🤖 AI Control Panel")

    st.markdown("---")

    selected_model = st.selectbox(
        "⚡ Choose Model",
        settings.ALLOWED_MODEL_NAMES
    )

    allow_web_search = st.toggle("🌐 Enable Web Search")

    uploaded_file = st.file_uploader(
        "📄 Upload File",
        type=["pdf", "txt", "docx"]
    )

    st.markdown("---")

    st.markdown("### 📊 AI Stats")

    st.metric("Models Available", len(settings.ALLOWED_MODEL_NAMES))
    st.metric("Status", "Online ✅")

    current_time = datetime.now().strftime("%H:%M:%S")
    st.metric("Server Time", current_time)

# ================= HEADER =================
st.markdown("""
<div class="main-card float">
    <h1 class="main-title">🤖 Multi AI Agent</h1>
    <p class="subtitle">
        Next Generation AI Assistant powered by Groq + Tavily + Streamlit
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ================= INPUTS =================
col1, col2 = st.columns([1, 1])

with col1:

    system_prompt = st.text_area(
        "🧠 System Prompt",
        placeholder="You are an advanced AI assistant...",
        height=160
    )

with col2:

    user_query = st.text_area(
        "💬 Ask Anything",
        placeholder="Explain AI, write code, summarize text...",
        height=160
    )

# ================= API =================
API_URL = "http://127.0.0.1:9999/chat"

# ================= CHAT HISTORY =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================= BUTTON =================
if st.button("🚀 Generate Response"):

    if not user_query.strip():
        st.warning("⚠ Please enter a query")
        st.stop()

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    try:

        logger.info("Sending request to backend")

        # User Message
        st.markdown(f"""
        <div class="user-msg">
            <b>🧑 You:</b><br><br>
            {user_query}
        </div>
        """, unsafe_allow_html=True)

        # Typing animation
        with st.spinner("🤖 AI is thinking deeply..."):

            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            response = requests.post(API_URL, json=payload)

            progress.empty()

        if response.status_code == 200:

            agent_response = response.json().get("response", "")

            logger.info("Successfully received response")

            # Save chat history
            st.session_state.chat_history.append(
                {
                    "query": user_query,
                    "response": agent_response
                }
            )

            # Bot Message
            st.markdown(f"""
            <div class="bot-msg">
                <b>🤖 AI Agent:</b><br><br>
                {agent_response}
            </div>
            """, unsafe_allow_html=True)

            st.success("✨ Response Generated Successfully")

        else:

            logger.error("Backend Error")
            st.error("❌ Backend server error")

    except Exception as e:

        logger.error("Communication Error")

        st.error(
            str(CustomException("Failed to communicate with backend"))
        )

# ================= CHAT HISTORY =================
if st.session_state.chat_history:

    st.write("")
    st.markdown("## 🕘 Conversation History")

    for idx, item in enumerate(reversed(st.session_state.chat_history)):

        with st.expander(f"Conversation {idx + 1}"):

            st.markdown(f"""
            <div class="glass">
                <b>🧑 Query:</b><br><br>
                {item["query"]}<br><br>

                <b>🤖 Response:</b><br><br>
                {item["response"]}
            </div>
            """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<style>

.custom-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(15,23,42,0.85);
    backdrop-filter: blur(10px);
    text-align: center;
    padding: 12px;
    color: white;
    font-size: 15px;
    border-top: 1px solid rgba(255,255,255,0.08);
    z-index: 999;
}

</style>

<div class="custom-footer">
    🚀 Developed by <b>Deepak Yadav</b> 💙
</div>

""", unsafe_allow_html=True)