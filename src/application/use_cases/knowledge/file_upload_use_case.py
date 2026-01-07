from src.domain.abstractions.clients.abstract_openai_client import AbstractOpenAIClient
from src.domain.abstractions.clients.abstract_qdrant_client import AbstractQdrantClient
from src.domain.exceptions.application_exception import ApplicationException
from src.domain.exceptions.system_exception import SystemException
from src.application.helpers.text_extraction_helper import extract_text
from src.application.helpers.chunking_helper import chunk_text_with_metadata
from src.application.helpers.text_cleaning_helper import clean_pdf_text_for_rag
from src.application.dtos.upload_file_dto import UploadFileDTO
class FileUploadUseCase:
    def __init__(self, openai_client: AbstractOpenAIClient, qdrant_client: AbstractQdrantClient):
        self.openai_client = openai_client
        self.qdrant_client = qdrant_client

    def execute(self, file_data: UploadFileDTO):
        try:
            file_content = extract_text(file_data.file)
            file_content = clean_pdf_text_for_rag(file_content)
            chunks = chunk_text_with_metadata(file_content, file_data.filename)
            embeddings = self.openai_client.generate_embedding([chunk.page_content for chunk in chunks])
            collection_name = self.qdrant_client.upload(file_data.filename, embeddings, [chunk.metadata for chunk in chunks])
            return collection_name
        except Exception as e:
            raise SystemException(f"Error uploading file")