import os
import re
def get_lexora_path(path):
    match = re.search(r'^(.*\\Lexora)(?:\\|$)', path)
    if match:
        return match.group(1)
    return None
Lexora_path = get_lexora_path(os.getcwd())
keyword_extraction_path = os.path.join(Lexora_path , "Keyword_Extraction")
Processing_path = os.path.join(Lexora_path , "Processing")
Retrival_path = os.path.join(Lexora_path , "Retrival")
import sys
sys.path.append(keyword_extraction_path)
sys.path.append(Processing_path)
sys.path.append(Retrival_path)
from main_processing import MainProcessing
from main_keyword_extraction import MainKeywordExtraction
from main_retrieval import MainRetrieval
import asyncio

class main:
    def __init__(self):
        self.processing = MainProcessing()
        self.keyword_extraction = MainKeywordExtraction()
        self.retrieval = MainRetrieval()

    def setup(self, root_folder):
        processed_files = self.processing.main_processing(root_folder)
        self.keyword_extraction.main_keyword_extraction(processed_files)
        print("Lexora is ready to use")
        
    def query(self, query):
        return self.retrieval.main_retrieval(query)

    
    
# Example
# Main = main()
# root_folder = "D:\Hilti_storage"
# Main.setup(root_folder)
# print(Main.query("Name a few pre-alloyed powders used in diamond tool industry."))
