import datetime
from http import HTTPStatus
from typing import Any


class BaseHTTPException(Exception):
    """
    Custom exception ready to use inside app logic,
    all handled exceptions should be converted into that custom exception which inherited from BaseHTTPException.
    This error type is registered in Fast API framework and translated into correct HTTP error response
    (without un-control interruptions).
    """

    error_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value
    error_name: str = HTTPStatus.INTERNAL_SERVER_ERROR.name
    message: str = f"{HTTPStatus.INTERNAL_SERVER_ERROR.description}, not handled exception"
    meta: Any | None = None

    def __init__(
        self,
        error_code: int | None = None,
        error_name: str | None = None,
        message: str | None = None,
    ) -> None:
        self.code = error_code or self.error_code
        self.name = error_name or self.error_name
        self.description = message or self.message
        self.error_datetime = datetime.datetime.now()
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code}, message={self.description}, datetime={self.error_datetime})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code}, message={self.description}, datetime={self.error_datetime})"

    def to_response(self) -> tuple[dict[str, str | int], int]:
        """
        The to_response function is a helper function that returns the error message in a format
        that can be easily serialized to JSON. It also includes the HTTP status code for this error.

        :return: A tuple with a dictionary {"name": name, "message": description}
        and an integer as Status Code
        """
        response: dict[str, Any] = {
            "name": self.name,
            "message": self.description,
            "datetime": self.error_datetime.isoformat(),
        }
        if self.meta:
            response["meta"] = self.meta
        return response, self.code
