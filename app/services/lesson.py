from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import lesson
from app.schemas.schemas import UserInDB, Lesson
from app.models.models import Lesson

def service_new_lesson(new_lesson, db: Session):
    try:
        # Convertir la instancia de Lesson a un diccionario
        lesson_dict = new_lesson.__dict__

        # Eliminar claves no deseadas, como claves internas de SQLAlchemy
        lesson_dict = {key: value for key, value in lesson_dict.items() if not key.startswith('_')}

        # Agregar manualmente time_creation y time_update al diccionario
        lesson_dict['time_creation'] = datetime.now()
        lesson_dict['time_update'] = None

        # Crear la instancia de Lesson con ** y el diccionario
        lesson_instance = Lesson(**lesson_dict)

        lesson.create_lesson(lesson_instance, db)
        return {"lesson": new_lesson}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la lección {e}"
        )
    
def service_get_by_number(number: int, db: Session):
    try:
        return lesson.get_lesson_by_number(number, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se ha encontrado la lección {e}"
        )
    
def service_get_category_by_number(number: int, db: Session):
    try:
        return lesson.get_lesson_category_by_number(number, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se ha encontrado la lección {e}"
        )
       
def service_get_all(db: Session):
    try:
        return lesson.get_all(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ha ocurrido un error inesperado {e}"
        )