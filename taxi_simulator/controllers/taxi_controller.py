import asyncio
import random
from uuid import UUID, uuid4

from api.schemas.requests import TripAssignment
from api.schemas.response import TripAssignmentResponse
import httpx
from loguru import logger
from models.enums import TripEventType
from models.models import TaxiRegisterNotification, TripEventNotification


class TaxiController:  # we can use state machine pattern too

    def __init__(
        self,
        taxi_id: UUID | None = None,
        position_x: int | None = None,
        position_y: int | None = None,
        network_id: str = "taxi",
        dispatcher_url: str = "http://dispacher:8080",
    ):
        self.taxi_id = taxi_id or uuid4()
        self.position_x = position_x or random.randint(1, 100)
        self.position_y = position_y or random.randint(1, 100)
        self._dispatcher_url = (
            dispatcher_url[:-1] if dispatcher_url.endswith("/") else dispatcher_url
        )
        self._network_id = network_id

    @property
    def dispatcher_url(self) -> str:
        return self._dispatcher_url

    @dispatcher_url.setter
    def dispatcher_url(self, value: str) -> None:
        self._dispatcher_url = (
            value[:-1] if value.endswith("/") else value
        )

    @property
    def network_id(self) -> str:
        return self._network_id

    @network_id.setter
    def network_id(self, value: str) -> None:
        self._network_id = value

    def register_taxi(self) -> None:
        #  todo can add one retry on fail
        logger.info("Registering taxi in the dispatcher service")
        notification = TaxiRegisterNotification(
            id=self.taxi_id, network_id=self.network_id, x=self.position_x, y=self.position_y
        )
        try:
            resp = httpx.post(
                f"{self.dispatcher_url}/api/v1/taxi/register",
                content=notification.model_dump_json(),
                timeout=30.0,
            )
            resp.raise_for_status()
            logger.info("Registered with dispatcher")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Error during dispatcher register {e.response.status_code}: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"Failed to register: {e}")

    async def unregister_taxi(self) -> None:
        try:
            resp = await httpx.AsyncClient().patch(
                f"{self.dispatcher_url}/api/v1/taxi/unregister",
                json={"id": str(self.taxi_id)},
                timeout=10.0,
            )
            resp.raise_for_status()
            logger.info("Unregistered with dispatcher")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Error during dispatcher unregister {e.response.status_code}: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"Failed to unregister: {e}")

    async def notify_dispatcher(self, action: TripEventType, trip_id: UUID) -> None:
        url = f"{self.dispatcher_url}/api/v1/trip/{action}"
        payload = TripEventNotification(taxi_id=self.taxi_id, trip_id=trip_id)
        try:
            resp = await httpx.AsyncClient().post(
                url, content=payload.model_dump_json(), timeout=10.0
            )
            resp.raise_for_status()
            logger.info(f"Notified dispatcher of {action}")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Error during dispatcher notification {e.response.status_code}: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"Failed to notify dispatcher: {e}")

    async def handle_trip_request(self, trip: TripAssignment) -> TripAssignmentResponse:
        pickup_distance = abs(trip.pickup_x - self.position_x) + abs(
            trip.pickup_y - self.position_y
        )
        pickup_time = sum(random.randint(1, 3) for _ in range(pickup_distance))
        logger.info(f"Driving to pick-up (simulated {pickup_time} min)...")
        await asyncio.sleep(pickup_time)  # 1s = 1 min
        await self.notify_dispatcher(TripEventType.pick_up, trip.id)
        self.position_x = trip.pickup_x
        self.position_y = trip.pickup_y

        dropoff_distance = abs(trip.dropoff_x - self.position_x) + abs(
            trip.dropoff_y - self.position_y
        )
        travel_time = sum(random.randint(1, 3) for _ in range(dropoff_distance))
        logger.info(f"Driving to drop-off (simulated {travel_time} min)...")
        await asyncio.sleep(travel_time)
        await self.notify_dispatcher(TripEventType.drop_off, trip.id)
        self.position_x = trip.dropoff_x
        self.position_y = trip.dropoff_y

        logger.info("Trip completed, taxi available again")


taxi_controller = TaxiController()
