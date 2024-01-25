from fastapi import HTTPException, APIRouter, Depends, status, WebSocket, WebSocketDisconnect
from app.models.models import User
from app.schemas.schemas import Section
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.section import service_get_all_sections_with_lessons, service_new_section, service_get_section_by_number, service_get_all_section
from app.services.user_lesson import service_get_user_lesson
from app.utils.hashing import Hash

router = APIRouter(
    prefix='/section',
    tags=['Section']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def new_section(section: Section, db: Session = Depends(get_db)):
    """
    Create a new section.

    Args:
        section (Section): The section data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: The response data.
    """
    created_section = service_new_section(section, db)
    return {
        "data": created_section,
        "message": "Sección creada correctamente"
    }

@router.get('/get/by/number', status_code=status.HTTP_200_OK)
def get_by_number(number: int, db: Session = Depends(get_db)):
    """
    Get a section by its number.

    Args:
        number (int): The section number.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: The response data.
    """
    section = service_get_section_by_number(number, db)
    if section is None:
        raise HTTPException(status_code=400, detail="No se ha encontrado la sección")
    return {
        "data": section,
        "message": "Sección encontrada correctamente"
    }

@router.get('/get', status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    """
    Get all sections.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: The response data.
    """
    sections = service_get_all_section(db)
    return {
        "data": sections,
        "message": "Secciones obtenidas correctamente"
    }


@router.get('/get/levelstage', status_code=status.HTTP_200_OK)
def get_all_sections_with_lessons(current_user: User = Depends(Hash.get_current_active_user), db: Session = Depends(get_db)):
    try:
        sections_with_lessons = service_get_all_sections_with_lessons(current_user['id'], db)
        return {
            "data": sections_with_lessons,
            "message": "Secciones con lecciones obtenidas correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))