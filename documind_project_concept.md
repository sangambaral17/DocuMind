# DocuMind — AI Document Intelligence Platform
> **Your portfolio project. Built free. Sellable as SaaS.**

---

## What is it?

DocuMind lets users upload any document (PDF, contract, resume, research paper) and:
- **Chat with it** — ask questions, get answers with source highlights
- **Auto-summarize** — executive summary in one click
- **Detect anomalies** — flags missing clauses, risky terms, inconsistencies
- **Explain its reasoning** — shows *which* part of the document led to each answer (whitebox)
- **Compare documents** — "How does Contract A differ from Contract B?"

The unique twist: a **Free LLM Router** that automatically selects the best available free model (Groq, Gemini Free, Together AI, Hugging Face) based on task type and latency. Zero paid API costs to run.

---

## Who buys this?

| Buyer | Pain | Willingness to Pay |
|---|---|---|
| Freelance lawyers | Review contracts manually | High |
| HR teams | Screen resumes at scale | High |
| Researchers | Read 50+ papers per project | Medium |
| Small businesses | Understand vendor agreements | Medium |
| Students | Digest long academic PDFs | Low (freemium) |

**Monetization path:** Freemium SaaS — 3 docs/month free, $9/month Pro (unlimited), $29/month Team.

---

## Tech Stack (100% Free)

| Layer | Tool | Cost |
|---|---|---|
| Notebook / Dev | Google Colab | Free |
| Backend | FastAPI (Python) | Free |
| Frontend | React + Tailwind | Free |
| Embeddings | `sentence-transformers` (local) | Free |
| Vector DB | FAISS (in-memory) or ChromaDB | Free |
| LLM — fast tasks | Groq API (Llama 3, free tier) | Free |
| LLM — reasoning | Google Gemini 1.5 Flash (free tier) | Free |
| LLM — fallback | Together AI / HuggingFace Inference | Free |
| Deployment | Railway / Render free tier | Free |
| File storage | Supabase free tier | Free |

---

## The Free LLM Router (Your Unique Feature)

This is what makes DocuMind different from every other RAG demo on GitHub.

```
User query comes in
        ↓
Router checks: What type of task is this?
        ↓
┌──────────────────────────────────────────────┐
│  Short Q&A / fast answer  → Groq (Llama 3)   │
│  Summarization / long doc → Gemini Flash     │
│  Code in document         → Together AI      │
│  All fail / rate limited  → HuggingFace      │
└──────────────────────────────────────────────┘
        ↓
Best response returned + model used is shown to user
```

In the UI, users see a small badge: `Answered by: Llama 3 via Groq`
This is honest, educational, and demonstrates you understand the LLM ecosystem.

---

## AI Concepts You Learn (Whitebox vs Blackbox)

### Blackbox concepts (you use these as APIs)
- **LLM inference** — you call the API, tokens go in, tokens come out. You don't see weights.
- **Tokenization** — text is broken into tokens before the model sees it. You observe this.
- **Temperature / sampling** — controls randomness. You set it, you don't implement it.

### Whitebox concepts (you build these yourself)
- **Text chunking** — splitting documents into overlapping 512-token windows. You write this.
- **Embeddings** — converting chunks to 768-dim vectors using `sentence-transformers`. You see the math.
- **Cosine similarity** — how "close" two vectors are. You compute this: `dot(a,b) / (|a| * |b|)`.
- **RAG (Retrieval-Augmented Generation)** — retrieve top-3 relevant chunks, inject into prompt. You build this pipeline.
- **Prompt engineering** — the system prompt you write controls everything. Fully visible.
- **Confidence scoring** — you compare embedding similarity scores to estimate answer certainty.
- **Source attribution** — you track which chunk each answer came from. Fully whitebox.
- **Hallucination detection** — cross-check: does the answer actually appear in retrieved chunks?

---

## Build Phases

### Phase 1 — Core RAG (Week 1-2)
**Goal:** Upload a PDF, ask a question, get an answer with source.

```
Tasks:
- [ ] PDF parser with PyMuPDF (extract raw text)
- [ ] Text chunker (512 tokens, 50-token overlap)
- [ ] Embed chunks with sentence-transformers (all-MiniLM-L6-v2)
- [ ] Store embeddings in FAISS index
- [ ] On query: embed question, cosine search top-3 chunks
- [ ] Build prompt: system + context chunks + user question
- [ ] Call Groq API (free), return answer
- [ ] Show which chunks were used (source highlighting)
```

**You can demo this to an interviewer after week 2.**

---

### Phase 2 — Whitebox Explainability (Week 3)
**Goal:** Show the reasoning, not just the answer.

```
Tasks:
- [ ] Similarity score display (0.0–1.0 per retrieved chunk)
- [ ] Highlight exact sentence in PDF that grounded the answer
- [ ] Confidence badge: High / Medium / Low based on top similarity score
- [ ] "Why this answer?" panel — shows prompt that was sent to LLM
- [ ] Token count display (teaches users about context windows)
```

---

### Phase 3 — Free LLM Router (Week 4)
**Goal:** Never hit a rate limit. Always use the best free model.

```
Tasks:
- [ ] Router class with model registry (Groq, Gemini, Together, HF)
- [ ] Task classifier: summarize / QA / extract / compare
- [ ] Rate limit tracker per provider (resets hourly)
- [ ] Fallback chain: try model 1 → if fail → model 2 → model 3
- [ ] Show user which model answered (transparency badge)
- [ ] Latency logger (build intuition for model speed differences)
```

