from api.v1.home import router as home_router
from api.v1.taxi import router as taxi_router
from api.v1.trip import router as trip_router
from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    app.include_router(home_router, prefix="")
    app.include_router(taxi_router, prefix="/api/v1/taxi")
    app.include_router(trip_router, prefix="/api/v1/trip")
