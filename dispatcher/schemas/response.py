from pydantic import BaseModel


class TaxiRegisterResponse(BaseModel):
    status: str
    taxi_id: str
