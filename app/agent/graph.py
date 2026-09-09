import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.memory.memory import ConversationMemory

from app.agent.nodes import (
    classify_query,
    retrieve_kb,
    order_tool_node,
    fallback_node,
    generate_answer,
    save_memory,
    pii_guardrail,
    injection_guardrail,
    injection_block_node
)


def load_memory(state):
    memory = ConversationMemory("demo_session")
    return {
        "conversation_history": memory.get_recent_messages(10)
    }


def route_after_classification(state):
    intent = state.get("intent")

    if intent == "rag":
        return "retrieve_kb"

    if intent == "order":
        return "order_tool"

    return "fallback"


def route_after_injection(state):
    if state.get("injection_detected", False):
        return "block"

    return "continue"


def build_graph():
    # Ensure storage directory exists
    os.makedirs("storage/checkpoints", exist_ok=True)

    # Initialize SQLite checkpointer
    conn = sqlite3.connect(
        "storage/checkpoints/checkpoints.db",
        check_same_thread=False
    )
    checkpointer = SqliteSaver(conn)

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("load_memory", load_memory)
    graph.add_node("pii_guardrail", pii_guardrail)
    graph.add_node("classify_query", classify_query)
    graph.add_node("retrieve_kb", retrieve_kb)
    graph.add_node("order_tool", order_tool_node)
    graph.add_node("injection_guardrail", injection_guardrail)
    graph.add_node("injection_block", injection_block_node)
    graph.add_node("fallback", fallback_node)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("save_memory", save_memory)

    # Entry point
    graph.set_entry_point("load_memory")

    # Edges
    graph.add_edge("load_memory", "pii_guardrail")
    graph.add_edge("pii_guardrail", "injection_guardrail")

    graph.add_conditional_edges(
        "injection_guardrail",
        route_after_injection,
        {
            "block": "injection_block",
            "continue": "classify_query"
        }
    )

    graph.add_conditional_edges(
        "classify_query",
        route_after_classification,
        {
            "retrieve_kb": "retrieve_kb",
            "order_tool": "order_tool",
            "fallback": "fallback"
        }
    )

    # All paths lead to generate_answer
    graph.add_edge("retrieve_kb", "generate_answer")
    graph.add_edge("order_tool", "generate_answer")
    graph.add_edge("fallback", "generate_answer")

    # Save memory before ending
    graph.add_edge("generate_answer", "save_memory")
    graph.add_edge("save_memory", END)

    # Return compiled graph with checkpointer attached
    return graph.compile(checkpointer=checkpointer)


# Compiled app instance for easy importing
app = build_graph()
# from langgraph.graph import StateGraph, END

# from app.agent.state import AgentState
# from app.memory.memory import ConversationMemory

# from app.agent.nodes import (
#     classify_query,
#     retrieve_kb,
#     order_tool_node,
#     fallback_node,
#     generate_answer
# )


# def load_memory(state):
#     memory = ConversationMemory("demo_session")

#     return {
#         "conversation_history": memory.get_recent_messages(10)
#     }


# def route_after_classification(state):

#     intent = state.get("intent")

#     if intent == "rag":
#         return "retrieve_kb"

#     if intent == "order":
#         return "order_tool"

#     return "fallback"


# def build_graph():

#     graph = StateGraph(AgentState)

#     # Nodes
#     graph.add_node(
#         "load_memory",
#         load_memory
#     )

#     graph.add_node(
#         "classify_query",
#         classify_query
#     )

#     graph.add_node(
#         "retrieve_kb",
#         retrieve_kb
#     )

#     graph.add_node(
#         "order_tool",
#         order_tool_node
#     )

#     graph.add_node(
#         "fallback",
#         fallback_node
#     )

#     graph.add_node(
#         "generate_answer",
#         generate_answer
#     )

#     # Entry point set to load_memory
#     graph.set_entry_point("load_memory")

#     # Flow from load_memory to classify_query
#     graph.add_edge("load_memory", "classify_query")

#     # Conditional routing
#     graph.add_conditional_edges(
#         "classify_query",
#         route_after_classification,
#         {
#             "retrieve_kb": "retrieve_kb",
#             "order_tool": "order_tool",
#             "fallback": "fallback"
#         }
#     )

#     # All branches eventually generate an answer
#     graph.add_edge(
#         "retrieve_kb",
#         "generate_answer"
#     )

#     graph.add_edge(
#         "order_tool",
#         "generate_answer"
#     )

#     graph.add_edge(
#         "fallback",
#         "generate_answer"
#     )

#     graph.add_edge(
#         "generate_answer",
#         END
#     )

#     return graph.compile()