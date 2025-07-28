import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

# Load your API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

# Function to get 3 varied responses using separate API calls
def get_multiple_responses(message):
    responses = []
    try:
        for _ in range(3):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": message}],
                temperature=1.0  # higher temperature = more variety
            )
            responses.append(response.choices[0].message.content.strip())
    except Exception as e:
        return [f"Error: {e}"]
    
    return responses

# Wrapper to update dropdown with responses
def show_options(message):
    options = get_multiple_responses(message)
    return gr.update(choices=options, value=options[0]), options[0]  # Set first one as default

# Show selected response in output box
def return_selected_response(selected_response):
    return selected_response

# Gradio UI layout
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Multi-Response Chatbot using LLaMA on Groq 🤖 ")
    input_box = gr.Textbox(label="Your message", placeholder="Ask me anything...", lines=2)
    
    generate_button = gr.Button("Get Responses")
    response_dropdown = gr.Dropdown(choices=[], label="Choose your favorite response")
    final_output = gr.Textbox(label="Selected Response")

    # Link actions
    generate_button.click(show_options, inputs=input_box, outputs=[response_dropdown, final_output])
    response_dropdown.change(return_selected_response, inputs=response_dropdown, outputs=final_output)

# Run app
if __name__ == "__main__":
    demo.launch()
