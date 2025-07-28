from uuid import UUID

from api.exceptions import (
    NotExistException,
)
from api.schemas.requests import TaxiRegisterRequest, TaxiUnregisterRequest
from api.schemas.response import TaxiRegisterResponse
from loguru import logger
from models.dto_models import TaxiDTO
from models.enums import TaxiStatus
from repository.taxi_repository import TaxiRepository, taxi_repo


class TaxiService:
    def __init__(self, repo: TaxiRepository):
        self.repo = repo

    def register_taxi(self, payload: TaxiRegisterRequest) -> TaxiRegisterResponse:
        dto = TaxiDTO(
            id=payload.id,
            network_id=payload.network_id,
            x=payload.x,
            y=payload.y,
            status=TaxiStatus.available,
        )
        model: TaxiDTO = self.repo.upsert(dto)
        return TaxiRegisterResponse(id=model.id, status=model.status)

    def update_taxi(self, dto: TaxiDTO) -> TaxiDTO:
        return self.repo.upsert(dto)

    def unregister_taxi(self, payload: TaxiUnregisterRequest) -> TaxiRegisterResponse:
        model: TaxiDTO = self.find_taxi_by_id(payload.id)
        model.status = TaxiStatus.off
        result: TaxiDTO = self.repo.upsert(model)
        return TaxiRegisterResponse(id=result.id, status=result.status)

    def update_taxi_status(self, taxi: TaxiDTO) -> TaxiDTO:
        return self.repo.update_status(taxi)

    def find_available_taxis(self) -> list[TaxiDTO]:
        return self.repo.get_taxis_by_status(status=TaxiStatus.available)  # type: ignore

    def find_taxi_by_id(self, taxi_id: UUID) -> TaxiDTO:
        try:
            return self.repo.get(taxi_id)
        except NotExistException as e:
            logger.error(f"Not found taxi - taxi_id: {taxi_id}")
            raise e


taxi_service = TaxiService(taxi_repo)
