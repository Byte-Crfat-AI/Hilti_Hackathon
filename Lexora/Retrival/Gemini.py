import ollama
from typing import List
import tracemalloc
from Retriever import FaissSearcher
import requests
import json
import re
import time 

# Define the Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Model you want to use
MODEL_NAME = "deepseek-r1"

tracemalloc.start()


class RAGSystem:
    def __init__(self, model_name="deepseek-r1"):
        # Load the local LLM
        self.model_name = model_name
        self.searcher = FaissSearcher()

    def generate_prompt(self, query, relevant_chunks):
        context = "\n\n".join(relevant_chunks)
        prompt = f"""
        You are Lexora, an advanced AI-based database management system. Your primary goal is to provide detailed and accurate responses to questions based on the given context. Follow these guidelines while crafting your response:

        1. **Context-Specific Answers:**
        - Analyze the provided context thoroughly.
        - If the question can be answered using the context, provide a detailed explanation derived from it.

        2. **Beyond Context:**
        - If the answer is not present in the context, respond based on your general knowledge.
        - Clearly state that the answer was derived outside the provided context.
        
        **Context:**
        {context}
        
        **Question:**
        {query}
        """
        return prompt

    def clean_response(self,text):
        """Removes <think> and </think> tags from the response."""
        return re.sub(r"</?think>", "\nthinking\n", text).strip()

    def chat_with_ollama(self,prompt):
        """Sends a prompt to Ollama and cleans the response."""
        data = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        print('Starting Local DeepSeek-r1 (7B)')
        start_time=time.time()

        response = requests.post(OLLAMA_API_URL, json=data)

        end_time=time.time()
        print('Time Taken for ollama :',end_time-start_time)

        if response.status_code == 200:
            result = response.json()
            cleaned_response = self.clean_response(result.get("response", ""))
            return cleaned_response
        else:
            return "Error: " + response.text

    def get_response(self, relevant_chunks, query):
        # Generate prompt
        prompt = self.generate_prompt(query, relevant_chunks)
        
        # Get response from local LLM
        response = self.chat_with_ollama(prompt)
        return response

    def respond(self, query, faiss_files, chunks_files):
        text_chunks = self.searcher.return_chunks(query, faiss_files, chunks_files)
        response = self.get_response(text_chunks, query)
        return response

    def chat(self, query):
        prompt = f"""
        You are Lexora, an advanced AI-based database management system.
        You are designed by Haris Narrendran, Devansh Yadav, and Manish Shaw, students of IIT Bombay.
        Answer the following question based on your knowledge:
        {query}
        """
        response = self.chat_with_ollama(prompt)
        return response