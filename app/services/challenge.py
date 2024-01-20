from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from app.utils.hashing import Hash
from sqlalchemy.orm import Session
from app.repository import challenge
from app.models import models
import json

def service_new_challenge(new_challenge, db: Session):
    challenge_dict = new_challenge.dict()

    try:
        new_challenge = models.Challenges(**challenge_dict)
        if not challenge.get_challenge(db, challenge_dict["number"], challenge_dict["name"] ):
            challenge.create_challenge(new_challenge, db)
            return challenge_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el reto {e}"
        )

def bring_challenge(db: Session):
    try:
        return challenge.get_challenges( db )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda de los retos {e}"
        )

def bring_challanges_by_category( db: Session, category: str ):
    try:
        return challenge.get_challenges_by_category( db, category.upper() )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda por la categoria {e}"
        )
    
def to_dict_list(results):
    response_data = []
    for challenge, end_points in results:
        challenge_dict = challenge.to_dict()
        challenge_dict["end_points"] = end_points
        response_data.append(challenge_dict)
    return response_data

def bring_challanges_by_user(category: str, id: int,  db: Session ):
    print('Hola mundo')
    result_chall = challenge.get_challenges_by_user_and_difficulty( db, id )
    # output = [x for x in result_chall]
    output = []
    categoria_data = {models.EnumCategory.PALABRAS: [], models.EnumCategory.NUMEROS: []}
    # for challenges, *aditional in result_chall:
    for categoria, dificultad, total, progreso, puntos in result_chall:
        if( categoria == models.EnumCategory.PALABRAS ):
            categoria_data[models.EnumCategory.PALABRAS].append({
                'dificultad': dificultad,
                'total': total, 
                'progreso': progreso,
                'puntos': puntos
            })
        
        if( categoria == models.EnumCategory.NUMEROS ):
            categoria_data[models.EnumCategory.NUMEROS].append({
                'dificultad': dificultad,
                'total': total, 
                'progreso': progreso,
                'puntos': puntos
            })

    print(categoria_data)
    # output = [jsonable_encoder(x) for x in result_chall]
    try:
        return categoria_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda por la categoria {e}"
        )
    

def bring_challanges_by_userDSA(category: str, id: int,  db: Session ):
    print('Hola mundo')
    result_chall = challenge.get_challenges_by_user( db, category.upper(), id )
    # output = [x for x in result_chall]
    output = []
    # for challenges, *aditional in result_chall:
    for challenges, end_points, reach_state, minutes, difficulty_name, category_name in result_chall:
        print(f'Este es el challange: { challenges.as_dict() }')
        final = challenges.as_dict()
        additional_info = {
            'end_points': end_points,
            'reach_state': reach_state,
            'minutes': minutes,
            'difficulty_name': difficulty_name,
            'category_name': category_name
        }
        final.update(additional_info)
        output.append(final)
    # print(output)
    # output = [jsonable_encoder(x) for x in result_chall]
    try:
        return output
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda por la categoria {e}"
        )
    
