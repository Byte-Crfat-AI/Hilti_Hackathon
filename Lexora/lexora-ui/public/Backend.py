import sys
sys.path.append('/workspace/Hilti_Hackathon/Lexora/Processing')
sys.path.append('/workspace/Hilti_Hackathon/Lexora/Keyword_Extraction')
sys.path.append('/workspace/Hilti_Hackathon/Lexora/Retrival')
from main_processing import MainProcessing
from main_keyword_extraction import MainKeywordExtraction
from main_retrieval import MainRetrieval
from Gemini import RAGSystem
import asyncio

class main:
    def __init__(self):
        self.processing = MainProcessing()
        self.keyword_extraction = MainKeywordExtraction()
        self.retrieval = MainRetrieval()
        self.rag=RAGSystem()

    def setup(self, root_folder):
        processed_files = self.processing.main_processing(root_folder)
        self.keyword_extraction.main_keyword_extraction(processed_files)
        print("Lexora is ready to use")
        
    def query(self, query):
        return self.retrieval.main_retrieval(query)

    def gemini(self,query,faiss_files,chunks_files):
        response = asyncio.run(self.rag.respond(query,faiss_files,chunks_files))
        return response

    
    
# Example
Main = main()
# Main.setup("D:\Hilti_storage")
print(Main.query("Get me the file with Owl"))
print(Main.gemini())