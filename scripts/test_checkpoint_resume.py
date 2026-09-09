from app.agent.graph import app

config = {
    "configurable": {
        "thread_id": "resume-demo"
    }
}

print("FIRST RUN")
result = app.invoke(
    {"query": "What is your return policy?"},
    config=config
)

print(result["answer"])

print("\nSECOND RUN - SAME THREAD")
result = app.invoke(
    {"query": "How long do refunds take?"},
    config=config
)

print(result["answer"])