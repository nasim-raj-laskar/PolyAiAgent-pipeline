from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    ALLOWED_MODEL_NAMES=["llama-3.3-70b-versatile", 
                          "openai/gpt-oss-120b",
                          "openai/gpt-oss-20b",
                          "whisper-large-v3",
                          "meta-llama/llama-guard-4-12b",
                          "whisper-large-v3-turbo"]
settings = Settings()