from transformers import AutoTokenizer, AutoModel
import torch


class Embeddings:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
        self.model = AutoModel.from_pretrained("google-bert/bert-base-uncased")

    def chunk_text(self, text, max_length=512, overlap=100):
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        for i in range(0, len(tokens), max_length - overlap):
            chunk = tokens[i:i + max_length]
            chunks.append(self.tokenizer.decode(chunk))
        return chunks

    def get_embeddings(self, text):
        chunks = self.chunk_text(text)
        embeddings = []
        for chunk in chunks:
            inputs = self.tokenizer(chunk, padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs)
            token_embeddings = outputs.last_hidden_state
            embeddings.append(token_embeddings.squeeze(0))
        return torch.cat(embeddings, dim=0).cpu().numpy(), chunks
