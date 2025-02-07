import torch
import faiss
import torch
import numpy as np
import pickle
from typing import List, Dict, Tuple
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import CrossEncoder
import os
import time

class MC():
    def __init__(self, 
                 tokenizer_name = "NeuML/pubmedbert-base-embeddings"
                 ,model_name = "NeuML/pubmedbert-base-embeddings",
                 reranker_name = 'cross-encoder/ms-marco-MiniLM-L-6-v2',
                 device = "cuda" if torch.cuda.is_available() else "cpu"):
        # Initialize encoder model and tokenizer
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.encoder = AutoModel.from_pretrained(model_name).to(self.device)
        self.encoder.eval()
        
        # Initialize reranker
        self.reranker = CrossEncoder(reranker_name)
        
        # Initialize empty index and chunks storage
        self.combined_index = None
        self.all_chunks = []
        self.dimension = None
        
        # Add debug counters
        self.vectors_per_file = []
        self.chunks_per_file = []
    def load_faiss_files(self, faiss_files, chunks_files):
        """Load and combine multiple FAISS indices and their corresponding chunks from pickle files"""
        if len(faiss_files) != len(chunks_files):
            raise ValueError("Number of FAISS files must match number of chunks files")
        
        # Load all chunks from pickle files
        for chunk_file in chunks_files:
            with open(chunk_file, 'rb') as f:
                chunks = pickle.load(f)
                if isinstance(chunks, list):
                    chunk_count = len(chunks)
                    self.chunks_per_file.append(chunk_count)
                    self.all_chunks.extend(chunks)
                else:
                    raise ValueError(f"Chunks in {chunk_file} must be stored as a list")
        
        # Initialize variables to store all vectors
        all_vectors = []
        
        # Load all indices and collect vectors
        for idx, faiss_file in enumerate(faiss_files):
            index = faiss.read_index(faiss_file)
            
            if idx == 0:
                self.dimension = index.d
            elif index.d != self.dimension:
                raise ValueError(f"Dimension mismatch in index {faiss_file}")
            
            # Extract vectors based on index type
            if hasattr(index, 'reconstruct_n'):
                vectors = index.reconstruct_n(0, index.ntotal)
            else:
                vectors = faiss.vector_float_to_array(index.get_xb()).reshape(index.ntotal, index.d)
            
            vector_count = len(vectors)
            self.vectors_per_file.append(vector_count)
            all_vectors.append(vectors)
        
        # Concatenate all vectors
        combined_vectors = np.vstack(all_vectors)
        
        # Create new index with same dimension
        self.combined_index = faiss.IndexFlatIP(self.dimension)
        
        # Add all vectors to the new index
        self.combined_index.add(combined_vectors)
        
        
        # Verify that number of vectors matches number of chunks
        if self.combined_index.ntotal != len(self.all_chunks):
            raise ValueError(f"Mismatch between number of vectors ({self.combined_index.ntotal}) "
                            f"and number of chunks ({len(self.all_chunks)}). "
                            f"Please check that your FAISS indices and chunk files correspond correctly.")


import os

# Folder path (change it to your folder path)
folder_path = "/workspace/Hilti_Hackathon/Lexora/Database/Embeddings"

embedding_files = []
metadata_files = []

# Iterate through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith("Embedding_index_Others"):
        embedding_files.append(os.path.join("/workspace/Hilti_Hackathon/Lexora/Database/Embeddings",file_name))
    elif file_name.startswith("metadata_Others"):
        metadata_files.append(os.path.join("/workspace/Hilti_Hackathon/Lexora/Database/Embeddings",file_name))

# Print the results
print("Embedding Files:", embedding_files)
print("Metadata Files:", metadata_files)

mc=MC()
mc.load_faiss_files(embedding_files,metadata_files)