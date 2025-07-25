from typing import Any
from uuid import uuid4

from api.schemas.requests import ClientRequest
from api.schemas.response import ClientResponse
from fastapi import APIRouter
from loguru import logger


router = APIRouter()


@router.post("/client_request", response_model=ClientResponse)
def register_taxi(payload: ClientRequest) -> dict[str, Any]:
    logger.debug("client request")
    return {"status": "registered", "client_id": uuid4()}
