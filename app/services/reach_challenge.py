from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.repository import reach_challenge
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
    if porcentaje > 75 :
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