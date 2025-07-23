from typing import Any

from fastapi import APIRouter
from api.schemas.requests import TaxiRegisterRequest
from api.schemas.response import TaxiRegisterResponse
from loguru import logger
from uuid import uuid4
router = APIRouter()


@router.get("/taxi")
def health_check() -> dict[str, Any]:
    logger.debug("taxi list")
    return {"taxi_id": uuid4()}


@router.post("/register_taxi", response_model=TaxiRegisterResponse)
def register_taxi(payload: TaxiRegisterRequest) -> dict[str, Any]:
    logger.debug("register taxi")
    return {"status": "registered", "taxi_id": uuid4()}
