import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

# Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client with your API key
client = Groq(api_key=api_key)

# Function to send message to Groq and return the response
def ask_groq(message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message}],
            n=3
        )

        for i,choice in enumerate(response.choices):
            print(f"Response {i+1}: \n{choice.message.content}\n")
        # return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Gradio interface setup
demo = gr.Interface(
    fn=ask_groq,
    inputs=gr.Textbox(lines=2, placeholder="Ask me anything..."),
    outputs="text",
    title="Groq Chatbot",
    description="Single-message chatbot powered by LLaMA on Groq"
)

# Launch the web app
if __name__ == "__main__":
    demo.launch()
