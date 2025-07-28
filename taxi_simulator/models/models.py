from uuid import UUID

from pydantic import BaseModel


class TaxiRegisterNotification(BaseModel):
    id: UUID
    network_id: str  # network address / service name in docker network
    x: int
    y: int


class TripEventNotification(BaseModel):
    taxi_id: UUID
    trip_id: UUID
