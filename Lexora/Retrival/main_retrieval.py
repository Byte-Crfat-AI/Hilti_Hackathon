from Decision import get_intent
import os
import re
def get_lexora_path(path):
    match = re.search(r'^(.*\\Lexora)(?:\\|$)', path)
    if match:
        return match.group(1)
    return None
lexora_path = get_lexora_path(os.getcwd())
keyword_extraction_dir = os.path.join(lexora_path, "Keyword_Extraction")
database_dir = os.path.join(lexora_path, "Database" , "Keywords")
embedding_database_dir = os.path.join(lexora_path, "Database" , "Embeddings")
import sys
sys.path.append(keyword_extraction_dir)
from keyword_ranking import Keyword
import faiss
from Gemini  import RAGSystem
import numpy as np
import pickle
from tqdm import tqdm
import asyncio

class MainRetrieval:
    def __init__(self):
        self.keyword = Keyword()
        self.RAG = RAGSystem()
    def main_retrieval(self, query):
        intent = get_intent(query)
        ranked_set = self.keyword.keyword_main(query)
        keyword_faiss_temp = os.listdir(database_dir)
        keyword_faiss = [keyword_faiss_temp[i] for i in range(len(keyword_faiss_temp)) if keyword_faiss_temp[i][-6:] == ".faiss"]
        keyword_metadata = [f'metadata_{keyword_faiss[i][14:-6]}.pkl' for i in range(len(keyword_faiss))]
        keywords = [ranked_set[i][2] for i in range(len(ranked_set))]
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
        file_paths = list(files.keys())
        if intent == 'retrieve file':
            return file_paths
        else:
            def match_pattern(path):
                folder_name = os.path.basename(os.path.dirname(path))
                file_name = os.path.splitext(os.path.basename(path))[0]
                return f"{folder_name}_{file_name.replace('.', '_')}"
            faiss_files = []
            chunk_files = []
            for i in range(len(file_paths)):
                modified_path = match_pattern(file_paths[i])
                faiss_files.append(os.path.join(embedding_database_dir, f"Embedding_index_{modified_path}.faiss"))
                chunk_files.append(os.path.join(embedding_database_dir, f"metadata_{modified_path}.pkl"))
            return asyncio.run(self.RAG.respond(query,faiss_files, chunk_files))
    