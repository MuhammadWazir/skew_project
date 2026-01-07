from abc import ABC, abstractmethod
from typing import List

class AbstractOpenAIClient(ABC):
    @abstractmethod
    def generate_embedding(self, texts: List[str]) -> List[List[float]]:
        pass