# PDF Parsing module
import fitz  # PyMuPDF

def parse_pdf(file_path: str) -> list[dict]:
    """
    Parses a PDF file and extracts text page-by-page.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        list[dict]: A list of dicts, each containing:
                    - "page": Page number (1-indexed)
                    - "text": Cleaned raw text of the page
    """
    doc = fitz.open(file_path)
    pages_data = []
    
    for i, page in enumerate(doc):
        # Extract text using standard layout grouping
        text = page.get_text("text")
        
        # Keep clean, strip excessive whitespaces
        cleaned_text = " ".join(text.split())
        
        pages_data.append({
            "page": i + 1,  # 1-indexed for user display
            "text": cleaned_text
        })
        
    return pages_data
