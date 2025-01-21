import faiss
import torch
import numpy as np
import pickle
from typing import List, Dict, Tuple
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import CrossEncoder
import os

<<<<<<< HEAD

class Retriever():
    def __init__(self):
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        os.environ["GOOGLE_API_KEY"] = "AIzaSyASciVtzGPKxHFbPo344pr0XBo59MYmDno"
        os.environ["GROQ_API_KEY"] = "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"
        logging.getLogger("httpx").setLevel(logging.WARNING)
        genai.configure(api_key="AIzaSyASciVtzGPKxHFbPo344pr0XBo59MYmDno")
        self.llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

    def disable_prints(self,func, *args, **kwargs):
        # Redirect standard output to null
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            result = func(*args, **kwargs)
        finally:
            sys.stdout.close()
            sys.stdout = original_stdout
        return result

    def hyde_query(self,query):
        hyde_prompt = (
            "Given the following query, create a hypothetical answer as if it were correct and complete:\n"
            f"Query: {query}\n\n"
            "Hypothetical Answer:"
        )
        return self.llm.invoke(hyde_prompt)


    def print_response(self,response):
        print('AI:',end=' ')
        response_txt = response["result"]
        for chunk in response_txt.split("\n"):
            if not chunk:
                print()
                continue
            print("\n".join(textwrap.wrap(chunk, 100, break_long_words=False)))

    def retriever(self,faiss_index):
        # Initialize FAISS retriever
        retriever = FAISS(faiss_index).as_retriever(search_kwargs={"k": 10})

        # Set up a FlashRank compressor
        compressor = FlashRankRerank(model="ms-marco-MiniLM-L-12-v2")

        # Create a compression retriever
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=retriever
        )

        # Define the prompt template
        prompt_template = """
        You are Lexora, a AI powered database manager.
        Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}
        Question: {question}

        Answer the question and provide additional helpful information,
        based on the pieces of information, if applicable. Be succinct.

        Responses should be properly formatted to be easily read.
=======
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
>>>>>>> 2e473f8c6f98103465bcf0fd3a60a365b3c949a3
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
        chunks=[]

        try:
            # Load indices and chunks
            searcher.load_faiss_files(faiss_files, chunks_files)
            
            # Perform search
            results = searcher.search(query, k=5)
            
            # Print results
            for idx, result in enumerate(results, 1):
                chunks.append(result['chunk'])
                # print(f"\nResult {idx}:")
                # print(f"Chunk: {result['chunk']}")
                # print(f"FAISS Score: {result['faiss_score']:.4f}")
                # print(f"Rerank Score: {result['rerank_score']:.4f}")
            return chunks
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")
