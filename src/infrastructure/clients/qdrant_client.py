from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue, VectorParams, Distance
from src.domain.exceptions.application_exception import ApplicationException
from src.domain.exceptions.system_exception import SystemException
from src.infrastructure.config.settings import get_settings
from src.domain.entities.chunk_data_entity import ChunkDataEntity
from src.domain.abstractions.clients.abstract_qdrant_client import AbstractQdrantClient

class QdrantClientWrapper(AbstractQdrantClient):
    def __init__(
        self
    ):
        settings = get_settings()
        self.client = QdrantClient(url=settings.QDRANT_CLUSTER_ENDPOINT, api_key=settings.QDRANT_API_KEY)

    def ensure_collection(self, collection_name: str, vector_size: int = 1536, distance: str = "Cosine"):
        try:
            if not self.client.collection_exists(collection_name=collection_name):
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=distance)
                )
        except Exception as e:
            raise SystemException(f"Error ensuring collection {collection_name}: {str(e)}")

    def upload(
        self,
        collection_name: str,
        embeddings: List[List[float]],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None,
        vector_size: Optional[int] = None
    ): 
        try:
            if not self.client.collection_exists(collection_name=collection_name):
                self.ensure_collection(collection_name, vector_size=vector_size or len(embeddings[0]))

            points = []
            for i, (vec, meta) in enumerate(zip(embeddings, metadatas)):
                point_id = ids[i] if ids else i
                points.append(PointStruct(id=point_id, vector=vec, payload=meta))

            self.client.upsert(collection_name=collection_name, points=points)
            return collection_name
        except Exception as e:
            raise SystemException(f"Error uploading to collection {collection_name}: {str(e)}")

    def search_chunks(
        self,
        query_embedding: list
    ) -> List[ChunkDataEntity]:
        try:
            results = []
            collections_response = self.client.get_collections()
            collection_names = [col.name for col in collections_response.collections]

            for collection_name in collection_names:
                search_results = self.client.query_points(
                    collection_name=collection_name,
                    query=query_embedding,
                    limit=5
                )
                for hit in search_results.points:
                    results.append(ChunkDataEntity(
                        filename=hit.payload.get("filename"),
                        chunk_index=hit.payload.get("chunk_index"),
                        text=hit.payload.get("original_text") or hit.payload.get("text") or "",
                        score=hit.score
                    ))

            results.sort(key=lambda x: x.score, reverse=True)
            return results
        except Exception as e:
            raise SystemException(f"Error searching chunks: {str(e)}")

    def delete_pdf_collection(self, collection_name: str):
        try:
            if self.client.collection_exists(collection_name):
                self.client.delete_collection(collection_name=collection_name)
                return {"success": True, "message": f"Collection {collection_name} deleted."}
            else:
                raise ApplicationException(f"Collection {collection_name} does not exist.")
        except ApplicationException:
            raise
        except Exception as e:
            raise SystemException(f"Error deleting collection {collection_name}: {str(e)}")

