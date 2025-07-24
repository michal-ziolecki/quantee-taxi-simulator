from uuid import UUID

from models.enums import TaxiStatus
from pydantic import BaseModel


class TaxiRegisterResponse(BaseModel):
    id: UUID
    status: TaxiStatus


class ClientResponse(BaseModel):
    user_id: UUID
