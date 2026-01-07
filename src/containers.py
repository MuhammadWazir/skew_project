from dependency_injector import containers, providers
from src.infrastructure.clients.openai_client import OpenAIClient
from src.infrastructure.clients.qdrant_client import QdrantClientWrapper
from src.application.use_cases.knowledge.file_upload_use_case import FileUploadUseCase
from src.application.use_cases.knowledge.file_delete_use_case import FileDeleteUseCase


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["src.presentation.routers"])

    openai_client = providers.Singleton(OpenAIClient)
    qdrant_client = providers.Singleton(QdrantClientWrapper)
    file_upload_use_case = providers.Factory(FileUploadUseCase, openai_client=openai_client, qdrant_client=qdrant_client)
    file_delete_use_case = providers.Factory(FileDeleteUseCase, qdrant_client=qdrant_client)