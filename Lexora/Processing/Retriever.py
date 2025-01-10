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
from langchain.vectorstores import Qdrant
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from llama_parse import LlamaParse
import sys

os.environ["GROQ_API_KEY"] = "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"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
logging.getLogger("httpx").setLevel(logging.WARNING)
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

def disable_prints(func, *args, **kwargs):
    # Redirect standard output to null
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    
    try:
        result = func(*args, **kwargs)
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout
    
    return result

def hyde_query(query):
    hyde_prompt = (
        "Given the following query, create a hypothetical answer as if it were correct and complete:\n"
        f"Query: {query}\n\n"
        "Hypothetical Answer:"
    )
    return llm.invoke(hyde_prompt).content


def print_response(response):
    print('AI:',end=' ')
    response_txt = response["result"]
    for chunk in response_txt.split("\n"):
        if not chunk:
            print()
            continue
        print("\n".join(textwrap.wrap(chunk, 100, break_long_words=False)))

def load_documents():
    loader = UnstructuredMarkdownLoader('/workspace/Hilti_Hackathon/Lexora/Processing/parsed_document.md')
    loaded_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=128)
    docs = text_splitter.split_documents(loaded_documents)
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        path="./db3",
        collection_name="document_embeddings",
    )

    return qdrant

def retriever(llm,qdrant):
    retriever = qdrant.as_retriever(search_kwargs={"k": 10})
    compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2")
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )

    prompt_template = """
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
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=compression_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt, "verbose": True},
    )

    return qa


def return_chunks(qa,qs):
    qry=hyde_query(qs)
    response = disable_prints(qa.invoke,qry)

    # Extract the answer and source documents
    answer = response["result"]
    source_documents = response["source_documents"]

    # Display or use the source documents with metadata
    for doc in source_documents:
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")

    return source_documents
