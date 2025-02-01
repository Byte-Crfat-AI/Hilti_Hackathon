import os
import re
import warnings
warnings.filterwarnings("ignore")

def get_lexora_path(path):
    match = re.search(r'^(.*\\Lexora)(?:\\|$)', path)
    if match:
        return match.group(1)
    return None
Lexora_path = '/workspace/Hilti_Hackathon/Lexora'
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

class MainClass:
    def __init__(self):
        self.processing = MainProcessing()
        self.keyword_extraction = MainKeywordExtraction()
        self.retrieval = MainRetrieval()

    def setup(self, root_folder):
        processed_files = self.processing.main_processing(root_folder)
        self.keyword_extraction.main_keyword_extraction(processed_files)
        print("Lexora is ready to use")
        
    async def query(self, query):
        return self.retrieval.main_retrieval(query)

    
    
# Example
# Main = MainClass()
# root_folder = "D:\Hilti_Hackathon\Hilti_Hackathon\Target_Folder"
# Main.setup(root_folder)
# print(Main.query("get me the file with a text 'collect moments not things' "))

# import sys

# def main():
#     if len(sys.argv) < 2:
#         print("Usage: python Backend.py [setup|query] [argument]")
#         sys.exit(1)

#     action = sys.argv[1]
#     Main = MainClass()  

#     if action == 'setup' and len(sys.argv) == 3:
#         root_folder = sys.argv[2]
#         Main.setup(root_folder)
#     elif action == 'query' and len(sys.argv) == 3:
#         query = sys.argv[2]
#         result = Main.query(query)
#         print(result)
#     else:
#         print("Invalid arguments")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()