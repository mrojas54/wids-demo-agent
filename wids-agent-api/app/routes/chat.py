from fastapi import APIRouter, Depends
from openai import AsyncOpenAI
from app.models.chat import ChatRequest, ChatResponse
from app.dependencies.llm import get_llm_client, get_test_chat
from wids.ai.agents.chatbot.graph import ChatbotGraph

router = APIRouter()


@router.get("/chat")
async def chat(client: AsyncOpenAI = Depends(get_llm_client)):
    return await get_test_chat(client)


@router.post("/chat/start", response_model=ChatResponse)
async def start_chat(request: ChatRequest):
    pass
