from datetime import datetime
from uuid import UUID, uuid4

from models.db_models import Taxi, Trip
from models.enums import TaxiStatus
from pydantic import BaseModel, Field


class TaxiDTO(BaseModel):

    id: UUID
    network_id: str
    x: int
    y: int
    status: TaxiStatus

    @classmethod
    def from_model(cls, model: Taxi) -> "TaxiDTO":
        return cls(
            id=model.id, network_id=model.network_id, x=model.x, y=model.y, status=model.status
        )

    def to_model(self) -> Taxi:
        return Taxi(id=self.id, network_id=self.network_id, x=self.x, y=self.y, status=self.status)


class TripDTO(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    taxi_id: UUID
    user_id: UUID

    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int

    created_at: datetime = datetime.utcnow()
    pickup_time: datetime | None = None
    dropoff_time: datetime | None = None

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
            created_at=model.created_at,
            pickup_time=model.pickup_time,
            dropoff_time=model.dropoff_time,
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
            created_at=self.created_at,
            pickup_time=self.pickup_time,
            dropoff_time=self.dropoff_time,
        )
