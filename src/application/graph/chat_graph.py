from typing import Dict, Any, Literal, TypedDict
from langgraph.graph import StateGraph, END
from src.domain.abstractions.nodes.abstract_node import AbstractNode


class ChatState(TypedDict, total=False):
    user_query: str
    needs_rag: bool
    retrieved_chunks: list
    sources: list
    response: str


class ChatGraph:
    def __init__(self, brain_node: AbstractNode, rag_node: AbstractNode, chat_response_node: AbstractNode):
        self.brain_node = brain_node
        self.rag_node = rag_node
        self.chat_response_node = chat_response_node
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ChatState)

        # Node wrappers - return only the delta/updates
        def brain_wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
            return self.brain_node.execute(state)
        
        async def rag_wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
            return await self.rag_node.execute(state)
        
        def chat_response_wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
            return self.chat_response_node.execute(state)

        # Add nodes
        workflow.add_node("brain", brain_wrapper)
        workflow.add_node("rag", rag_wrapper)
        workflow.add_node("chat_response", chat_response_wrapper)

        workflow.set_entry_point("brain")

        def should_use_rag(state: Dict[str, Any]) -> Literal["rag", "chat_response"]:
            return "rag" if state.get("needs_rag", False) else "chat_response"

        workflow.add_conditional_edges(
            "brain",
            should_use_rag,
            {"rag": "rag", "chat_response": "chat_response"}
        )

        workflow.add_edge("rag", "chat_response")
        workflow.add_edge("chat_response", END)

        return workflow.compile()

    async def invoke(self, state: Dict[str, Any]):
        return await self.graph.ainvoke(state)
        