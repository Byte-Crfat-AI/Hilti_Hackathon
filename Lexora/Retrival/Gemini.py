import google.generativeai as genai
from typing import List, Dict
import os
import numpy as np
from Retriever import FaissSearcher
import tracemalloc

tracemalloc.start()


class RAGSystem:
    def __init__(self, google_api_key=""):

        # Configure Gemini
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
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

    async def get_response(self, relevant_chunks,query):
        
        # Generate prompt
        prompt = self.generate_prompt(query, relevant_chunks)
        
        # Get response from Gemini
        response = await self.model.generate_content_async(prompt)
        return response.text

    # Example usage
    async def respond(self,query,faiss_files,chunks_files):
        text_chunks=self.searcher.return_chunks(query,faiss_files,chunks_files)
        # Get response
        response = await self.get_response(text_chunks,query)
        return response
    
    async def chat(self,query):
        prompt = f"""
        You are Lexora, an advanced AI-powered database management assistant developed by 
        Haris Narrendran, Devansh Yadav, and Manish Shaw, students of IIT Bombay.

        Your goal is to provide accurate, insightful, and well-structured responses based on 
        your extensive knowledge.

        Answer the following question with clarity and precision:
        {query}
        """
        response = await self.model.generate_content_async(prompt)
        return response.text

# import asyncio

# async def main():
#     rag=RAGSystem()
#     response = await rag.respond(
#         'Describe the fourth finger on the left hand',
#         [
#             'Lexora/Database/Embeddings/Embedding_index_to_file1.faiss',
#             'Lexora/Database/Embeddings/Embedding_index_to_file2.faiss'
#         ],
#         [
#             'Lexora/Database/Embeddings/metadata_to_file1.pkl',
#             'Lexora/Database/Embeddings/metadata_to_file2.pkl'
#         ]
#     )
#     return response

# # Run the async function
# print(asyncio.run(main()))
