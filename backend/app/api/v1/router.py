from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, files, notes

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
