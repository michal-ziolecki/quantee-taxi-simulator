from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter()


@router.get("/health-check")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")
