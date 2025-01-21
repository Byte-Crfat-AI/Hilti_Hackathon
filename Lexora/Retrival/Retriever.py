import os
import textwrap
from pathlib import Path
import asyncio
import logging
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from llama_parse import LlamaParse
import google.generativeai as genai
import sys
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


class Retriever():
    def __init__(self):
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        os.environ["GOOGLE_API_KEY"] = "AIzaSyASciVtzGPKxHFbPo344pr0XBo59MYmDno"
        os.environ["GROQ_API_KEY"] = "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"
        logging.getLogger("httpx").setLevel(logging.WARNING)
        genai.configure(api_key="AIzaSyASciVtzGPKxHFbPo344pr0XBo59MYmDno")
        self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

    def disable_prints(self,func, *args, **kwargs):
        # Redirect standard output to null
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            result = func(*args, **kwargs)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout
        return result

    def hyde_query(self,query):
        hyde_prompt = (
            "Given the following query, create a hypothetical answer as if it were correct and complete:\n"
            f"Query: {query}\n\n"
            "Hypothetical Answer:"
        )
        return self.llm.invoke(hyde_prompt)


    def print_response(self,response):
        print('AI:',end=' ')
        response_txt = response["result"]
        for chunk in response_txt.split("\n"):
            if not chunk:
                print()
                continue
            print("\n".join(textwrap.wrap(chunk, 100, break_long_words=False)))

    def retriever(self,faiss_index):
        # Initialize FAISS retriever
        retriever = FAISS(faiss_index).as_retriever(search_kwargs={"k": 10})

        # Set up a FlashRank compressor
        compressor = FlashRankRerank(model="ms-marco-MiniLM-L-12-v2")

        # Create a compression retriever
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=retriever
        )

        # Define the prompt template
        prompt_template = """
        You are Lexora, a AI powered database manager.
        Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}
        Question: {question}

        Answer the question and provide additional helpful information,
        based on the pieces of information, if applicable. Be succinct.

        Responses should be properly formatted to be easily read.
        """

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Set up the QA system
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=compression_retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt, "verbose": True},
        )

        return qa


    def return_chunks(self,qs):
        qa=self.retriever('Database/Keywords/Keyword_index_to_file.txt.faiss')
        qry=self.hyde_query(qs)
        response = disable_prints(qa.invoke,qry)

        # Extract the answer and source documents
        answer = response["result"]
        source_documents = response["source_documents"]

        # Display or use the source documents with metadata
        for doc in source_documents:
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")

        return source_documents
