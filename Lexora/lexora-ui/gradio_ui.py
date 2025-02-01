import gradio as gr
import os
import re

def get_lexora_path(path):
    match = re.search(rf'^(.*{re.escape(os.sep)}Lexora)(?:{re.escape(os.sep)}|$)', path)
    return match.group(1) if match else None

Lexora_path = get_lexora_path(os.getcwd())
backend_path = os.path.join(Lexora_path, "lexora-ui", "public")
embeddings_path = os.path.join(Lexora_path, "Database", "Embeddings")
keywords_path = os.path.join(Lexora_path, "Database", "Keywords")

import sys
if os.path.exists(backend_path):
    sys.path.append(backend_path)
else:
    print(f"Warning: Backend path '{backend_path}' not found.")

try:
    from Backend import MainClass
    Main = MainClass()
except ImportError as e:
    print(f"Error importing Backend: {e}")
    Main = None  # Prevent crashes if Backend import fails

def process_value(value):
    if Main:
        Main.setup(value)
        return "Processed Successfully"
    return "Error: Backend not loaded."

def remove_files(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

def delete_value(confirm):
    if confirm:
        remove_files(embeddings_path)
        remove_files(keywords_path)
        return "Deleted Successfully",False
    return "Error: Please confirm before deleting.", confirm

async def chatbot_response(message, history):
    if Main:
        response = await Main.query(message)
        return response
    return "Error: Backend not loaded."

with gr.Blocks() as demo:
    gr.Markdown("# Lexora")

    with gr.Row():
        with gr.Column(scale=1):
            value_input = gr.Textbox(label="Path of the root folder")
            process_button = gr.Button("Process")
            output_text = gr.Textbox(label="Processing Result")
            process_button.click(process_value, value_input, output_text)
            delete_button = gr.Button("Delete Database")
            confirm_delete = gr.Checkbox(label="Confirm before deleting", value=False)
            delete_button.click(delete_value, confirm_delete, [output_text, confirm_delete])

        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(fn=chatbot_response)

if __name__ == "__main__":
    demo.launch(share=True)
