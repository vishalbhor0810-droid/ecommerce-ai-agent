import json
from pathlib import Path
from datetime import datetime


MEMORY_DIR = Path("storage/memory")


class ConversationMemory:

    def __init__(self, session_id="default"):

        self.session_id = session_id

        MEMORY_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file_path = (
            MEMORY_DIR /
            f"{session_id}.json"
        )

        self.messages = []

        self.load()

    def load(self):

        if self.file_path.exists():

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.messages = json.load(file)

        else:

            self.messages = []

    def save(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.messages,
                file,
                indent=2
            )

    def add_message(self, role, content):

        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        self.save()

    def get_messages(self):

        return self.messages

    def get_recent_messages(self, limit=10):

        return self.messages[-limit:]