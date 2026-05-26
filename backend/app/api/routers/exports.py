from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.api.deps import get_export_service
from app.schemas.export import ExportRequest
from app.services.export_service import ExportService

router = APIRouter(prefix="/exports", tags=["exports"])


@router.post("")
def export_jobs(
    payload: ExportRequest,
    service: ExportService = Depends(get_export_service),
) -> Response:
    result = service.export(format_name=payload.format, filters=payload.filters)
    return Response(
        content=result.artifact.content,
        media_type=result.artifact.media_type,
        headers={"Content-Disposition": f'attachment; filename="{result.filename}"'},
    )
