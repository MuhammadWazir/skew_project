from fastapi import APIRouter, Request
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from src.containers import Container
from src.application.dtos.chat_request_dto import ChatRequestDTO
from src.application.dtos.chat_response_dto import ChatResponseDTO
from src.application.use_cases.chat.chat_use_case import ChatUseCase


chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("", response_model=ChatResponseDTO)
@inject
async def chat(
    request: ChatRequestDTO,
    http_request: Request,
    chat_use_case: "ChatUseCase" = Depends(Provide[Container.chat_use_case])
):
    return await chat_use_case.execute(request)

