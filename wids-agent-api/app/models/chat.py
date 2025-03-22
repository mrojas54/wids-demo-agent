from pydantic import BaseModel, Field
from enum import Enum


class ModelName(str, Enum):
    CLAUDE_3_5_SONNET_20240620 = "claude-3-5-sonnet-20240620"
    GPT_4_TURBO_2024_04_09 = "gpt-4-turbo-2024-04-09"


class ChatRequest(BaseModel):
    user_input: str
    model_name: ModelName = Field(default=ModelName.GPT_4_TURBO_2024_04_09)
    temperature: float = Field(default=0.0)
    recursion_limit: int = Field(default=25)


class ChatResponse(BaseModel):
    response: str
    session_id: str
