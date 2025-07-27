from uuid import UUID

from api.exceptions import NotExistException
from db.session import SessionLocal
from models.db_models import Taxi
from models.dto_models import TaxiDTO
from models.enums import TaxiStatus


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
        return TaxiDTO.from_model(model)

    def update_status(self, dto: TaxiDTO) -> TaxiDTO | None:
        model = self.db.get(Taxi, dto.id)
        if not model:
            raise NotExistException(message=f"Taxi with id = {dto.id}, not found!")

        model.status = dto.status
        self.db.commit()
        return TaxiDTO.from_model(model)

    def get(self, taxi_id: UUID) -> TaxiDTO:
        existing_obj = self.db.get(Taxi, taxi_id)
        if not existing_obj:
            raise NotExistException(message=f"Not found taxi object with ID = {taxi_id}")
        return TaxiDTO.from_model(existing_obj)

    def get_taxis_by_status(self, status: TaxiStatus) -> list[TaxiDTO]:
        existing_objs = self.db.query(Taxi).filter_by(status=status).all()
        return [TaxiDTO.from_model(existing_obj) for existing_obj in existing_objs]


taxi_repo = TaxiRepository()
