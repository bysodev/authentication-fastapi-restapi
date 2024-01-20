from fastapi import HTTPException,APIRouter,Depends,status, WebSocket, WebSocketDisconnect
from app.models.models import User
from app.schemas.schemas import Section
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.services.section import service_get_lessons_by_section, service_new_section, service_get_section_by_number, service_get_all_section
from app.services.user_lesson import service_get_user_lesson
from app.utils.hashing import Hash

router = APIRouter(
    prefix='/section',
    tags=['Section']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def new_section(section: Section, db: Session = Depends(get_db)):
    return service_new_section(section,db)

@router.get('/get/by/number', status_code=status.HTTP_200_OK)
def get_by_number(number: int, db: Session = Depends(get_db)):
    section = service_get_section_by_number(number,db)
    if section is None:
            raise HTTPException(status_code=400, detail="No se ha encontrado la sección")
    return section

@router.get('/get', status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    return service_get_all_section(db)


@router.get('/get/levelstage', status_code=status.HTTP_200_OK)
# def get_all_sections_with_lessons(db: Session = Depends(get_db), current_user = Depends(Hash.get_current_active_user)):
def get_all_sections_with_lessons(db: Session = Depends(get_db)):
    sections = service_get_all_section(db)
    sections_with_lessons = []
    for section in sections:
        lessons = service_get_lessons_by_section(section.id, db)
        # user_lesson = service_get_user_lesson(current_user.id, section.id, db)
        user_lesson = service_get_user_lesson(1, section.id, db)
        # 1) Validar si el usuario no tiene ningún registro en la tabla User_lesson.
        if user_lesson is None and lessons:
            # Si el usuario no ha realizado ninguna lección, y hay lecciones disponibles,
            # actualiza el estado de la primera lección a 2.
            lessons[0].state_id = 2
        # 2) Validar si el usuario ya tiene registros en la tabla User_lesson.
        elif user_lesson and lessons:
            # for lesson in lessons:
            # Obtén las IDs de lecciones que el usuario ya ha realizado.
            state_name = [user_lesson.state_name.name]
            completed_lesson_ids = [user_lesson.User_lesson.id_lesson]
            # Encuentra la siguiente lección no completada.
            next_incomplete_lesson = next((lesson for lesson in lessons if lesson.state_id == 1 and lesson.id not in completed_lesson_ids), None)
            if next_incomplete_lesson:
                # Si hay una lección no completada, actualiza su estado a 2.
                next_incomplete_lesson.state_id = 2
        sections_with_lessons.append({"section": section, "lessons": lessons})
    return sections_with_lessons