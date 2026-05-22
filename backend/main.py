from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import time

from backend.parser import parse_pdf
from backend.chunker import chunk_pages
from backend.embedder import LocalEmbedder
from backend.retriever import FAISSIndex
from backend.prompter import compose_rag_prompt
from backend.groq_client import GroqClient

app = FastAPI(title="DocuMind - AI Document Intelligence Platform")

# CORS setup to ensure React frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables initialized on startup
embedder = None
vector_store = None
groq_client = None

# Directory to temporarily buffer uploaded files during processing
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
def startup_event():
    global embedder, vector_store, groq_client
    print("----------------------------------------------------------------------")
    print("Loading local embedding model weights... (this may take a few seconds)")
    # Loads all-MiniLM-L6-v2 (384 dimensions)
    embedder = LocalEmbedder()
    
    # Init FAISS Index Flat Inner Product
    vector_store = FAISSIndex(dimension=384)
    
    # Init Groq Client for reasoning
    groq_client = GroqClient()
    print("Pipeline initialization complete. Server is ready!")
    print("----------------------------------------------------------------------")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global embedder, vector_store
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a PDF.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        # Save upload buffer to physical disk temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        start_time = time.time()

        # Step 1: Parse PDF page-by-page
        pages_data = parse_pdf(file_path)

        # Step 2: Split text into overlapping chunks
        chunks = chunk_pages(pages_data, chunk_size=200, overlap=50)

        if not chunks:
            raise HTTPException(status_code=400, detail="This PDF contains no readable text content.")

        # Step 3: Embed chunks locally using sentence-transformers
        chunk_texts = [c["text"] for c in chunks]
        embeddings = embedder.embed_text(chunk_texts)

        # Step 4: Reset the index and store chunks + vectors in FAISS
        vector_store.reset()
        vector_store.add_chunks(chunks, embeddings)

        elapsed = time.time() - start_time

        return {
            "status": "success",
            "filename": file.filename,
            "pages_count": len(pages_data),
            "chunks_count": len(chunks),
            "processing_time_seconds": round(elapsed, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document indexing failed: {str(e)}")
    finally:
        # Housekeeping: delete the temp uploaded PDF file from local storage
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/query")
async def query_document(request: QueryRequest):
    global embedder, vector_store, groq_client
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")

    try:
        # Step 1: Embed the search query
        query_embeddings = embedder.embed_text([request.query])
        if len(query_embeddings) == 0:
            raise HTTPException(status_code=500, detail="Could not encode the query.")
        query_emb = query_embeddings[0]

        # Step 2: Search top-K similar chunks in FAISS
        retrieved_results = vector_store.search(query_emb, top_k=request.top_k)

        if not retrieved_results:
            return {
                "answer": "No documents have been indexed yet. Please upload a PDF first.",
                "sources": []
            }

        # Step 3: Parse chunks and compose prompts
        chunks_only = [chunk for chunk, score in retrieved_results]
        system_prompt, user_prompt = compose_rag_prompt(request.query, chunks_only)

        # Step 4: Invoke LLM reasoning (Groq/Llama 3)
        answer = groq_client.generate_answer(system_prompt, user_prompt)

        # Step 5: Format response payload with source attribution
        sources = [
            {
                "chunk_id": chunk["chunk_id"],
                "page": chunk["page"],
                "text": chunk["text"],
                "similarity_score": round(score, 4)
            }
            for chunk, score in retrieved_results
        ]

        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query resolution failed: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "embedder_loaded": embedder is not None,
        "vector_store_initialized": vector_store is not None,
        "has_groq_key": groq_client.api_key is not None if groq_client else False
    }
