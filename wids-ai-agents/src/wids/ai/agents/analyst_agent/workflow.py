from typing import Annotated, Literal

# LangGraph and LangChain imports
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command
from typing_extensions import TypedDict

from wids.ai.agents.analyst_agent.tools import perform_eda, presentation_tool, train_model

# Our team supervisor is an LLM node. It just picks the next agent to process
# and decides when the work is completed
members = ["analyst", "scientist", "reporter"]

SUPERVISOR_AGENT_PROMPT = f"""You are a supervisor tasked with managing a conversation between the following workers:
                              {members}.

                              Given the following user request, respond with the worker to act next.
                              Each worker will perform a task and respond with their results and status.
                              Analyze the results carefully and decide which worker to call next accordingly.
                              Remember analyst agent can do exploratory analysis, scientist can build predictive models
                              and reporter can build presentations for executives.
                              When finished, respond with FINISH."""


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal["analyst", "scientist", "reporter", "FINISH"]


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next: str


llm = ChatOpenAI(model="gpt-4o", temperature=0)


def supervisor_node(
    state: AgentState,
) -> Command[Literal["analyst", "scientist", "reporter", "__end__"]]:
    messages = [
        {"role": "system", "content": SUPERVISOR_AGENT_PROMPT},
    ] + state["messages"]
    response = llm.with_structured_output(Router).invoke(
        messages
    )  # Respond which agent to call next or finish
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})


# Create analyst Sub-Agent
analyst_agent = create_react_agent(
    llm,
    tools=[perform_eda],
    state_modifier="""You are a data analyst. You take input csv file, do exploratory data analysis.
                                                Do not build any predictive models. Only do descriptive analysis.
                                                        Once your task is done report your results back to the supervisor.""",
)


def analyst_node(state: AgentState) -> Command[Literal["supervisor"]]:
    result = analyst_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="analyst")
            ]
        },
        goto="supervisor",
    )


# Create a scientist Sub-Agent
scientist_agent = create_react_agent(
    llm,
    tools=[train_model],
    state_modifier="""You are a data scientist. You take input csv file, build predictive model.
                                                Only build the most relevant predictive model related to the question.
                                                        Once your task is done report your results back to the supervisor.""",
)


def scientist_node(state: AgentState) -> Command[Literal["supervisor"]]:
    result = scientist_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="scientist")
            ]
        },
        goto="supervisor",
    )


# Create reporter Sub-Agent
reporter_agent = create_react_agent(
    llm,
    tools=[presentation_tool],
    state_modifier="""You are a reporter who makes presentations. You create presentations for executives.
                     Take the scientist's analysis and build a powerpoint presentation summarizing the key findings.
                     You MUST use the content from the data scientist.
                     Once your task is done, report results back to the supervisor.""",
)


# create node function for reporter sub-agent
def reporter_node(state: AgentState) -> Command[Literal["supervisor"]]:

    last_message = state["messages"][-1].content if state["messages"] else ""

    # Create message for the reporter with the analysis content
    reporter_input = f"""
    Create a presentation with the following content:

    {last_message}

    Translate the numbers. Keep in mind, the audience is business executives.
    """

    modified_state = state.copy()
    modified_state["messages"].append(HumanMessage(content=reporter_input))

    result = reporter_agent.invoke(modified_state)

    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="reporter")
            ]
        },
        goto="supervisor",
    )
