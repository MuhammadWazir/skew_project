from src.domain.abstractions.clients.abstract_openai_client import AbstractOpenAIClient
from src.domain.abstractions.clients.abstract_qdrant_client import AbstractQdrantClient
from src.domain.exceptions.application_exception import ApplicationException
from src.domain.exceptions.system_exception import SystemException
from src.application.dtos.search_chunk_dto import SearchChunkDTO
from src.application.dtos.chunk_data_dto import ChunkDataDTO

class SearchChunksUseCase:
    def __init__(self, qdrant_client= AbstractQdrantClient, openai_client = AbstractOpenAIClient):
        self.qdrant_client = qdrant_client
        self.openai_client = openai_client
    
    def execute(self, request: SearchChunkDTO):
        try:
            query_embeddings = self.openai_client.generate_embedding([request.query])
            results = self.qdrant_client.search_chunks(query_embeddings[0])
            return [ChunkDataDTO.model_validate(result.model_dump()) for result in results]
        except Exception as e:
            raise e