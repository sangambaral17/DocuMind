# Text chunking module
def chunk_pages(pages_data: list[dict], chunk_size: int = 200, overlap: int = 50) -> list[dict]:
    """
    Splits page-by-page text into overlapping chunks, maintaining page mapping.
    
    Args:
        pages_data (list[dict]): List of dictionaries from parse_pdf -> [{"page": int, "text": str}]
        chunk_size (int): Target number of words per chunk.
        overlap (int): Number of overlapping words between adjacent chunks.
        
    Returns:
        list[dict]: List of chunks -> [{"chunk_id": int, "page": int, "text": str}]
    """
    chunks = []
    chunk_id = 0
    
    for page_info in pages_data:
        page_num = page_info["page"]
        text = page_info["text"]
        
        words = text.split()
        num_words = len(words)
        
        # If the page is shorter than chunk_size, keep it as a single chunk
        if num_words <= chunk_size:
            if num_words > 0:  # Skip completely empty pages
                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_num,
                    "text": text
                })
                chunk_id += 1
            continue
            
        # Sliding window over the words of the page
        start = 0
        while start < num_words:
            end = start + chunk_size
            chunk_words = words[start:end]
            
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "chunk_id": chunk_id,
                "page": page_num,
                "text": chunk_text
            })
            chunk_id += 1
            
            # Slide the window forward by chunk_size - overlap
            start += (chunk_size - overlap)
            
            # Break if we've processed all words and the next slide is out of bounds
            if start >= num_words:
                break
                
            # If the remaining words are fewer than the overlap, stop to avoid tiny chunks
            if num_words - start < overlap:
                break
                
    return chunks
