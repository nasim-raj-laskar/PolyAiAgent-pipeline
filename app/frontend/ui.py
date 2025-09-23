import streamlit as st
import requests
import time
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

# Page config
st.set_page_config(
    page_title="PolyAgent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

logger = get_logger(__name__)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 PolyAgent</h1>
    <p>Multi AI Agent powered by Groq & Tavily Search</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h2 style="color: white; text-align: center;">⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Define Your AI Agent")
    system_prompt = st.text_area(
        "System Prompt",
        placeholder="Enter system prompt (e.g., 'You are a helpful medical assistant')",
        height=100,
        key="system_prompt",
        label_visibility="collapsed"
    )
    
    st.markdown("### 🧠 Select Model")
    selected_model = st.selectbox(
        "Model Selection",
        settings.ALLOWED_MODEL_NAMES,
        key="model_select",
        label_visibility="collapsed"
    )
    
    st.markdown("### 🔍 Web Search")
    allow_web_search = st.checkbox(
        "Enable web search capabilities",
        key="web_search"
    )
    
    # Model info
    st.markdown("---")
    st.markdown("### 📊 Model Info")
    if selected_model == "llama-3.3-70b-versatile":
        st.info("🦙 Llama 3.3 70B - Versatile and powerful")
    elif selected_model == "openai/gpt-oss-120b":
        st.info("🧠 GPT OSS 120B - Large scale reasoning")
    elif selected_model == "openai/gpt-oss-20b":
        st.info("🧠 GPT OSS 20B - Efficient reasoning")
    elif selected_model == "whisper-large-v3":
        st.info("🎤 Whisper Large V3 - Advanced speech recognition")
    elif selected_model == "meta-llama/llama-guard-4-12b":
        st.info("🛡️ Llama Guard 4 12B - Safety and moderation")
    elif selected_model == "whisper-large-v3-turbo":
        st.info("⚡ Whisper Large V3 Turbo - Fast speech recognition")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Enter Your Query")
    user_query = st.text_area(
        "User Query",
        placeholder="Ask me anything...",
        height=150,
        key="user_query",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 🚀 Actions")
    st.markdown("<br>", unsafe_allow_html=True)
    
    ask_button = st.button("✨ Ask Agent", key="ask_button")

# Handle response outside columns for full width
if ask_button:
    if user_query.strip() and system_prompt.strip():
        # Loading animation
        with st.spinner("🤔 Agent is thinking..."):
            API_URL = "http://127.0.0.1:8000/chat"
            
            payload = {
                "model_name": selected_model,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }
            
            try:
                logger.info("Sending request to backend")
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    agent_response = response.json().get("response", "")
                    logger.info("Received response from backend")
                    
                    # Success animation
                    st.success(" Response generated successfully!")
                    
                    # Full width response
                    st.markdown("### Agent Response:")
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                        padding: 2rem;
                        border-radius: 15px;
                        margin-top: 1rem;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                        width: 100%;
                    ">
                        <div style="
                            background: #ffffff;
                            padding: 2rem;
                            border-radius: 10px;
                            line-height: 1.8;
                            color: #333333;
                            font-size: 16px;
                            min-height: 200px;
                            border: 1px solid #e0e0e0;
                        ">
                            {agent_response.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    logger.error(f"Error in response from backend: {response.status_code}")
                    st.error("❌ Failed to get response from backend")
                    
            except Exception as e:
                logger.error(f"Error in sending request to backend: {e}")
                st.error(f"❌ {str(CustomException('Failed to get response from backend', error_details=e))}")
    
    elif not system_prompt.strip():
        st.warning("⚠️ Please define your AI agent first!")
    else:
        st.warning("⚠️ Please enter your query!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Built with Streamlit • Powered by Groq & Tavily</p>
</div>
""", unsafe_allow_html=True)