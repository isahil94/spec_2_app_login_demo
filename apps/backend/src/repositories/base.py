"""Base repository for generic CRUD operations."""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import and_
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository for CRUD operations."""

    def __init__(self, session: Session, model: Type[T]):
        """Initialize repository."""
        self.session = session
        self.model = model

    def create(self, obj_in: dict) -> T:
        """Create a new object."""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def get_by_id(self, id: str) -> Optional[T]:
        """Get object by ID."""
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with pagination."""
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: str, obj_in: dict) -> Optional[T]:
        """Update object."""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: str) -> bool:
        """Delete object."""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        self.session.delete(db_obj)
        self.session.commit()
        return True

    def filter(self, **kwargs) -> List[T]:
        """Filter objects by criteria."""
        query = self.session.query(self.model)
        for key, value in kwargs.items():
            if value is not None:
                query = query.filter(getattr(self.model, key) == value)
        return query.all()
