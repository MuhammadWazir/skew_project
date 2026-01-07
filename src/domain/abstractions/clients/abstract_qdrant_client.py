from abc import ABC, abstractmethod
from typing import List, Dict, Optional
class AbstractQdrantClient(ABC):
    @abstractmethod
    def ensure_collection(self, collection_name: str, vector_size: int = 1536, distance: str = "Cosine"):
        pass

    @abstractmethod
    def upload(self, collection_name: str, embeddings: List[List[float]], metadatas: List[Dict], ids: Optional[List[str]] = None, vector_size: Optional[int] = None):
        pass

    @abstractmethod
    def search_chunks(self, query_embedding: list, top_k: int = 5, collections: Optional[List[str]] = None):
        pass

    @abstractmethod
    def delete_pdf_collection(self, collection_name: str):
        pass