import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger=get_logger(__name__)

st.set_page_config(
    page_title="PolyAgent",
    page_icon="🤖",
    layout="centered"
)
st.title("Multi Ai Agent - Groq and Tavily")
st.caption("🚀 A streamlit chatbot powered by Groq and Tavily search"
           )

system_prompt=st.text_area(
    "Define your AI AGENT:",height=70)

selected_model=st.selectbox(
    "Select a model",
    settings.ALLOWED_MODEL_NAMES)

allow_web_search=st.checkbox(
    "Allow web search")

user_query=st.text_area("Enter Your Query:",height=150)
API_URL="http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload={
        "model_name":selected_model,
        "system_prompt":system_prompt,
        "messages":[user_query],
        "allow_search":allow_web_search
    }
    try:
        logger.info("Sending request to backend")
        response=requests.post(API_URL,json=payload)
        if response.status_code==200:
            agent_response=response.json().get("response","")
            logger.info("Received response from backend")
            st.subheader("Agent Response:")
            st.markdown(agent_response.replace("\n","<br>"),unsafe_allow_html=True)
        else:
            logger.error(f"Error in response from backend: {response.status_code}")
            st.error("Failed to get response from backend")
    except Exception as e:
        logger.error(f"Error in sending request to backend: {e}")
        st.error(str(CustomException("Failed to get response from backend",error_details=e)))
