from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List

def chunk_text_with_metadata(pdf_text: str, filename: str) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=128
    )
    chunks = splitter.split_text(pdf_text)
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "filename": filename,
                "chunk_index": i,
                "original_text": chunk
            }
        )
        documents.append(doc)
    return documents
