from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger=get_logger(__name__)
app=FastAPI(title="PolyAgent")

class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search:bool

@app.post("/chat")
def chat_endpoint(request:RequestState):
    logger.info(f"Received request: {request.model_name}")
    
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")    
        raise HTTPException(status_code=400, detail="Invalid model name")
    try:  
        logger.info(f"Calling AI agent with model: {request.model_name}")
        response=get_response_from_ai_agents(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        logger.info(f"Successfully got Response from AI: {request.model_name}")

        return {"response":response}
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to get AI response: {str(e)}"
            )