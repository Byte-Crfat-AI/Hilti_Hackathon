from transformers import AutoTokenizer, AutoModel
import torch

class Embeddings:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  
        self.model = AutoModel.from_pretrained("bert-base-uncased")

    def chunk_text(self, text, max_length=512, overlap=100):
        words = text.split()  
        chunks = []
        chunks_returned = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i : i + max_length - overlap])  
            tokenized_chunk = self.tokenizer.encode(chunk, add_special_tokens=True, truncation=True, max_length=max_length)
            chunks.append(tokenized_chunk)
            chunks_returned.append(chunk)
            i += max_length - overlap  
        return chunks, chunks_returned

    def get_embeddings(self, text):
        chunks , chunks_returned = self.chunk_text(text)
        embeddings = []
        for chunk in chunks:
            inputs = torch.tensor([chunk])  
            with torch.no_grad():
                outputs = self.model(inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :]  
            embeddings.append(cls_embedding.squeeze(0))
        return torch.stack(embeddings).cpu().numpy(), chunks_returned
