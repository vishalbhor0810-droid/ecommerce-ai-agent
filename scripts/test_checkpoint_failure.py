import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict


class State(TypedDict, total=False):
    value: str


attempts = {"count": 0}


def node_a(state):
    print("NODE A EXECUTED")
    return {"value": "A completed"}


def node_b(state):
    attempts["count"] += 1

    if attempts["count"] == 1:
        print("NODE B FAILED")
        raise RuntimeError("Simulated failure")

    print("NODE B RESUMED")
    return {"value": "B completed"}


builder = StateGraph(State)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", END)

conn = sqlite3.connect(
    "storage/checkpoints/checkpoints.db",
    check_same_thread=False
)
checkpointer = SqliteSaver(conn)
graph = builder.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "failure-demo"
    }
}

print("FIRST RUN")
try:
    graph.invoke({"value": ""}, config=config)
except RuntimeError as e:
    print("Caught:", e)

print("\nRESUMING")
result = graph.invoke(None, config=config)

print("\nFINAL STATE:")
print(result)