from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import Base
from src.models.models import User, UserRole
from src.repositories.user_repository import UserRepository


def test_get_active_users_returns_only_active_users():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        active_user = User(
            email="active@example.com",
            password_hash="hash",
            full_name="Active User",
            role=UserRole.TEAM_MEMBER,
            is_active=True,
        )
        inactive_user = User(
            email="inactive@example.com",
            password_hash="hash",
            full_name="Inactive User",
            role=UserRole.TEAM_MEMBER,
            is_active=False,
        )
        session.add_all([active_user, inactive_user])
        session.commit()

        repo = UserRepository(session)
        users = repo.get_active_users()

        assert [user.id for user in users] == [active_user.id]
