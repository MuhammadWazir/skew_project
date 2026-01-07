from typing import Dict, Any
from src.domain.abstractions.nodes.abstract_node import AbstractNode
from src.domain.abstractions.clients.abstract_openai_client import AbstractOpenAIClient
from src.infrastructure.config.constants import BRAIN_PROMPT
from src.domain.exceptions.system_exception import SystemException


class BrainNode(AbstractNode):
    def __init__(self, openai_client: AbstractOpenAIClient):
        self.openai_client = openai_client
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_query = state.get("user_query", "")
            response = self.openai_client.client.chat.completions.create(
                model=self.openai_client.chat_model,
                messages=[
                    {"role": "system", "content": BRAIN_PROMPT},
                    {"role": "user", "content": user_query}
                ],
                max_completion_tokens=100
            )
            decision = response.choices[0].message.content.strip().lower()
            needs_rag = decision == "yes"

            return {"needs_rag": needs_rag}
            
        except Exception as e:
            return {"needs_rag": False}

