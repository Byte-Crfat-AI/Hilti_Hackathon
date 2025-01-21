import sys
sys.path.append('D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Processing')
sys.path.append('D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Keyword_Extraction')
sys.path.append('D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Retrival')
from main_processing import MainProcessing
from main_keyword_extraction import MainKeywordExtraction
from main_retrieval import MainRetrieval

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
Main = main()
Main.setup("D:\Hilti_storage")
print(Main.query("Get me the file with Owl"))