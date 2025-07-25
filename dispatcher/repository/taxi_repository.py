from uuid import UUID

from api.exceptions import (
    NotExistException,
)
from db.session import SessionLocal
from models.db_models import Taxi
from models.dto_models import TaxiDTO


class TaxiRepository:
    # todo rethink reconnect on connection issue
    def __init__(self) -> None:
        self.db: SessionLocal = SessionLocal()

    def __del__(self) -> None:
        if self.db:
            self.db.close()

    def upsert(self, dto: TaxiDTO) -> TaxiDTO:
        model = self.db.merge(dto.to_model())
        self.db.commit()
        self.db.refresh(model)
        return TaxiDTO.from_model(model)

    def get(self, texi_id: UUID) -> TaxiDTO:
        existing_obj = self.db.get(Taxi, texi_id)
        if not existing_obj:
            raise NotExistException(f"Not found taxi object with ID = {texi_id}")
        return TaxiDTO.from_model(existing_obj)


taxi_repo = TaxiRepository()
