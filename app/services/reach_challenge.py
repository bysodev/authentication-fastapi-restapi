from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.repository import reach_challenge, category, difficulty
from app.models import models
from app.utils.hashing import Hash
from app.services.challenge import bring_challenge_id

def service_new_reach_challenge(new_reach_challenge, db: Session):
    reach_challenge_dict = new_reach_challenge
    print(reach_challenge_dict)
    challenge, difficulty = bring_challenge_id(reach_challenge_dict['id_challenge'], db)
    porcentaje = (reach_challenge_dict['points'] / challenge.points) * 100
    print(porcentaje)
    print(difficulty.bonus)
    bonus = 0
    end_points = 0
    if porcentaje > 65 :
        print('Si entro')
        bonus = difficulty.bonus
        end_points = reach_challenge_dict['points'] + bonus

    new_user_challenge = {
        "bonus": bonus,
        "end_points": end_points,
        **new_reach_challenge
    }
    print(new_user_challenge)
    try:
        new_reach_challenge = models.ReachChallenges(**new_user_challenge)
        reach_challenge.create_reach_challenge(new_reach_challenge, db)
        return new_user_challenge
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el alcance del reto {e}"
        )
    
def service_new_reach_customized_challenge(new_reach_customized_challenge, db: Session):
    categoria = category.get_category(db, new_reach_customized_challenge['category'])
    dificultad = difficulty.get_difficulty(db, new_reach_customized_challenge['difficulty'])
    if not categoria or not dificultad:
        return None

    definitivo_customized_challenge = { 
        "id_user": new_reach_customized_challenge["id_user"],
        "id_category": categoria.id,
        "id_difficulty": dificultad.id,
        "bonus": dificultad.bonus,
        "points": 0,
        "end_points": dificultad.bonus,
        "minutes_max": new_reach_customized_challenge["minutes_max"],
        "seconds_max": new_reach_customized_challenge["seconds_max"],
        "minutes": new_reach_customized_challenge["minutes"],
        "seconds": new_reach_customized_challenge["seconds"],
        "lives": new_reach_customized_challenge["lives"],
        "fails": new_reach_customized_challenge["fails"]
    }
    try:
        print('El modelo')
        print(definitivo_customized_challenge)
        new_reach_customized_challenge = models.ReachChallengesCustomized(**definitivo_customized_challenge)
        print(new_reach_customized_challenge)
        reach_challenge.create_reach_customized_challenge(new_reach_customized_challenge, db)
        print('Buena respuesta')
        return definitivo_customized_challenge
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al registrar el reto personalizado {e}"
        )

def bring_reach_challenges(db: Session):
    try:
        return reach_challenge.get_reach_challenges(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda de todos los retos logrados {e}"
        )

def bring_reach_challanges_by_id( db: Session, id: int ):
    try:
        return reach_challenge.get_reach_challenge_by_challenge(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda del reto logrado {e}"
        )
    
def bring_reach_challanges_by_user( db: Session, category: str, id: int ):
    try:
        return reach_challenge.get_reach_challenge_by_user(category, id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda de sus retos ha fallado {e}"
        )
    
def bring_reach_challanges_by_user( db: Session, current_user = Depends(Hash.get_current_user) ):
    print(current_user)
    try:
        return reach_challenge.get_reach_challenge_by_user(current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda de sus retos logrados {e}"
        )