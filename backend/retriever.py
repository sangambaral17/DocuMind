import faiss
import numpy as np

class FAISSIndex:
    def __init__(self, dimension: int = 384):
        """
        Initializes an in-memory FAISS IndexFlatIP (Inner Product) index.
        By L2-normalizing vectors before insertion and query, dot product (Inner Product)
        is mathematically equivalent to Cosine Similarity.
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        # Keeps mapping from vector index to original chunk information (e.g. text, page)
        self.chunks_metadata = []

    def add_chunks(self, chunks: list[dict], embeddings: np.ndarray):
        """
        Adds text chunks and their embeddings to the FAISS index.
        
        Args:
            chunks (list[dict]): List of chunk dicts -> [{"chunk_id": int, "page": int, "text": str}]
            embeddings (np.ndarray): 2D numpy array of shape (num_chunks, dimension)
        """
        if len(chunks) == 0:
            return
            
        # Ensure array is float32 and contiguous in memory (required by FAISS)
        embeddings_f32 = np.ascontiguousarray(embeddings, dtype=np.float32)
        
        # Normalize vectors: |v| = 1
        faiss.normalize_L2(embeddings_f32)
        
        # Add embeddings to index
        self.index.add(embeddings_f32)
        
        # Save corresponding metadata
        self.chunks_metadata.extend(chunks)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> list[tuple[dict, float]]:
        """
        Searches the index for the top_k most similar chunks.
        
        Args:
            query_embedding (np.ndarray): 1D or 2D vector for the query.
            top_k (int): Number of nearest neighbors to retrieve.
            
        Returns:
            list[tuple[dict, float]]: List of (chunk_dict, cosine_similarity_score)
        """
        if self.index.ntotal == 0:
            return []
            
        # Reshape query embedding if 1D to 2D
        q_emb = np.ascontiguousarray(query_embedding, dtype=np.float32)
        if len(q_emb.shape) == 1:
            q_emb = np.expand_dims(q_emb, axis=0)
            
        # Normalize query vector so inner product = cosine similarity
        faiss.normalize_L2(q_emb)
        
        # Perform search
        # scores: array of dot products (similarities)
        # indices: array of indices matching elements in self.chunks_metadata
        scores, indices = self.index.search(q_emb, top_k)
        
        results = []
        for rank, idx in enumerate(indices[0]):
            if idx == -1:
                continue  # FAISS returns -1 if index has fewer elements than top_k
            metadata = self.chunks_metadata[idx]
            similarity_score = float(scores[0][rank])
            results.append((metadata, similarity_score))
            
        return results

    def reset(self):
        """Resets the FAISS index and clears all stored chunks metadata."""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.chunks_metadata = []
