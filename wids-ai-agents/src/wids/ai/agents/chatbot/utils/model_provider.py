import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def get_model(model_name: str, temperature: float = 0, **kwargs):
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    return ChatOpenAI(model=model_name, temperature=temperature, **kwargs)
