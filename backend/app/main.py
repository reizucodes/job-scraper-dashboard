from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_exception_handlers
from app.api.routers import (
    bookmarks_router,
    exports_router,
    job_listings_router,
    job_sources_router,
    scrape_runs_router,
    source_profiles_router,
)
from app.core.config import get_settings
from app.db.seeds import seed_job_sources, seed_source_profiles
from app.db.session import SessionLocal

settings = get_settings()


@asynccontextmanager
async def seed_app_lifespan(_: FastAPI):
    with SessionLocal() as session:
        seed_source_profiles(session)
        seed_job_sources(session)
        session.commit()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=seed_app_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(source_profiles_router)
app.include_router(job_sources_router)
app.include_router(scrape_runs_router)
app.include_router(job_listings_router)
app.include_router(bookmarks_router)
app.include_router(exports_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
