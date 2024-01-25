from datetime import datetime
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.repository import user_lesson
from app.schemas.schemas import UserInDB
from app.models.models import User_lesson

def service_create_new(new_user_lesson, db: Session):
    try:
        # Eliminar claves no deseadas, como claves internas de SQLAlchemy
        user_lesson_dict = {key: value for key, value in new_user_lesson.items() if not key.startswith('_')}
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
def service_update_user_lesson(last_user_lesson, user_id, db: Session):
    try:
        user_lesson_instance = user_lesson.get_user_lesson_by_lesson_id_and_user_id(last_user_lesson.id_lesson, user_id, db)
        #get fails, fails detail
        fails = last_user_lesson.fails
        detail_fails = last_user_lesson.detail_fails
        #add last fails, fails detail with news data
        fails += user_lesson_instance.fails
        detail_fails = [str(int(a) + int(b)) for a, b in zip(detail_fails, user_lesson_instance.detail_fails)]
        if user_lesson_instance is not None:
            if user_lesson_instance.last_points_reached == 0:
                if last_user_lesson.points_reached > user_lesson_instance.points_reached:
                    #update only values score, fails, detail_fails
                    user_lesson.update_user_lesson(user_lesson_instance.id, last_user_lesson.state_id, last_user_lesson.points_reached, fails, detail_fails, db)
                    return JSONResponse(content={"message": "Lección actualizada correctamente"}, status_code=status.HTTP_201_CREATED)
                else:
                    return JSONResponse(content={"message": "La puntuación no es mayor que la puntuación alcanzada anteriormente"}, status_code=status.HTTP_400_BAD_REQUEST)          

            elif user_lesson_instance.last_points_reached != 0:
                if last_user_lesson.points_reached > user_lesson_instance.last_points_reached:
                    #update only values score, fails, detail_fails
                    user_lesson.update_user_lesson(user_lesson_instance.id, last_user_lesson.state_id, last_user_lesson.points_reached, fails, detail_fails, db)
                    return JSONResponse(content={"message": "Lección actualizada correctamente"}, status_code=status.HTTP_201_CREATED)
                else:
                    return JSONResponse(content={"message": "La puntuación no es mayor que la última puntuación alcanzada"}, status_code=status.HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse(content={"message": "No se han encontrado registros"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise HTTPException(
            status_code=getattr(e, "status_code", status.HTTP_400_BAD_REQUEST),
            detail=f"{e.detail}"
        )