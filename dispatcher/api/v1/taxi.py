from api.schemas.requests import TaxiRegisterRequest, TaxiUnregisterRequest
from api.schemas.response import TaxiRegisterResponse, TaxiResponse
from fastapi import APIRouter
from loguru import logger
from models.dto_models import TaxiDTO
from services.taxi_service import taxi_service


router = APIRouter()


@router.get("/available")
def fetch_available_taxis() -> list[TaxiResponse]:
    logger.debug("taxis list")
    taxi_dtos: list[TaxiDTO] = taxi_service.find_available_taxis()
    return [TaxiResponse(**t.model_dump()) for t in taxi_dtos]


# todo optional - add taxi by id


@router.post("/register", response_model=TaxiRegisterResponse)
def register_taxi(payload: TaxiRegisterRequest) -> TaxiRegisterResponse:
    logger.debug(f"register taxi  - payload: {payload}")
    return taxi_service.register_taxi(payload)


@router.patch("/unregister", response_model=TaxiRegisterResponse)
def unregister_taxi(payload: TaxiUnregisterRequest) -> TaxiRegisterResponse:
    logger.debug(f"unregister taxi - payload: {payload}")
    return taxi_service.unregister_taxi(payload)
