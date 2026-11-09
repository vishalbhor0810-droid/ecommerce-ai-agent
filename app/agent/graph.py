import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.memory.memory import ConversationMemory

from app.agent.nodes import (
    agent_node,
    tools_node,
    route_after_agent,
    finalize_node,
    save_memory,
    pii_guardrail,
    injection_guardrail,
    injection_block_node
)


def load_memory(state):
    # Each session has its own history, so users never see each other's chats
    memory = ConversationMemory(state.get("session_id", "default"))
    return {
        "conversation_history": memory.get_recent_messages(10),

        # The checkpointer keeps state between turns of the same thread,
        # so clear everything from the previous turn before starting
        "messages": [],
        "tools_used": [],
        "tool_iterations": 0,
        "llm_error": False,
        "retrieved_context": [],
        "order_results": [],
        "answer": "",
        "source": None,
        "similarity": None,
        "intent": ""
    }


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
    graph.add_node("injection_guardrail", injection_guardrail)
    graph.add_node("injection_block", injection_block_node)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)
    graph.add_node("finalize", finalize_node)
    graph.add_node("save_memory", save_memory)

    # Entry point
    graph.set_entry_point("load_memory")

    # Input guardrails run before the LLM sees anything
    graph.add_edge("load_memory", "pii_guardrail")
    graph.add_edge("pii_guardrail", "injection_guardrail")

    graph.add_conditional_edges(
        "injection_guardrail",
        route_after_injection,
        {
            "block": "injection_block",
            "continue": "agent"
        }
    )

    graph.add_edge("injection_block", END)

    # Agent loop: the LLM calls tools until it has enough to answer
    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "finalize": "finalize"
        }
    )

    graph.add_edge("tools", "agent")

    # Output guardrails, then save memory before ending
    graph.add_edge("finalize", "save_memory")
    graph.add_edge("save_memory", END)

    # Return compiled graph with checkpointer attached
    return graph.compile(checkpointer=checkpointer)


# Compiled app instance for easy importing
app = build_graph()
