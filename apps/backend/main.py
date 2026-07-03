from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from apps.backend.src.db.database import init_db
from apps.backend.src.middleware.auth import request_correlation_middleware
from apps.backend.src.routes.router import api_router

app = FastAPI(title="Task Management Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173", "http://127.0.0.1:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=request_correlation_middleware)
app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "healthy"}
