from sqlalchemy import Column, ForeignKey, Integer, String

from dispatcher.db.base import Base


class Taxi(Base):
    __tablename__ = "taxis"

    id = Column(Integer, primary_key=True, index=True)
    taxi_id = Column(String, unique=True, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    status = Column(String, nullable=False)  # 'available' or 'busy' # todo add enum


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    taxi_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    pickup_x = Column(Integer, nullable=False)
    pickup_y = Column(Integer, nullable=False)
    dropoff_x = Column(Integer, nullable=False)
    dropoff_y = Column(Integer, nullable=False)
    waiting_time = Column(Integer)
    travel_time = Column(Integer)
