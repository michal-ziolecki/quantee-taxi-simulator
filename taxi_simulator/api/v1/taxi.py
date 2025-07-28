from api.schemas.requests import TripAssignment
from api.schemas.response import TripAssignmentResponse
from controllers.taxi_controller import taxi_controller
from fastapi import APIRouter, BackgroundTasks
from loguru import logger
from models.enums import TripAssignmentStatus


router = APIRouter()


@router.post("/assign_client", response_model=TripAssignmentResponse)
async def assign_client(
    trip: TripAssignment, background_tasks: BackgroundTasks
) -> TripAssignmentResponse:
    logger.info(f"Received trip assignment req: {trip}")
    # await taxi_controller.handle_trip_request(
    #     trip
    # )
    background_tasks.add_task(taxi_controller.handle_trip_request, trip)
    return TripAssignmentResponse(
        status=TripAssignmentStatus.accepted, taxi_id=trip.taxi_id, user_id=trip.id
    )
