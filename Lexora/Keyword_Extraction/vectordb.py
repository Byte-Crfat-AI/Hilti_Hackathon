import faiss
import numpy as np
import pickle
import re

class VectorDB:
    def __init__(self):
        pass
    def match_pattern(self, path):
        pattern = r".*[\\/](\w+)[\\/](.+)$"
        match = re.search(pattern, path)
        if match:
            folder_name, file_name = match.groups()
            modified_path = f"{folder_name}_{file_name}"
        else:
            modified_path = path
        return modified_path
    def keywords_db(self,ranked_set, path):
        embeddings = [ranked_set[i][0] for i in range(len(ranked_set))]
        metadata = [[ranked_set[i][1],ranked_set[i][2],path] for i in range(len(ranked_set))]
        embedding_matrix = np.array(embeddings, dtype="float32")
        dimension = embedding_matrix.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embedding_matrix)
        faiss.write_index(index, f'D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Keywords\Keyword_index_{self.match_pattern(path)}.faiss')
        with open(f'D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Keywords\metadata_{self.match_pattern(path)}.pkl', "wb") as f:
            pickle.dump(metadata, f)
        return
    def embeddings_db(self,embeddings, path):
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        faiss.write_index(index, f'D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Embeddings\Embedding_index_{self.match_pattern(path)}.faiss')
        metadata = [path]
        with open(f'D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Embeddings\metadata_{self.match_pattern(path)}.pkl', "wb") as f:
            pickle.dump(metadata, f)   
        return
        
        
    