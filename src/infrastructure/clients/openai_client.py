from typing import List, Optional
from openai import OpenAI
from src.domain.abstractions.clients.abstract_openai_client import AbstractOpenAIClient
from src.infrastructure.config.settings import get_settings
from src.domain.exceptions.system_exception import SystemException
class OpenAIClient(AbstractOpenAIClient):
    def __init__(
        self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.embedding_model = settings.EMBEDDING_MODEL
        self.chat_model = settings.CHAT_MODEL

    def generate_embedding(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            raise SystemException(f"Error generating embeddings")
