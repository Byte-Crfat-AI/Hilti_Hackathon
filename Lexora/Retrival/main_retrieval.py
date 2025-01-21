from Decision import get_intent
import os
import re
def get_parent_folder_path(path):
    match = re.match(r'^(.*?\\[^\\]+)\\[^\\]+$', path)
    if match:
        return match.group(1)
    return None
keyword_extraction_dir = os.path.join(get_parent_folder_path(os.getcwd()), "Keyword_Extraction")
database_dir = os.path.join(get_parent_folder_path(os.getcwd()), "Database" , "Keywords")
import sys
sys.path.append(keyword_extraction_dir)
from keyword_ranking import Keyword
import faiss
from Gemini  import RAGSystem
import numpy as np
import pickle
from tqdm import tqdm

class MainRetrieval:
    def __init__(self):
        self.keyword = Keyword()
        self.RAG = RAGSystem()
    def main_retrieval(self, query):
        intent = get_intent(query)
        ranked_set = self.keyword.keyword_main(query)
        keyword_faiss = os.listdir(database_dir)
        keyword_faiss = [keyword_faiss[i] for i in range(len(keyword_faiss)) if keyword_faiss[i][-6:] == ".index"]
        keyword_metadata = [f'metadata_{keyword_faiss[i][14:-6]}.pkl' for i in range(len(keyword_faiss))]
        files = {}
        for i in tqdm(range(len(ranked_set))):
            for j in range(len(keyword_faiss)):
                index_path = os.path.join(database_dir, keyword_faiss[j])
                metadata_path = os.path.join(database_dir, keyword_metadata[j])
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
            faiss_files = None
            chunk_files = None
            return self.RAG.respond(query,faiss_files, chunk_files)
    