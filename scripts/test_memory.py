from app.memory.memory import ConversationMemory


def main():

    session_id = "demo_session"

    memory = ConversationMemory(
        session_id
    )

    print("=" * 60)
    print("MEMORY BEFORE")
    print("=" * 60)

    print(memory.get_messages())

    memory.add_message(
        "user",
        "My order ID is ORD1001."
    )

    memory.add_message(
        "assistant",
        "Got it. I will remember your order ID."
    )

    print("\n" + "=" * 60)
    print("MEMORY AFTER")
    print("=" * 60)

    print(memory.get_messages())

    print("\nMemory saved to:")
    print(memory.file_path)


if __name__ == "__main__":
    main()