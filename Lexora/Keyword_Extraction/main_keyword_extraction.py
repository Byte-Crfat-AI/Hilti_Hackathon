from vectordb import VectorDB
from embeddings import Embeddings
from keyword_ranking import Keyword

class MainKeywordExtraction:
    def __init__(self):
        self.vector_db = VectorDB()
        self.embeddings = Embeddings()
        self.keyword = Keyword()
    def Main_keyword_extraction(self,processed_files):
        for text,path in processed_files:
            # Extract the keywords from the text
            ranked_set = self.keyword.keyword_main(text)
            # File embeddings
            embeddings = self.embeddings.get_embeddings(text)
            # Store the keywords in the database
            self.vector_db.keywords_db(ranked_set, path)
            self.vector_db.embeddings_db(embeddings, path)
        return "Keywords and embeddings stored in the database"
    