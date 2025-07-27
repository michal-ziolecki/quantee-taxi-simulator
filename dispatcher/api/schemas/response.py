from datetime import datetime
from uuid import UUID

from models.enums import TaxiStatus, TripRequestStatus
from pydantic import BaseModel


class TaxiRegisterResponse(BaseModel):
    id: UUID
    status: TaxiStatus


class TaxiResponse(BaseModel):
    id: UUID
    network_id: str
    x: int
    y: int
    status: TaxiStatus


class TripResponse(BaseModel):
    id: UUID
    taxi_id: UUID
    user_id: UUID

    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int

    created_at: datetime | None = None
    pickup_time: datetime | None = None
    dropoff_time: datetime | None = None


class ClientRequestResponse(BaseModel):
    status: TripRequestStatus
    trip_id: UUID | None = None
    taxi_id: UUID | None = None
