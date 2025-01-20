import faiss
import torch
import numpy as np
import pickle
from typing import List, Dict, Tuple
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import CrossEncoder
import os

class FaissSearcher:
    def __init__(self, model_name = "bert-base-uncased", 
                 reranker_name = "cross-encoder/ms-marco-MiniLM-L-6-v2",
                 device = "cuda" if torch.cuda.is_available() else "cpu"):
        # Initialize encoder model and tokenizer
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.encoder = AutoModel.from_pretrained(model_name).to(device)
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
    
    def encode_text(self, text):
        """Encode text using BERT model"""
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors="pt", 
                                  padding=True, truncation=True, 
                                  max_length=512).to(self.device)
            outputs = self.encoder(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        return embeddings
    
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
                    print(f"{chunk_file}: {chunk_count} chunks")
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
        self.combined_index = faiss.IndexFlatL2(self.dimension)
        
        # Add all vectors to the new index
        self.combined_index.add(combined_vectors)
        
        
        # Verify that number of vectors matches number of chunks
        if self.combined_index.ntotal != len(self.all_chunks):
            raise ValueError(f"Mismatch between number of vectors ({self.combined_index.ntotal}) "
                           f"and number of chunks ({len(self.all_chunks)}). "
                           f"Please check that your FAISS indices and chunk files correspond correctly.")
    
    def search(self, query, k = 5, rerank_k = 20):
        """
        Perform similarity search and reranking
        """
        # Encode query
        query_vector = self.encode_text(query)
        
        # Perform initial search with larger k for reranking
        distances, indices = self.combined_index.search(query_vector, rerank_k)
        
        # Prepare candidates for reranking
        candidates = [(self.all_chunks[idx], score) for idx, score in zip(indices[0], distances[0])]
        
        # Prepare pairs for reranking
        rerank_pairs = [[query, chunk] for chunk, _ in candidates]
        
        # Rerank using cross-encoder
        rerank_scores = self.reranker.predict(rerank_pairs)
        
        # Sort by reranker scores
        reranked_results = sorted(zip(candidates, rerank_scores), 
                                key=lambda x: x[1], reverse=True)[:k]
        
        # Format results
        results = []
        for (chunk, faiss_score), rerank_score in reranked_results:
            results.append({
                'chunk': chunk,
                'faiss_score': float(faiss_score),
                'rerank_score': float(rerank_score)
            })
            
        return results

    def return_chunks(self,query,faiss_files,chunks_files):

        # Initialize searcher
        searcher = FaissSearcher()

        try:
            # Load indices and chunks
            searcher.load_faiss_files(faiss_files, chunks_files)
            
            # Perform search
            results = searcher.search(query, k=5)
            
            # Print results
            for idx, result in enumerate(results, 1):
                print(f"\nResult {idx}:")
                print(f"Chunk: {result['chunk']}")
                print(f"FAISS Score: {result['faiss_score']:.4f}")
                print(f"Rerank Score: {result['rerank_score']:.4f}")
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")
