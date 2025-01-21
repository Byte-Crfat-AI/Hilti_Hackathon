from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from transformers import AutoTokenizer, AutoModel
import torch


class Keyword:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
        self.model = AutoModel.from_pretrained("google-bert/bert-base-uncased")
        self.kw_model = KeyBERT(model=self.model)

    def get_keywords(self, text):
        vectorizer = KeyphraseCountVectorizer()
        keywords = self.kw_model.extract_keywords(text, vectorizer=vectorizer, use_mmr=True)
        rank = [word[1] for word in keywords]
        return [word[0] for word in keywords], rank

    def keyword_main(self, text):
        keywords, rank = self.get_keywords(text)
        inputs = self.tokenizer(keywords, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        token_embeddings = outputs.last_hidden_state
        sentence_embeddings = torch.mean(token_embeddings, dim=1)
        ranked_set = [[sentence_embeddings[i], rank[i], keywords[i]]y for i in range(len(rank))]
        return ranked_set
