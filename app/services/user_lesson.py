from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import user_lesson
from app.schemas.schemas import UserInDB
from app.models.models import User_lesson

def service_create_new(new_user_lesson, db: Session):
    try:
        # Convertir la instancia de Lesson a un diccionario
        user_lesson_dict = new_user_lesson.__dict__
        # Eliminar claves no deseadas, como claves internas de SQLAlchemy
        user_lesson_dict = {key: value for key, value in user_lesson_dict.items() if not key.startswith('_')}
        # Crear la instancia de Lesson con ** y el diccionario
        user_lesson_instance = User_lesson(**user_lesson_dict)
        user_lesson.create_new(user_lesson_instance, db)
        return {"user_lesson": new_user_lesson}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el detalle de la lección {e}"
        )
    
def service_get_by_number(number: int, db: Session):
    try:
        return user_lesson.get_by_number(number, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se ha encontrado el detalle de la lección {e}"
        )
    
def service_get_all(db: Session):
    try:
        return user_lesson.get_all(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se han encontrado registros de detalle de las lecciones {e}"
        )
    
def service_get_user_lesson(user_id: int, section_id: int, db: Session):
    try:
        return user_lesson.get_detail_user_lesson(user_id, section_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se han encontrado registros {e}"
        )