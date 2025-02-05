import re
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch
from collections import defaultdict

class Keyword:
    def __init__(self ):
        self.tokenizer = AutoTokenizer.from_pretrained("NeuML/pubmedbert-base-embeddings")
        self.model = AutoModel.from_pretrained("NeuML/pubmedbert-base-embeddings")
        self.kw_model = KeyBERT(model=self.model)

    def get_keywords(self, text):
        vectorizer = KeyphraseCountVectorizer()
        keywords = self.kw_model.extract_keywords(text, vectorizer=vectorizer, use_mmr=True)
        rank = [word[1] for word in keywords]
        return [word[0] for word in keywords], rank
    
    def chunk_text(self, text, max_length=512, overlap=100):
        words = text.split()  
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i : i + max_length - overlap])  
            chunks.append(chunk)
            i += max_length - overlap  
        return chunks


    def keyword_main(self, text):
        chunks = self.chunk_text(text)
        keywords_dict = {}
        for j in range(len(chunks)):
            keywords, rank = self.get_keywords(chunks[j])
            for i in range(len(keywords)):
                if keywords[i] not in keywords_dict:
                    keywords_dict[keywords[i]] = rank[i]
                elif keywords_dict[keywords[i]] < rank[i]:
                    keywords_dict[keywords[i]] = rank[i]
        keywords = list(keywords_dict.keys())
        rank = list(keywords_dict.values())
        inputs = self.tokenizer(keywords, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        token_embeddings = outputs.last_hidden_state
        sentence_embeddings = torch.mean(token_embeddings, dim=1)
        ranked_set = [[sentence_embeddings[i], rank[i], keywords[i]] for i in range(len(rank))]
        return ranked_set
