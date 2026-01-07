from src.domain.abstractions.clients.abstract_qdrant_client import AbstractQdrantClient

class FileDeleteUseCase:
    def __init__(self, qdrant_client= AbstractQdrantClient):
        self.qdrant_client = qdrant_client
    
    def execute(self, file_id):
        try:
            self.qdrant_client.delete_pdf_collection(file_id)
            return {"success": True}
        except Exception as e:
            raise e