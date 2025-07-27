from uuid import UUID

from models.enums import TripAssignmentStatus
from pydantic import BaseModel


class TripAssignmentResponse(BaseModel):
    status: TripAssignmentStatus
    taxi_id: UUID
    user_id: UUID
