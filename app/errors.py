from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi.exceptions import HTTPException


class CustomHTTPException(HTTPException):
    status_code: int

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=self.status_code, detail=detail, headers=headers)


class StripeBadRequest(CustomHTTPException):
    status_code = HTTPStatus.BAD_REQUEST
