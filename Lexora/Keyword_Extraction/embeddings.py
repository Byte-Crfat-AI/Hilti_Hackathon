from transformers import AutoTokenizer, AutoModel
import torch

class Embeddings:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("NeuML/pubmedbert-base-embeddings")
        self.model = AutoModel.from_pretrained("NeuML/pubmedbert-base-embeddings")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
    def chunk_text(self, text, max_length=512, overlap=50):
        """
        Chunk text into smaller pieces with overlap, ensuring proper tokenization.
        
        Args:
            text (str): Input text to chunk
            max_length (int): Maximum token length for each chunk
            overlap (int): Number of overlapping tokens between chunks
            
        Returns:
            tuple: (tokenized_chunks, original_chunks)
        """
        # Pre-tokenize the entire text
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        chunks_text = []
        
        # Create chunks based on tokens rather than words
        start_idx = 0
        while start_idx < len(tokens):
            # Calculate end index accounting for [CLS] and [SEP] tokens
            end_idx = min(start_idx + max_length - 2, len(tokens))
            
            # Extract chunk tokens
            chunk_tokens = tokens[start_idx:end_idx]
            
            # Add special tokens
            chunk_tokens = [self.tokenizer.cls_token_id] + chunk_tokens + [self.tokenizer.sep_token_id]
            chunks.append(chunk_tokens)
            
            # Decode chunk for reference
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks_text.append(chunk_text)
            
            # Move start index, accounting for overlap
            start_idx += max_length - overlap - 2  # -2 for special tokens
            
        print(f"Created {len(chunks)} chunks from input text")
        return chunks, chunks_text
    
    def get_embeddings(self, text, batch_size=32):
        """
        Get embeddings for text in batches.
        
        Args:
            text (str): Input text
            batch_size (int): Number of chunks to process at once
            
        Returns:
            tuple: (numpy array of embeddings, list of chunk texts)
        """
        chunks, chunks_text = self.chunk_text(text)
        embeddings = []
        
        # Process chunks in batches
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            
            # Pad sequences in batch to same length
            max_len = max(len(chunk) for chunk in batch_chunks)
            padded_chunks = [chunk + [self.tokenizer.pad_token_id] * (max_len - len(chunk)) 
                           for chunk in batch_chunks]
            
            # Create attention mask
            attention_mask = [[1] * len(chunk) + [0] * (max_len - len(chunk)) 
                            for chunk in batch_chunks]
            
            # Convert to tensors
            inputs = torch.tensor(padded_chunks).to(self.device)
            mask = torch.tensor(attention_mask).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(inputs, attention_mask=mask)
                # Get CLS token embeddings
                batch_embeddings = outputs.last_hidden_state[:, 0, :]
                embeddings.append(batch_embeddings.cpu())
        
        # Concatenate all embeddings
        all_embeddings = torch.cat(embeddings, dim=0).numpy()
        print(f"Generated {len(all_embeddings)} embeddings")
        
        assert len(all_embeddings) == len(chunks_text), \
            f"Mismatch between embeddings ({len(all_embeddings)}) and chunks ({len(chunks_text)})"
            
        return all_embeddings, chunks_text