from __future__ import annotations


class ServiceError(Exception):
    """Base service exception."""


class NotFoundError(ServiceError):
    pass


class ConflictError(ServiceError):
    pass


class ValidationServiceError(ServiceError):
    def __init__(self, detail: str, errors: list[str] | None = None) -> None:
        super().__init__(detail)
        self.detail = detail
        self.errors = errors or []
