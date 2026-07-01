import datetime
from typing import Any

from jose import jwt

from apps.backend.config import settings


def create_token(subject: str, roles: list[str]) -> dict[str, Any]:
    now = datetime.datetime.utcnow()
    expires = now + datetime.timedelta(minutes=settings.jwt_expiration_minutes)
    payload = {
        "sub": subject,
        "roles": roles,
        "iat": now,
        "exp": expires,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    return {"token": token, "expires_in": settings.jwt_expiration_minutes}


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
