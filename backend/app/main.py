from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.database import Base, engine, ensure_database_schema
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="FastAPI Notes Application",
    description="Production-quality FastAPI backend for managing notes",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    ensure_database_schema()
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "FastAPI Notes Application is running successfully!"}
