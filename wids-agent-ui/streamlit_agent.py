import asyncio
import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories.streamlit import (
    StreamlitChatMessageHistory,
)
from wids.ai.agents.analyst_agent.graph import build_graph
from wids.ai.agents.chatbot.utils.constants import (
    MODEL_NAME,
)

from utils.st_callable_util import (
    get_streamlit_cb,
)  # Utility function to get a Streamlit callback handler with context

load_dotenv()

st.title("StreamLit 🤝 LangGraph")
st.markdown("#### Secret Agent Demo")


# Check if the API key is available as an environment variable
if not os.getenv("OPENAI_API_KEY"):
    # If not, display a sidebar input for the user to provide the API key
    st.sidebar.header("OPENAI_API_KEY Setup")
    api_key = st.sidebar.text_input(
        label="API Key", type="password", label_visibility="collapsed"
    )
    os.environ["OPENAI_API_KEY"] = api_key
    # If no key is provided, show an info message and stop further execution and wait till key is entered
    if not api_key:
        st.info("Please enter your OPENAI_API_KEY in the sidebar.")
        st.stop()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()

if "graph" not in st.session_state:
    st.session_state.graph = build_graph(st.session_state.memory)

message_history = StreamlitChatMessageHistory(key="langchain_messages")
memory = st.session_state["memory"]
if len(message_history.messages) == 0 or st.sidebar.button("Clear message history"):
    message_history.clear()
    message_history.add_ai_message("How can I help you?")

# Loop through all messages in the session state and render them as a chat on every st.refresh mech
avatars = {"human": "user", "ai": "assistant"}
for msg in message_history.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

# takes new input in chat box from user and invokes the graph
if prompt := st.chat_input(placeholder="Ask me anything..."):
    message_history.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # Process the AI's response and handles graph events using the callback mechanism
    with st.chat_message("assistant"):
        msg_placeholder = (
            st.empty()
        )  # Placeholder for visually updating AI's response after events end
        # create a new placeholder for streaming messages and other events, and give it context
        st_callback = get_streamlit_cb(st.container())
        response = asyncio.run(
            st.session_state.graph.ainvoke(
                input={"messages": [{"role": "user", "content": prompt}]},
                config={
                    "callbacks": [st_callback],
                    "configurable": {"thread_id": st.session_state.thread_id},
                },
            )
        )
        last_msg = response["messages"][-1].content
        message_history.messages.append(
            AIMessage(content=last_msg)
        )  # Add that last message to the st_message_state
        msg_placeholder.write(
            last_msg
        )  # visually refresh the complete response after the callback container
