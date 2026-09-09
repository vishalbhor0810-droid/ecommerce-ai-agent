from app.agent.graph import app

def main():
    config = {
        "configurable": {
            "thread_id": "checkpoint-demo"
        }
    }

    print("Invoking agent with SQLite checkpointing enabled...")
    result = app.invoke(
        {"query": "What is the return policy?"},
        config=config
    )

    print("\nAGENT RESULT:")
    print(result)
    print("\nCheckpoint database created successfully.")

if __name__ == "__main__":
    main()