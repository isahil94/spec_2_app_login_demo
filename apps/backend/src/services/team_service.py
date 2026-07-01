import uuid
from typing import Optional

from sqlalchemy.orm import Session

from apps.backend.src.domain.models import Team, TeamMembership, User


def create_team(db: Session, name: str, description: Optional[str], lead_user_id: str) -> dict:
    team_id = str(uuid.uuid4())
    team = Team(
        id=team_id,
        name=name,
        description=description,
        lead_user_id=lead_user_id,
    )
    db.add(team)
    membership = TeamMembership(
        id=str(uuid.uuid4()),
        team_id=team_id,
        user_id=lead_user_id,
        role="TeamLead",
    )
    db.add(membership)
    db.commit()
    db.refresh(team)
    return {
        "team_id": team.id,
        "name": team.name,
        "description": team.description,
        "lead_user_id": team.lead_user_id,
    }


def get_team(db: Session, team_id: str) -> Optional[dict]:
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        return None
    members = [
        {"user_id": member.user_id, "role": member.role}
        for member in team.members
    ]
    return {
        "team_id": team.id,
        "name": team.name,
        "description": team.description,
        "lead_user_id": team.lead_user_id,
        "members": members,
    }


def list_teams(db: Session) -> list[dict]:
    teams = db.query(Team).all()
    return [
        {"team_id": team.id, "name": team.name, "description": team.description, "lead_user_id": team.lead_user_id}
        for team in teams
    ]


def add_team_member(db: Session, team_id: str, user_id: str, role: str) -> dict:
    membership = TeamMembership(
        id=str(uuid.uuid4()),
        team_id=team_id,
        user_id=user_id,
        role=role,
    )
    db.add(membership)
    db.commit()
    return {"team_id": team_id, "user_id": user_id, "role": role}


def update_team_member_role(db: Session, team_id: str, user_id: str, role: str) -> dict:
    membership = db.query(TeamMembership).filter(TeamMembership.team_id == team_id, TeamMembership.user_id == user_id).first()
    if not membership:
        raise ValueError("Membership not found")
    membership.role = role
    db.commit()
    return {"team_id": team_id, "user_id": user_id, "role": role}


def remove_team_member(db: Session, team_id: str, user_id: str) -> dict:
    membership = db.query(TeamMembership).filter(TeamMembership.team_id == team_id, TeamMembership.user_id == user_id).first()
    if not membership:
        raise ValueError("Membership not found")
    db.delete(membership)
    db.commit()
    return {"team_id": team_id, "user_id": user_id, "status": "removed"}
