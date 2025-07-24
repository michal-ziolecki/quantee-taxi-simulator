from uuid import UUID

from models.db_models import Taxi, Trip
from models.enums import TaxiStatus
from pydantic import BaseModel


class TaxiDTO(BaseModel):
    id: UUID
    x: int
    y: int
    status: TaxiStatus

    @classmethod
    def from_model(cls, model: Taxi) -> "TaxiDTO":
        return cls(id=model.id, x=model.x, y=model.y, status=model.status)

    def to_model(self) -> Taxi:
        return Taxi(id=self.id, x=self.x, y=self.y, status=self.status)


class TripDTO(BaseModel):
    id: UUID
    taxi_id: UUID
    user_id: UUID

    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int

    waiting_time: int | None = None
    travel_time: int | None = None

    @classmethod
    def from_model(cls, model: Trip) -> "TripDTO":
        return cls(
            id=model.id,
            taxi_id=model.taxi_id,
            user_id=model.user_id,
            pickup_x=model.pickup_x,
            pickup_y=model.pickup_y,
            dropoff_x=model.dropoff_x,
            dropoff_y=model.dropoff_y,
            waiting_time=model.waiting_time,
            travel_time=model.travel_time,
        )

    def to_model(self) -> Trip:
        return Trip(
            id=self.id,
            taxi_id=self.taxi_id,
            user_id=self.user_id,
            pickup_x=self.pickup_x,
            pickup_y=self.pickup_y,
            dropoff_x=self.dropoff_x,
            dropoff_y=self.dropoff_y,
            waiting_time=self.waiting_time,
            travel_time=self.travel_time,
        )
