from fastapi import APIRouter
from schemas.requests import TaxiRegisterRequest
from schemas.response import TaxiRegisterResponse


router = APIRouter()


@router.get("/health-check")
def health_check():
    return {"status": "ok"}


@router.post("/register_taxi", response_model=TaxiRegisterResponse)
def register_taxi(payload: TaxiRegisterRequest):
    return {"status": "registered", "taxi_id": payload.taxi_id}
