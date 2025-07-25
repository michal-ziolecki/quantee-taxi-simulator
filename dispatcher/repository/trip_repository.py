from uuid import UUID

from api.exceptions import NotExistException
from db.session import SessionLocal
from models.db_models import Trip
from models.dto_models import TripDTO


class TripRepository:
    # todo rethink reconnect on connection issue
    def __init__(self) -> None:
        self.db: SessionLocal = SessionLocal()

    def __del__(self) -> None:
        if self.db:
            self.db.close()

    def insert(self, dto: TripDTO) -> TripDTO:
        model: Trip = dto.to_model()
        self.db.add(model)
        self.db.commit()
        return TripDTO.from_model(model)

    def get_trips(self) -> list[TripDTO]:
        existing_objs = self.db.query(Trip).all()
        return [TripDTO.from_model(existing_obj) for existing_obj in existing_objs]

    def get_trip_by_id(self, trip_id: UUID) -> TripDTO:
        if not self.db.query(
            self.db.query(Trip).filter_by(id=trip_id).exists()
        ).scalar():
            raise NotExistException(message=f"Trip {trip_id} not exists!")
        existing_obj = self.db.query(Trip).filter_by(id=trip_id).one()
        return TripDTO.from_model(existing_obj)

    def update_trip(self, dto: TripDTO) -> TripDTO:
        if not self.db.query(
            self.db.query(Trip).filter_by(id=dto.id).exists()
        ).scalar():
            raise NotExistException(message=f"Trip {dto.id} not exists!")
        trip_data = dto.model_dump()
        not_editable = ["id", "taxi_id", "user_id"]
        for k in not_editable:
            trip_data.pop(k)
        self.db.query(Trip).filter_by(id=dto.id).update(trip_data)
        self.db.commit()
        return self.get_trip_by_id(trip_id=dto.id)


trip_repo = TripRepository()
