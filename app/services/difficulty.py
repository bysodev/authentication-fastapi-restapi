from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import difficulty
from app.models import models

def service_new_difficulty(new_difficulty, db: Session):
    difficulty_dict = new_difficulty.dict()

    try:
        new_difficulty = models.Difficulty(**difficulty_dict)
        if not difficulty.get_difficulty(db, difficulty_dict["name"] ):
            difficulty.create_difficulty(new_difficulty, db)
            return difficulty_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el nivel de dificultad {e}"
        )

def bring_difficulties( db: Session ):
    try:
        return difficulty.get_difficultys(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda de las dificultades {e}"
        )