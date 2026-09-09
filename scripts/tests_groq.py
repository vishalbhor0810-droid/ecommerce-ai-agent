import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are an e-commerce customer support assistant."
        },
        {
            "role": "user",
            "content": "What is an e-commerce return policy?"
        }
    ]
)

print(response.choices[0].message.content)