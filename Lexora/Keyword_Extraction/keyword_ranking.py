from keybert import KeyBERT
from transformers.pipelines import pipeline
from keyphrase_vectorizers import KeyphraseCountVectorizer
from transformers import AutoTokenizer, AutoModel
import torch

# For a single file
class Keyword:
    def __init__(self):
        self.hf_model = pipeline("feature-extraction", model="google-bert/bert-base-uncased")
        self.tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
        self.model = AutoModel.from_pretrained("google-bert/bert-base-uncased")
    def get_keywords(self,text):
        vectorizer = KeyphraseCountVectorizer()
        kw_model = KeyBERT(model=self.hf_model)
        keywords = kw_model.extract_keywords(text, vectorizer=vectorizer, use_mmr=True)
        rank = [word[1] for word in keywords]
        return [word[0] for word in keywords], rank

    def keyword_main(self,text):
        keywords, rank = self.get_keywords(text)
        inputs = self.tokenizer(keywords, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        token_embeddings = outputs.last_hidden_state
        sentence_embeddings = torch.mean(token_embeddings, dim=1)
        ranked_set = []
        for i in range(len(rank)):
            ranked_set.append([sentence_embeddings[i],rank[i],keywords[i]])
        return ranked_set

#Example
# keyword_class = Keyword()
# text = "The history of natural language processing (NLP) generally started in the 1950s, although work can be found from earlier periods."
# print(keyword_class.keyword_main(text))


    
    
    

