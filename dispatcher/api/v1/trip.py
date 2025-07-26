from api.schemas.requests import ClientRequest, DropoffNotification, PickupNotification
from api.schemas.response import ClientRequestResponse, TripResponse
from fastapi import APIRouter
from loguru import logger
from models.dto_models import TripDTO
from services.trip_service import trip_service


router = APIRouter()


@router.post("/request", response_model=ClientRequestResponse)
def request_trip(payload: ClientRequest) -> ClientRequestResponse:
    logger.debug(f"client {payload.user_id} requested trip")
    return trip_service.assign_trip(payload)


@router.get("/list")
def trips() -> list[TripResponse]:
    logger.debug("trip list")
    trip_dtos: list[TripDTO] = trip_service.trip_list()
    return [TripResponse(**t.model_dump()) for t in trip_dtos]


@router.post("/pick-up", response_model=TripResponse)
def pick_up(payload: PickupNotification) -> TripResponse:
    logger.debug(f"taxi {payload.taxi_id} requested pick-up")
    return trip_service.update_trip_metadata(payload)


@router.post("/drop-off", response_model=TripResponse)
def drop_off(payload: DropoffNotification) -> TripResponse:
    logger.debug(f"taxi {payload.taxi_id} requested dropoff")
    return trip_service.update_trip_metadata(payload)
