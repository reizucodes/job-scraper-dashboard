from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.errors import ConflictError, NotFoundError, ValidationServiceError


class ErrorResponse(JSONResponse):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, content={"detail": detail})


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return ErrorResponse(status_code=404, detail=str(exc))

    @app.exception_handler(ConflictError)
    async def conflict_handler(_: Request, exc: ConflictError) -> JSONResponse:
        return ErrorResponse(status_code=409, detail=str(exc))

    @app.exception_handler(ValidationServiceError)
    async def validation_handler(_: Request, exc: ValidationServiceError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": exc.detail, "errors": exc.errors},
        )
