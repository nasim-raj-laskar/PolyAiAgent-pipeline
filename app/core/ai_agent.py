import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from app.config.settings import settings

load_dotenv()

def get_response_from_ai_agents(llm_id,query,allow_search,system_prompt):
    
    # Set API keys
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY
    if allow_search:
        os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
    
    llm=ChatGroq(model=llm_id, api_key=settings.GROQ_API_KEY)
    tools=[TavilySearchResults(max_results=2)] if allow_search else []

    agent=create_react_agent(
        model=llm,
        tools=tools
    )
    
    # Prepare messages with system prompt
    messages = [SystemMessage(content=system_prompt)]
    if isinstance(query, list):
        messages.extend([HumanMessage(content=msg) for msg in query])
    else:
        messages.append(HumanMessage(content=query))
    
    state={"messages": messages}

    response=agent.invoke(state)

    messages=response.get("messages")
    ai_message=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_message[-1] if ai_message else "No response generated"