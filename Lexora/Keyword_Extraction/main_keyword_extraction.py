from Keyword_Extraction.vectordb import VectorDB
from Keyword_Extraction.embeddings import Embeddings
from Keyword_Extraction.keyword_ranking import Keyword


class MainKeywordExtraction:
    def __init__(self):
        self.vector_db = VectorDB()
        self.embeddings = Embeddings()
        self.keyword = Keyword()

    def main_keyword_extraction(self, processed_files):
        for text, path in processed_files:
            try:
                # Extract keywords and embeddings
                ranked_set = self.keyword.keyword_main(text)
                embeddings = self.embeddings.get_embeddings(text)
                
                # Store in the database
                self.vector_db.keywords_db(ranked_set, path)
                self.vector_db.embeddings_db(embeddings, path)
            except Exception as e:
                print(f"Error processing {path}: {e}")
        return "Keywords and embeddings stored in the database"
