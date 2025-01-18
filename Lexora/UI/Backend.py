import sys
sys.path.append('D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Processing')
sys.path.append('D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Keyword_Extraction')
sys.path.append('D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Retrival')
from main_processing import MainProcessing
from main_keyword_extraction import MainKeywordExtraction
from main_retrieval import MainRetrieval

class main():
    def setup(root_folder):
        processing = MainProcessing()
        keyword_extraction = MainKeywordExtraction()
        processed_files = processing.main_processing(root_folder)
        keyword_extraction.main_keyword_extraction(processed_files)
        print("Lexora is ready to use")
        
    def query(query):
        retrieval = MainRetrieval()
        return retrieval.main_retrieval(query)
    
    
# Example
main.setup("D:\Hilti_storage")