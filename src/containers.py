from dependency_injector import containers, providers
from src.infrastructure.clients.openai_client import OpenAIClient
from src.infrastructure.clients.qdrant_client import QdrantClientWrapper
from src.application.use_cases.knowledge.file_upload_use_case import FileUploadUseCase
from src.application.use_cases.knowledge.file_delete_use_case import FileDeleteUseCase
from src.application.use_cases.knowledge.search_chunks_use_case import SearchChunksUseCase
from src.application.use_cases.chat.chat_use_case import ChatUseCase
from src.domain.nodes.brain_node import BrainNode
from src.domain.nodes.rag_node import RAGNode
from src.domain.nodes.chat_response_generation_node import ChatResponseGenerationNode
from src.application.graph.chat_graph import ChatGraph

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["src.presentation.routers"])

    openai_client = providers.Singleton(OpenAIClient)
    qdrant_client = providers.Singleton(QdrantClientWrapper)
    brain_node = providers.Factory(BrainNode, openai_client=openai_client)
    rag_node = providers.Factory(RAGNode, openai_client=openai_client, qdrant_client = qdrant_client)
    chat_response_node = providers.Factory(ChatResponseGenerationNode, openai_client=openai_client)
    chat_graph = providers.Factory(
        ChatGraph,
        brain_node=brain_node,
        rag_node=rag_node,
        chat_response_node=chat_response_node
    )
    file_upload_use_case = providers.Factory(FileUploadUseCase, openai_client=openai_client, qdrant_client=qdrant_client)
    file_delete_use_case = providers.Factory(FileDeleteUseCase, qdrant_client=qdrant_client)
    search_chunks_use_case = providers.Factory(SearchChunksUseCase, qdrant_client=qdrant_client, openai_client=openai_client)
    chat_use_case = providers.Factory(ChatUseCase, chat_graph=chat_graph)