---

### Phase 4 — Agentic Features (Week 5-6)
**Goal:** Multi-step tasks the user didn't have to break down themselves.

```
Tasks:
- [ ] "Compare two documents" — agent breaks into: extract A, extract B, diff, summarize
- [ ] "Find all dates and deadlines" — structured extraction with JSON output
- [ ] "Red flag detector" — scan contract for risky clauses using a checklist prompt
- [ ] Memory: remember what the user asked earlier in the session
- [ ] Multi-doc index: ask questions across 5 documents at once
```

---

### Phase 5 — Evaluation + Polish (Week 7-8)
**Goal:** Prove it works. Make it sellable.

```
Tasks:
- [ ] RAGAS eval: faithfulness + answer relevancy scores per query
- [ ] Hallucination rate dashboard (% of answers not grounded in doc)
- [ ] User feedback thumbs up/down → logged to Supabase
- [ ] Landing page with waitlist (Vercel free)
- [ ] 3 pricing tiers defined (free / pro / team)
- [ ] README with architecture diagram
```

---

## File Structure

```
documind/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── parser.py            # PDF → raw text
│   ├── chunker.py           # Text → chunks
│   ├── embedder.py          # Chunks → vectors
│   ├── retriever.py         # Query → top-k chunks
│   ├── router.py            # Free LLM router (your unique piece)
│   ├── prompter.py          # Build prompts
│   ├── evaluator.py         # RAGAS + hallucination check
│   └── models/
│       ├── groq_model.py
│       ├── gemini_model.py
│       └── together_model.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── UploadPanel.jsx
│   │   ├── ChatPanel.jsx
│   │   ├── SourceHighlight.jsx  # The whitebox UI
│   │   └── ConfidenceBadge.jsx
├── notebooks/
│   └── DocuMind_Colab.ipynb     # Start here on Google Colab
├── requirements.txt
└── README.md
```

---

## Start Right Now on Google Colab

Paste this into a Colab cell to get the core pipeline running in 10 minutes:

```python
# Cell 1 — Install
!pip install pymupdf sentence-transformers faiss-cpu groq -q

# Cell 2 — Parse + chunk
import fitz  # PyMuPDF

def parse_pdf(path):
    doc = fitz.open(path)
    return " ".join(page.get_text() for page in doc)

def chunk_text(text, size=512, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunks.append(" ".join(words[i:i+size]))
    return chunks

# Cell 3 — Embed + index
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_index(chunks):
    embeddings = model.encode(chunks, show_progress_bar=True)
    index = faiss.IndexFlatIP(embeddings.shape[1])  # Inner product = cosine on normalized
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    return index, embeddings

# Cell 4 — Retrieve
def retrieve(query, chunks, index, top_k=3):
    q_emb = model.encode([query])
    faiss.normalize_L2(q_emb)
    scores, indices = index.search(q_emb, top_k)
    return [(chunks[i], float(scores[0][j])) for j, i in enumerate(indices[0])]

# Cell 5 — Answer with Groq (free)
from groq import Groq
client = Groq(api_key="YOUR_GROQ_API_KEY")  # Free at console.groq.com

def answer(query, retrieved_chunks):
    context = "\n\n".join([c for c, _ in retrieved_chunks])
    prompt = f"""Answer based ONLY on the context below.
If the answer is not in the context, say "Not found in document."

Context:
{context}

Question: {query}"""
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Cell 6 — Run it
text = parse_pdf("/content/your_document.pdf")
chunks = chunk_text(text)
index, _ = build_index(chunks)

query = "What are the payment terms?"
results = retrieve(query, chunks, index)
print("Sources used:")
for chunk, score in results:
    print(f"  Score: {score:.3f} | {chunk[:100]}...")
print("\nAnswer:", answer(query, results))
```

---

## What to Say in Your Portfolio / Interview

> "DocuMind is a document intelligence platform I built from scratch. The core is a RAG pipeline — I wrote the chunker, the embedding layer using sentence-transformers, and the FAISS retrieval myself, so I understand exactly what's happening mathematically. The LLM call is a blackbox — I treat it as a reasoning API. But everything around it is whitebox: I show users the source chunks, similarity scores, and a confidence rating for every answer. The unique feature is the free LLM router — it automatically selects the best free model (Groq, Gemini, Together AI) based on task type and rate limit availability. I evaluated the system using RAGAS and added a hallucination detector that flags answers not grounded in the document. The product is designed to sell as SaaS at $9/month Pro tier."

---

## How to Make it Sellable

1. **Niche it down first.** "AI for contracts" sells faster than "AI for any document."
2. **Waitlist before you finish.** Put up a one-page site at week 2, not week 8.
3. **The router is your moat.** No competitor shows users which model answered and why.
4. **GDPR angle.** Since embeddings run locally and docs never leave the user's session, you can market to European businesses who are scared of sending contracts to OpenAI.
5. **White-label.** Law firms will pay $200-500/month for a branded version.

---

*Built with: Python · FastAPI · React · FAISS · sentence-transformers · Groq · Gemini · Together AI*
*Total infrastructure cost to run: $0/month (free tiers)*
