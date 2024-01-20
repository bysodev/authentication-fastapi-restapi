from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import section, lesson
from app.models.models import Section

def service_new_section(new_section, db: Session):
    try:
        # Convertir la instancia de Lesson a un diccionario
        section_dict = new_section.__dict__

        # Eliminar claves no deseadas, como claves internas de SQLAlchemy
        section_dict = {key: value for key, value in section_dict.items() if not key.startswith('_')}

        # Crear la instancia de Lesson con ** y el diccionario
        lesson_instance = Section(**section_dict)

        section.create_section(lesson_instance, db)
        return {"section": new_section}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la sección {e}"
        )
    
def service_get_section_by_number(number: int, db: Session):
    try:
        return section.get_section_by_number(number, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se ha encontrado la lección {e}"
        )
    
def service_get_all_section(db: Session):
    try:
        return section.get_all(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ha ocurrido un error inesperado {e}"
        )
    
def service_get_lessons_by_section(section_id: int, db: Session):
    try:
        return lesson.get_lessons_by_section(section_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se han encontrado lecciones para la sección {section_id}: {e}"
        )