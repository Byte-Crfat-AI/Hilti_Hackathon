import faiss
import numpy as np
import pickle
import re
import os

class VectorDB:
    def __init__(self):
        self.base_path = os.path.join(os.getcwd(), "Database")
    def match_pattern(self, path):
        folder_name = os.path.basename(os.path.dirname(path))
        file_name = os.path.splitext(os.path.basename(path))[0]
        return f"{folder_name}_{file_name.replace('.', '_')}"
    
    def keywords_db(self, ranked_set, path):
        embeddings = [ranked_set[i][0] for i in range(len(ranked_set))]
        metadata = [[ranked_set[i][1], ranked_set[i][2], path] for i in range(len(ranked_set))]
        embedding_matrix = np.array(embeddings, dtype="float32")
        dimension = embedding_matrix.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embedding_matrix)
        base_dir = os.path.join(os.getcwd(), "Lexora", "Database")
        keyword_dir = os.path.join(base_dir, "Keywords")
        os.makedirs(keyword_dir, exist_ok=True)
        modified_path = self.match_pattern(path)
        faiss.write_index(index, os.path.join(keyword_dir, f"Keyword_index_{modified_path}.faiss"))
        with open(os.path.join(keyword_dir, f"metadata_{modified_path}.pkl"), "wb") as f:
            pickle.dump(metadata, f)

    def embeddings_db(self, embeddings,chunks, path):
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        base_dir = os.path.join(os.getcwd(), "Lexora", "Database")
        embedding_dir = os.path.join(base_dir, "Embeddings")
        os.makedirs(embedding_dir, exist_ok=True)
        modified_path = self.match_pattern(path)
        faiss.write_index(index, os.path.join(embedding_dir, f"Embedding_index_{modified_path}.faiss"))
        metadata = chunks
        with open(os.path.join(embedding_dir, f"metadata_{modified_path}.pkl"), "wb") as f:
            pickle.dump(metadata, f)
