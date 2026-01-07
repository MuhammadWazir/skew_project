from typing import Dict, Any
import httpx
from src.domain.abstractions.nodes.abstract_node import AbstractNode
from src.domain.entities.chunk_data_entity import ChunkDataEntity
from src.domain.exceptions.system_exception import SystemException
from src.domain.abstractions.clients.abstract_qdrant_client import AbstractQdrantClient
from src.domain.abstractions.clients.abstract_openai_client import AbstractOpenAIClient
class RAGNode(AbstractNode):
    def __init__(self, qdrant_client: AbstractQdrantClient, openai_client: AbstractOpenAIClient):
        self.qdrant_client = qdrant_client
        self.openai_client = openai_client
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            query_embedding = self.openai_client.generate_embedding(state.get("user_query", ""))
            chunks_data = self.qdrant_client.search_chunks(query_embedding[0])
            
            # Extract unique sources
            sources = list(set([chunk.filename for chunk in chunks_data]))
            return {
                "retrieved_chunks": chunks_data,
                "sources": sources
            }
            
        except Exception as e:
            return {"retrieved_chunks": [], "sources": []}