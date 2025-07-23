from pydantic import BaseModel


class TaxiRegisterRequest(BaseModel):
    taxi_id: str
    x: int
    y: int


class ClientRequest(BaseModel):
    user_id: str
    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int


class PickupNotification(BaseModel):
    taxi_id: str
    user_id: str


class DropoffNotification(BaseModel):
    taxi_id: str
    user_id: str
