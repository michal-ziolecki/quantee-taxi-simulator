from datetime import datetime

from api.exceptions import NotExistException
from api.schemas.requests import ClientRequest, DropoffNotification, PickupNotification
from api.schemas.response import ClientRequestResponse
import httpx
from loguru import logger
from models.dto_models import TaxiDTO, TripDTO
from models.enums import TaxiStatus, TripRequestStatus
from repository.trip_repository import TripRepository, trip_repo
from services.taxi_service import TaxiService, taxi_service


class TripService:
    def __init__(self, trip_repo: TripRepository, taxi_svc: TaxiService) -> None:
        self.trip_repo = trip_repo
        self.taxi_svc = taxi_svc

    def find_nearest_available_taxi(self, pickup_x: int, pickup_y: int) -> TaxiDTO | None:
        taxis: list[TaxiDTO] = self.taxi_svc.find_available_taxis()

        if not taxis:
            return None

        def distance(t: TaxiDTO) -> int:
            return abs(t.x - pickup_x) + abs(t.y - pickup_y)  # type: ignore

        taxis.sort(key=distance)
        return taxis[0]

    def assign_trip(self, payload: ClientRequest) -> ClientRequestResponse:
        taxi = self.find_nearest_available_taxi(payload.pickup_x, payload.pickup_y)
        if not taxi:
            return ClientRequestResponse(status=TripRequestStatus.no_taxi_available)

        trip_dto = TripDTO(
            taxi_id=taxi.id,
            user_id=payload.user_id,
            pickup_x=payload.pickup_x,
            pickup_y=payload.pickup_y,
            dropoff_x=payload.dropoff_x,
            dropoff_y=payload.dropoff_y,
        )
        # Send assignment to taxi
        try:
            url = f"http://{taxi.network_id}:8080/assign_client"
            httpx.post(url, json=trip_dto.model_dump_json())
        except Exception as e:
            logger.error(f"Error assigning trip to taxi: {e}")
            return ClientRequestResponse(
                status=TripRequestStatus.error_during_assigning, taxi_id=taxi.id
            )

        taxi.status = TaxiStatus.busy
        taxi = self.taxi_svc.update_taxi_status(taxi)
        trip_dto = self.trip_repo.insert(trip_dto)
        return ClientRequestResponse(
            status=TripRequestStatus.taxi_assigned, taxi_id=taxi.id, trip_id=trip_dto.id
        )

    def trip_list(self) -> list[TaxiDTO]:
        return self.trip_repo.get_trips()  # type: ignore

    def update_trip_metadata(self, payload: PickupNotification | DropoffNotification) -> TaxiDTO:
        logger.info(
            f"Taxi {payload.taxi_id} notify about pickup user related to the trip {payload.trip_id}."
        )
        trip: TripDTO = self.trip_repo.get_trip_by_id(trip_id=payload.trip_id)
        if trip is None:
            raise NotExistException(
                message=f"Trip {payload.trip_id} related to"
                f" the Taxi {payload.taxi_id} not exists!"
            )

        if isinstance(payload, PickupNotification):
            trip.pickup_time = datetime.utcnow()
        elif isinstance(payload, DropoffNotification):
            trip.dropoff_time = datetime.utcnow()
        return self.trip_repo.update_trip(dto=trip)


trip_service = TripService(trip_repo=trip_repo, taxi_svc=taxi_service)
