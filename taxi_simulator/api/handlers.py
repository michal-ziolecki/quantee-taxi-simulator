from api.exceptions import (
    BaseHTTPException,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"name": "BAD_REQUEST", "message": exc.errors()},
        )

    @app.exception_handler(BaseHTTPException)
    def handle_custom_exception(request: Request, error: BaseHTTPException) -> JSONResponse:
        content, status_code = error.to_response()
        return JSONResponse(
            status_code=status_code,
            content=content,
        )

    @app.exception_handler(ValidationError)
    def handle_pydantic_exception(request: Request, error: ValidationError) -> JSONResponse:
        logger.error(f"Error handler caught pydantic error: {error}")
        http_error = BaseHTTPException(message="Validation problems.")
        content, status_code = http_error.to_response()
        return JSONResponse(
            status_code=status_code,
            content=content,
        )

    @app.exception_handler(Exception)
    def handle_exception(request: Request, error: Exception) -> JSONResponse:
        if isinstance(error, BaseHTTPException):
            logger.error(f"Error handler caught custom error: {error}")
            content, status_code = error.to_response()
            return JSONResponse(
                status_code=status_code,
                content=content,
            )
        logger.error(f"Error handler caught standard error: {error}")
        http_error = BaseHTTPException()
        content, status_code = http_error.to_response()
        return JSONResponse(
            status_code=status_code,
            content=content,
        )
