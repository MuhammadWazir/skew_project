from io import BytesIO
from typing import List, Dict
import pdfplumber

def extract_text(pdf_content: bytes) -> str:
    pdf_file = BytesIO(pdf_content)
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    
    return text