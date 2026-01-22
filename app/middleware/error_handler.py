from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exception import DatabaseError, BusinessError, ItemNotFoundError


def business_exception_handler(request: Request, exc: BusinessError):
    status_code = 500
    if isinstance(exc, DatabaseError):
        status_code = 504
    if isinstance(exc, ItemNotFoundError):
        status_code = 404

    return JSONResponse(
        status_code=status_code,
        content={"error": exc.__class__.__name__, "message": str(exc)},
    )
