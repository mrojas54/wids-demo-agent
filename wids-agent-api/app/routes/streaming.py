import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from langchain_core.messages import HumanMessage

router = APIRouter()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, request: Request):
    await websocket.accept()
    chat_session = request.state.chat_sessions[session_id]

    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            chat_session["state"]["messages"].append(
                [HumanMessage(content=json_data["user_input"])]
            )
            await websocket.send_text("Processing your query...")

            # Stream assistant's response
            try:
                async for event in chat_session.graph.astream(
                    chat_session["state"], chat_session["config"]
                ):
                    await websocket.send_text(event[0].content)
            except Exception as e:
                await websocket.send_text(f"Error occurred: {e}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
