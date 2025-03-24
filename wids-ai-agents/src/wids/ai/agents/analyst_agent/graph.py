from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver, BaseCheckpointSaver
from wids.ai.agents.analyst_agent.workflow import (
    AgentState,
    analyst_node,
    reporter_node,
    scientist_node,
    supervisor_node,
)


def build_graph(checkpointer: BaseCheckpointSaver | None = None):
    # build the agent graph
    builder = StateGraph(AgentState)
    builder.add_edge(START, "supervisor")
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("analyst", analyst_node)
    builder.add_node("scientist", scientist_node)
    builder.add_node("reporter", reporter_node)
    if not checkpointer:
        checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)
    return graph


graph = build_graph()
