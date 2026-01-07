from typing import Dict, Any
from src.domain.abstractions.nodes.abstract_node import AbstractNode
from src.domain.abstractions.clients.abstract_openai_client import AbstractOpenAIClient
from src.infrastructure.config.constants import CHAT_RESPONSE_PROMPT
from src.domain.exceptions.system_exception import SystemException


class ChatResponseGenerationNode(AbstractNode):
    def __init__(self, openai_client: AbstractOpenAIClient):
        self.openai_client = openai_client
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:            
            user_query = state.get("user_query", "")
            retrieved_chunks = state.get("retrieved_chunks", [])
            needs_rag = state.get("needs_rag", False)
            
            
            if needs_rag and retrieved_chunks:
                context_parts = []
                for idx, chunk in enumerate(retrieved_chunks):
                    context_parts.append(f"[Source: {chunk.filename}]\n{chunk.text}")
                context = "\n\n".join(context_parts)
                context_section = f"Context from knowledge base:\n{context}"
            else:
                context_section = ""
            
            prompt = CHAT_RESPONSE_PROMPT.format(
                context_section=context_section
            )
            
            response = self.openai_client.client.chat.completions.create(
                model=self.openai_client.chat_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_query}
                ],
                max_completion_tokens=1000
            )
            
            generated_response = response.choices[0].message.content
            
            if generated_response:
                generated_response = generated_response.strip()
            else:
                generated_response = "I apologize, but I couldn't generate a response. Please try again."
            
            return {"response": generated_response}
            
        except Exception as e:
            raise SystemException(f"Error generating response: {str(e)}")