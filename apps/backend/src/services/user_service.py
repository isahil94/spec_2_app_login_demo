import json
from typing import Any

from sqlalchemy.orm import Session

from apps.backend.src.domain.models import TeamMembership, User


def get_user_profile(db: Session, user_id: str) -> dict[str, Any]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    team_memberships = db.query(TeamMembership).filter(TeamMembership.user_id == user_id).all()
    teams = [membership.team_id for membership in team_memberships]
    preferences = json.loads(user.preferences or "{}")
    return {
        "user_id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "roles": user.roles.split(",") if user.roles else ["User"],
        "teams": teams,
        "preferences": preferences,
    }


def update_profile(db: Session, user: User, updates: dict) -> dict[str, Any]:
    if updates.get("display_name"):
        user.display_name = updates["display_name"]
    if updates.get("avatar_url"):
        preferences = json.loads(user.preferences or "{}")
        preferences["avatar_url"] = updates["avatar_url"]
        user.preferences = json.dumps(preferences)
    if updates.get("time_zone"):
        preferences = json.loads(user.preferences or "{}")
        preferences["time_zone"] = updates["time_zone"]
        user.preferences = json.dumps(preferences)
    if updates.get("language"):
        preferences = json.loads(user.preferences or "{}")
        preferences["language"] = updates["language"]
        user.preferences = json.dumps(preferences)

    db.commit()
    db.refresh(user)
    return get_user_profile(db, user.id)


def update_settings(db: Session, user: User, updates: dict) -> dict[str, Any]:
    preferences = json.loads(user.preferences or "{}")
    if updates.get("notification_preferences") is not None:
        preferences["notification_preferences"] = updates["notification_preferences"]
    if updates.get("theme") is not None:
        preferences["theme"] = updates["theme"]
    if updates.get("time_zone") is not None:
        preferences["time_zone"] = updates["time_zone"]
    if updates.get("language") is not None:
        preferences["language"] = updates["language"]
    user.preferences = json.dumps(preferences)
    db.commit()
    db.refresh(user)
    return get_user_profile(db, user.id)
