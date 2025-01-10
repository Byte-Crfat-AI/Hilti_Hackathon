from Processing.main_processing import MainProcessing
from Keyword_Extraction.main_keyword_extraction import MainKeywordExtraction

def main():
    processing = MainProcessing()
    keyword_extraction = MainKeywordExtraction()
    processed_files = processing.main_processing(processing.root_folder)
    keyword_extraction.Main_keyword_extraction(processed_files)
    return "Lexora is ready to use"