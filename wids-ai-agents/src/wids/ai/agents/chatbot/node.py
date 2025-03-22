from typing import Optional, List

from langchain_core.messages import SystemMessage

from agents.chatbot.state import ChatbotState
from agents.chatbot.utils.model_provider import get_model


class ChatbotNode:
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        system_prompt: str = "You are a helpful assistent.",
    ) -> None:
        self.system_message = SystemMessage(content=system_prompt)
        self.model = get_model(model_name, temperature)

    def run(self, state: ChatbotState) -> ChatbotState:
        messages = state["messages"]

        # Ensure system message is always first
        if not messages or isinstance(messages[0]) != SystemMessage:
            messages.insert(0, self.system_message)

        response = self.model.invoke(messages)
        state["messages"].append(response)
        return state
