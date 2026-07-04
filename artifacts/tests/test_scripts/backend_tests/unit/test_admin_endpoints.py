from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from src.models.models import UserRole
from src.repositories.other_repositories import TeamRepository
from src.repositories.user_repository import UserRepository


def test_create_admin_and_team_membership():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    user_repo = UserRepository(session)
    team_repo = TeamRepository(session)

    # Create admin user
    admin = user_repo.create_user(
        "admin@example.com", "hashedpw", "Admin User", role=UserRole.ADMIN
    )
    assert admin is not None
    assert str(admin.role) == str(UserRole.ADMIN)

    # Create team
    team = team_repo.create_team("Team A", "Test team")
    assert team is not None
    assert team.name == "Team A"

    # Add member to team
    user = user_repo.create_user("member@example.com", "hashedpw2", "Member User")
    team.members.append(user)
    session.commit()

    members = team_repo.get_user_teams(user.id)
    # get_user_teams returns list of teams for the user; ensure membership exists
    assert isinstance(members, list)
    assert any(t.name == "Team A" for t in members)
