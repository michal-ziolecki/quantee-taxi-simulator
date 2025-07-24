from uuid import UUID

from pydantic import BaseModel


class TaxiRegisterRequest(BaseModel):
    id: UUID
    x: int
    y: int


class ClientRequest(BaseModel):
    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int


class PickupNotification(BaseModel):
    taxi_id: UUID
    user_id: UUID


class DropoffNotification(BaseModel):
    taxi_id: UUID
    user_id: UUID
