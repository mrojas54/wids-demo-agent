import uuid
import traceback
from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.logger import logger
from openai import AsyncOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from app.models.chat import ChatRequest, ChatResponse
from app.dependencies.llm import get_llm_client, get_test_chat
from wids.ai.agents.chatbot.graph import ChatbotGraph

router = APIRouter()


@router.get("/chat")
async def chat(client: AsyncOpenAI = Depends(get_llm_client)):
    return await get_test_chat(client)


@router.post("/chat/start", response_model=ChatResponse)
async def start_chat(chat_request: ChatRequest, request: Request):
    """Start a new chat session with the agent"""
    try:
        graph = ChatbotGraph(
            model_name=chat_request.model_name, temperature=chat_request.temperature
        )

        session_id = str(uuid.uuid4())

        inputs = {"messages": [{"role": "user", "content": chat_request.user_input}]}
        config = {
            "recursion_limit": chat_request.recursion_limit,
            "configurable": {"thread_id": session_id},
        }

        output: List[AIMessage] = await graph.ainvoke(input=inputs, config=config)

        request.state.chat_sessions[session_id] = {
            "graph": graph,
            "state": output,
            "config": config,
        }

        return ChatResponse(
            response=output["messages"][-1].content, session_id=session_id
        )
    except Exception as e:
        logger.error(f"Error starting chat: {traceback.format_exc()}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/chat/{session_id}/continue", response_model=ChatResponse)
async def continue_chat(session_id: str, chat_request: ChatRequest, request: Request):
    """Continue chat with user input"""
    try:
        uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid chat session ID")
    if session_id not in request.state.chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    chat_session = request.state.chat_sessions[session_id]
    chat_session["state"]["messages"].append(
        HumanMessage(content=chat_request.user_input)
    )

    new_state = await chat_session["graph"].ainvoke(
        chat_session["state"], chat_session["config"]
    )

    request.state.chat_sessions[session_id].update({"state": new_state})

    return ChatResponse(
        response=new_state["messages"][-1].content, session_id=session_id
    )


@router.get("/chat/sessions")
async def list_sessions(request: Request):
    """List all active chat sessions"""
    return {"sessions": list(request.state.chat_sessions.keys())}


@router.delete("/chat/{session_id}")
async def end_session(session_id: str, request: Request):
    """End a chat session"""
    try:
        uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid chat session ID")
    if session_id not in request.state.chat_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")

    del request.state.chat_sessions[session_id]

    return {"message": "Session ended successfully"}
