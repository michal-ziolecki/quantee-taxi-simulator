from uuid import UUID

from pydantic import BaseModel


class TripAssignment(BaseModel):
    id: UUID
    taxi_id: UUID
    user_id: UUID
    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int
