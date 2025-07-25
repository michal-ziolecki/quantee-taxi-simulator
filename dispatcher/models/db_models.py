import uuid

from db.base import Base
from models.enums import TaxiStatus
from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



class Taxi(Base):
    __tablename__ = "taxis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    status = Column(Enum(TaxiStatus), nullable=False)  # type: ignore[var-annotated]

    trips = relationship("Trip", back_populates="taxi")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    taxi_id = Column(UUID(as_uuid=True), ForeignKey("taxis.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    pickup_x = Column(Integer, nullable=False)
    pickup_y = Column(Integer, nullable=False)
    dropoff_x = Column(Integer, nullable=False)
    dropoff_y = Column(Integer, nullable=False)

    waiting_time = Column(Integer)
    travel_time = Column(Integer)

    taxi = relationship("Taxi", back_populates="trips")
