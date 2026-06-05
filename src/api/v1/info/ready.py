from asyncio import gather
from fastapi import APIRouter, Request, status
from shared.models.api import ReadyResponse

router = APIRouter()


@router.get("/ready", response_model=ReadyResponse, status_code=status.HTTP_200_OK)
async def ready(request: Request) -> ReadyResponse:
    """Readiness check for api service"""
    return ReadyResponse(API=True)
