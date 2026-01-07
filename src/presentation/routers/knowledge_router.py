from fastapi import APIRouter
from dependency_injector.wiring import inject, Provide
from fastapi import UploadFile, File, Path, Depends
from src.containers import Container
from src.application.dtos.upload_file_dto import UploadFileDTO
knowledge_router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@knowledge_router.post("/upload")
@inject
def upload_document(
    document: UploadFile = File(...),
    upload_file_use_case: "FileUploadUseCase" = Depends(Provide[Container.file_upload_use_case])
):  
    file_data = UploadFileDTO(filename= document.filename, file= document.file.read())
    return upload_file_use_case.execute(file_data)

@knowledge_router.delete("/files/{file_id}")
@inject
def delete_document(
    file_id: str = Path(..., description="ID of the file to delete"),
    file_delete_use_case: "FileDeleteUseCase" = Depends(Provide[Container.file_delete_use_case])
):
    return file_delete_use_case.execute(file_id)
