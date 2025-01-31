import gradio as gr
import os
import re
def get_lexora_path(path):
    match = re.search(r'^(.*\\Lexora)(?:\\|$)', path)
    if match:
        return match.group(1)
    return None
Lexora_path = get_lexora_path(os.getcwd())
backend_path = os.path.join(Lexora_path , "lexora-ui\public")
import sys
sys.path.append(backend_path)
from Backend import MainClass
Main = MainClass()

def process_value(value):
    response = Main.setup(value)
    return "Processed Successfully"

def chatbot_response(message, history):
    response = Main.query(message)
    return response

with gr.Blocks() as demo:
    gr.Markdown("# Lexora")
    with gr.Row():
        with gr.Column(scale=1):
            value_input = gr.Textbox(label="Path of the root folder")
            process_button = gr.Button("Process")
            output_text = gr.Textbox(label="")
            process_button.click(process_value, value_input, output_text)
        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(fn=chatbot_response)

if __name__ == "__main__":
    demo.launch(share=True)
