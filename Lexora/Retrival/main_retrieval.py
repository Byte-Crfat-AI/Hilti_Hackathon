from Decision import get_intent
import sys
sys.path.append("D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Keyword_Extraction")
from keyword_ranking import Keyword
import os
import faiss
import numpy as np
import pickle
from tqdm import tqdm

class MainRetrieval:
    def __init__(self):
        self.keyword = Keyword()
    def main_retrieval(self, query):
        intent = get_intent(query)
        ranked_set = self.keyword.keyword_main(query)
        keyword_faiss = os.listdir(r"D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Keywords")
        keyword_faiss = [keyword_faiss[i] for i in range(len(keyword_faiss)) if keyword_faiss[i][-6:] == ".index"]
        keyword_metadata = [f'metadata_{keyword_faiss[i][14:-6]}.pkl' for i in range(len(keyword_faiss))]
        files = {}
        for i in tqdm(range(len(ranked_set))):
            for j in range(len(keyword_faiss)):
                index_path = os.path.join(r"D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Keywords", keyword_faiss[j])
                metadata_path = os.path.join(r"D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Keywords", keyword_metadata[j])
                index = faiss.read_index(index_path)
                with open(metadata_path, "rb") as f:
                    metadata = pickle.load(f)
                keyword_embedding = np.array(ranked_set[i][0], dtype="float32").reshape(1, -1)
                D, I = index.search(keyword_embedding, 1)
                keyword_score = ranked_set[i][1]
                file_score = metadata[I[0][0]][0]
                distance = D[0][0]
                score = keyword_score + file_score - distance
                file_path = metadata[I[0][0]][2]
                if file_path in files and files[file_path] < score:
                    files[file_path] = score
                else:
                    files[file_path] = score
        files = {k: v for k, v in sorted(files.items(), key=lambda item: item[1], reverse=True)}
        print(files)
        file_paths = list(files.keys())
        if intent == 'retrieve file':
            return file_paths
        else:
            # Manish's function, input = (file_paths, query)
            pass
    