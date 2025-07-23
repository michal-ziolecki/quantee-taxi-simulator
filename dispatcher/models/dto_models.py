from pydantic import BaseModel


class TaxiDTO(BaseModel):
    taxi_id: str
    x: int
    y: int
    status: str


class TripDTO(BaseModel):
    taxi_id: str
    user_id: str
    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int
    waiting_time: int | None = None
    travel_time: int | None = None
