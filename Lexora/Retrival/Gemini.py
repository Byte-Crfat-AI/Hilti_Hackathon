import google.generativeai as genai
from typing import List, Dict
import os
import numpy as np
from Retriever import FaissSearcher
import tracemalloc

tracemalloc.start()


class RAGSystem:
    def __init__(self, google_api_key="AIzaSyASciVtzGPKxHFbPo344pr0XBo59MYmDno"):

        # Configure Gemini
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')


    def generate_prompt(self, query, relevant_chunks):

        context = "\n\n".join(relevant_chunks)
        prompt = f"""Please answer the following question based on the provided context. 
        If the answer cannot be found in the context, please say so.

        Context:
        {context}

        Question: {query}

        Answer:"""
        return prompt

    async def get_response(self, relevant_chunks,query):
        
        # Generate prompt
        prompt = self.generate_prompt(query, relevant_chunks)
        
        # Get response from Gemini
        response = await self.model.generate_content_async(prompt)
        return response.text

    # Example usage
    async def respond(self,query,faiss_files,chunks_files):

        searcher=FaissSearcher()
        text_chunks=searcher.return_chunks(query,faiss_files,chunks_files)
        
        # Get response
        response = await self.get_response(text_chunks,query)
        return response

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
