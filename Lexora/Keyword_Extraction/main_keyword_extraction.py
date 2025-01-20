from vectordb import VectorDB
from embeddings import Embeddings
from keyword_ranking import Keyword


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
                embeddings, chunks = self.embeddings.get_embeddings(text)
                
                # Store in the database
                self.vector_db.keywords_db(ranked_set, path)
                self.vector_db.embeddings_db(embeddings, chunks, path)
            except Exception as e:
                print(f"Error processing {path}: {e}")
        return "Keywords and embeddings stored in the database"
