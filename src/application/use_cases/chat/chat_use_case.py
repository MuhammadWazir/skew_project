from src.application.dtos.chat_request_dto import ChatRequestDTO
from src.application.dtos.chat_response_dto import ChatResponseDTO
from src.application.graph.chat_graph import ChatGraph
from src.domain.exceptions.system_exception import SystemException


class ChatUseCase:
    def __init__(self, chat_graph: ChatGraph):
        self.chat_graph = chat_graph
    
    async def execute(self, request: ChatRequestDTO) -> ChatResponseDTO:
        try:
            initial_state = {
                "user_query": request.message,
                "needs_rag": None,
                "retrieved_chunks": None,
                "response": None,
                "sources": None
            }
            
            final_state = await self.chat_graph.invoke(initial_state)
            
            response = ChatResponseDTO(
                response=final_state.get("response", "I'm sorry, I couldn't generate a response."),
                sources=final_state.get("sources", []),
                used_rag=final_state.get("needs_rag", False)
            )
            
            return response
            
        except Exception as e:
            raise SystemException(f"Error generating response: {str(e)}")

