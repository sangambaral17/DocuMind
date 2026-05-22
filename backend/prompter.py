def compose_rag_prompt(query: str, retrieved_chunks: list[dict]) -> tuple[str, str]:
    """
    Composes the system prompt and user prompt for Retrieval-Augmented Generation.
    
    Args:
        query (str): The user's query.
        retrieved_chunks (list[dict]): List of retrieved chunk dictionaries -> [{"page": int, "text": str}]
        
    Returns:
        tuple[str, str]: (system_prompt, user_prompt)
    """
    system_prompt = (
        "You are DocuMind, an advanced document intelligence assistant.\n"
        "Your goal is to answer the user's question using ONLY the provided document chunks.\n"
        "Follow these strict rules:\n"
        "1. Base your answer strictly on the provided context. Do NOT use outside knowledge.\n"
        "2. If the context does not contain the answer, say exactly: 'Not found in document.'\n"
        "3. Keep your answer factual, direct, and concise.\n"
        "4. Do not speculate or extrapolate beyond what is explicitly written."
    )
    
    context_blocks = []
    for idx, chunk in enumerate(retrieved_chunks):
        block = (
            f"--- Context Segment {idx + 1} (Source: Page {chunk['page']}) ---\n"
            f"{chunk['text']}"
        )
        context_blocks.append(block)
        
    context_str = "\n\n".join(context_blocks)
    
    user_prompt = (
        f"Here is the context from the document:\n\n"
        f"{context_str}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )
    
    return system_prompt, user_prompt
