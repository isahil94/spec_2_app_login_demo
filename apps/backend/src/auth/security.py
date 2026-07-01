from typing import Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from apps.backend.src.auth.jwt import decode_token

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict[str, object]:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from exc

    return {
        "user_id": payload.get("sub"),
        "roles": payload.get("roles", []),
    }


def require_role(required_roles: list[str]):
    def role_dependency(current_user: dict[str, object] = Depends(get_current_user)) -> dict[str, object]:
        roles = current_user.get("roles", [])
        if not any(role in roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

    return role_dependency


def optional_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Optional[dict[str, object]]:
    if not credentials:
        return None
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except Exception:
        return None
    return {
        "user_id": payload.get("sub"),
        "roles": payload.get("roles", []),
    }
