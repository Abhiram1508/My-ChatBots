import dotenv as env
import os
import os

from groq import Groq

env.load_dotenv()

a = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)
print(chat_completion.choices[0].message.content)