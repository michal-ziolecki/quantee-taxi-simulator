from typing import Any
from uuid import uuid4

from api.schemas.requests import TaxiRegisterRequest, TaxiUnregisterRequest
from api.schemas.response import TaxiRegisterResponse
from fastapi import APIRouter
from loguru import logger
from services.taxi_service import taxi_service


router = APIRouter()


@router.get("/available-taxis")
def fetch_available_taxis() -> dict[str, Any]:
    logger.debug("taxis list")
    return {"taxi_id": uuid4()}


@router.post("/register_taxi", response_model=TaxiRegisterResponse)
def register_taxi(payload: TaxiRegisterRequest) -> TaxiRegisterResponse:
    logger.debug(f"register taxi  - payload: {payload}")
    return taxi_service.register_taxi(payload)


@router.patch("/unregister_taxi", response_model=TaxiRegisterResponse)
def unregister_taxi(payload: TaxiUnregisterRequest) -> TaxiRegisterResponse:
    logger.debug(f"unregister taxi - payload: {payload}")
    return taxi_service.unregister_taxi(payload)
