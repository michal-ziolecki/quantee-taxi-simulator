import json
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, model_validator


class TaxiRegisterRequest(BaseModel):
    id: UUID | None
    network_id: str  # network address / service name in docker network
    x: int
    y: int

    @model_validator(mode="before")
    @classmethod
    def generate_id_if_missing(cls, values: dict[str, Any] | str) -> dict[str, Any]:
        if isinstance(values, str):
            values = json.loads(values)
        if not values.get("id"):  # type: ignore
            values["id"] = uuid4()  # type: ignore
        return values  # type: ignore


class TaxiUnregisterRequest(BaseModel):
    id: UUID


class ClientRequest(BaseModel):
    user_id: UUID  # in real application this is will be from JWT during the request.
    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int


class PickupNotification(BaseModel):
    taxi_id: UUID
    trip_id: UUID


class DropoffNotification(BaseModel):
    taxi_id: UUID
    trip_id: UUID
