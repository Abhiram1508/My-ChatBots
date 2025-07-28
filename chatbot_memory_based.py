import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

# Load API Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Store the conversation history
chat_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

# Function to get response with chat memory
def chat_with_memory(user_message):
    # Add user message to history
    chat_history.append({"role": "user", "content": user_message})
    
    # Call the model with full conversation so far
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_history,
        temperature=1
    )

    # Extract model reply
    assistant_reply = response.choices[0].message.content.strip()

    # Add assistant reply to history
    chat_history.append({"role": "assistant", "content": assistant_reply})

    # Format chat for display
    formatted_chat = ""
    for msg in chat_history[1:]:  # skip system message
        role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 AI"
        formatted_chat += f"{role}: {msg['content']}\n ===================================== \n"
    
    return formatted_chat, gr.update(value="")

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Chatbot with Memory using Groq + LLaMA")
    
    chat_output = gr.Textbox(label="Conversation", lines=20, interactive=False)
    user_input = gr.Textbox(label="Your message", placeholder="Type a message and hit Enter", lines=2)
    send_button = gr.Button("Send")

    send_button.click(fn=chat_with_memory, inputs=user_input, outputs=[chat_output, user_input])
    user_input.submit(fn=chat_with_memory, inputs=user_input, outputs=[chat_output, user_input])

if __name__ == "__main__":
    demo.launch()
