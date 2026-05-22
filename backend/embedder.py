from sentence_transformers import SentenceTransformer
import numpy as np

class LocalEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the local SentenceTransformer model.
        The model will be downloaded automatically on first run and cached.
        """
        # This loads the model (on CPU by default, or GPU if available)
        self.model = SentenceTransformer(model_name)
        
    def embed_text(self, texts: list[str]) -> np.ndarray:
        """
        Generates dense vector embeddings for a list of text strings.
        
        Args:
            texts (list[str]): The text chunks to embed.
            
        Returns:
            np.ndarray: A 2D numpy array of shape (num_texts, embedding_dimension).
                        For all-MiniLM-L6-v2, the embedding dimension is 384.
        """
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
            
        # encode automatically handles batching and tokenization under the hood
        embeddings = self.model.encode(
            texts, 
            show_progress_bar=False, 
            convert_to_numpy=True
        )
        return embeddings
