from openai import AsyncOpenAI

from app.utils.constants import MODEL_NAME


async def get_llm_client(openai_api_key: str) -> AsyncOpenAI:
    return AsyncOpenAI(api_key=openai_api_key)


async def get_test_chat(
    client: AsyncOpenAI, input: str, model_name: str = MODEL_NAME
) -> str:
    generate_story_prompt = """
    You are a loving mother spending time wih her sleepy baby. Your son loves 
    knights, castles, and fighting dragons. Create a bedtime story where the 
    knight overcomes evil to save the princess. The story should be 100 words or 
    less.
    """
    chat_messages = [
        {"role": "user", "content": generate_story_prompt},
        {"role": "user", "content": input},
    ]

    response = await client.completions.create(
        model=model_name, messages=chat_messages, temperature=0.7
    )
    return response.choices[0].message.content
