import logging

from apps.backend.src.logging.logger import configure_logging
from apps.backend.src.routes.routes import api_router
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from apps.backend.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug, version="1.0.0")
configure_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = request.headers.get("X-Request-ID", "")
    details = [error.get("msg") for error in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={
            "error_code": "VALIDATION_ERROR",
            "message": "Validation failed.",
            "details": details,
            "request_id": request_id,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = request.headers.get("X-Request-ID", "")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "details": [],
            "request_id": request_id,
        },
    )


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled exception: %s", exc)
    request_id = request.headers.get("X-Request-ID", "")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "details": [],
            "request_id": request_id,
        },
    )


app.include_router(api_router)
