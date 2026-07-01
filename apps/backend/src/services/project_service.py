import uuid

from sqlalchemy.orm import Session

from apps.backend.src.domain.models import Project


def create_project(db: Session, name: str, description: str | None) -> dict:
    project_id = str(uuid.uuid4())
    project = Project(id=project_id, name=name, description=description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
    }


def get_project(db: Session, project_id: str) -> dict | None:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
    }
