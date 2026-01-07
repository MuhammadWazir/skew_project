from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractNode(ABC):
    
    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass

