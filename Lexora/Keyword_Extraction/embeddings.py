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
            cls_embedding = outputs.last_hidden_state[:, 0, :]  # CLS token embedding
            embeddings.append(cls_embedding.squeeze(0))
        if len(embeddings) != len(chunks):
            raise ValueError(f"Mismatch between number of embeddings ({len(embeddings)}) and chunks ({len(chunks)})")
        return torch.stack(embeddings).cpu().numpy(), chunks