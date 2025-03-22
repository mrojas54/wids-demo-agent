from typing import Annotated, Optional

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class ChatbotState(TypedDict):
    messages: Annotated[list, add_messages]
    session_id: Optional[str] = None
