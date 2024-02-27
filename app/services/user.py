import datetime
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import numpy as np
from sqlalchemy.orm import Session
from app.utils import hashing
from app.utils import gesture
from app.utils.proccess import process_image_from_base64
from app.repository import user
from app.models import models
from app.schemas.schemas import Provider, User_lesson, UserInDB, Lesson, UserUpdate
from app.models.models import User
from decouple import config
from datetime import timedelta, datetime
from app.utils.hashing import Hash

# model_path = "./model/gesture_recognizer.task"
model_path_number = "./model/gesture_recognizer_number.task"
model_path_letter = "./model/gesture_recognizer_letters.task"

# gesture_recognition = gesture.GestureRecognitionService(model_path)
gesture_recognition_number = gesture.GestureRecognitionService(model_path_number)
gesture_recognition_letter = gesture.GestureRecognitionService(model_path_letter)

class UserAlreadyExistsException(Exception):
    pass

def service_new_user(new_user, db: Session):
    user_dict = new_user.dict()
    password_hash = hashing.Hash.hash_password(user_dict["password"])
    verify_hash = hashing.Hash.hash_verify()

    try:
        new_user = models.User(
            username=user_dict["username"],
            password=password_hash,
            email=user_dict["email"],
            image=user_dict["image"],
            token=verify_hash
        )

        if not user.get_user_by_name_or_email(new_user, db):
            user.create_user(new_user, db)
            return { "username": new_user.username, "token": str(verify_hash) }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario {e}"
        )

def service_verified_user(token: str, db: Session):
    try:
        return user.verify_user_by_token(token, db)
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error verificando usuario {e}"
        )
    
def authenticate_user(db: Session, username: str, password: str):
    userData = user.get_user(db, username)
    if not userData:
        return False
    if not hashing.Hash.verify_password(password, userData.password):
        return False
    return userData


def authenticate_user_provider(user_provider: Provider, db: Session):
    try: 
        # parse string value int int 
        db_provider = user.get_provider_by_user_id(id=user_provider.password, db=db)
        if db_provider:
            provider_found = user.get_user_by_id(db_provider.user_id, db)
            user_verify = authenticate_user_verify(db, provider_found.username, user_provider.password)
            access_token_expire = timedelta(minutes=int(config('ACCESS_TOKEN_EXPIRE_MINUTES')))
            access_token = Hash.create_access_token(
                data={'name': user_verify.username, 'email': user_verify.email},
                expires_delta=access_token_expire
            )
            return {
                'message': "Has iniciado sesión correctamente",
                'accessToken': access_token,
                'creation': user_verify.creation.strftime("%Y-%m-%d"),
                'username': user_verify.username,
                'email': user_verify.email,
                'image': user_verify.image,
                'id': user_verify.id
            }
        else:
            password_hash = hashing.Hash.hash_password(user_provider.password)
            verify_hash = hashing.Hash.hash_verify()
            # genearete a unique string for username user
            random_username = generate_unique_username(db, user_provider) 
            # create a user object from provider
            new_user = models.User(
                username=random_username,
                password=password_hash,
                email=user_provider.email,
                image=user_provider.image,
                token=verify_hash,
                verified=True
            )
            if not user.get_user_by_name_or_email(new_user, db):
                user.create_user(new_user, db)
                new_user_provider = models.Provider(provider_name=user_provider.provider_name, provider_id=int(user_provider.password), user_id=new_user.id)
                user.create_provider(new_user_provider, db=db)
                access_token_expire = timedelta(minutes=int(config('ACCESS_TOKEN_EXPIRE_MINUTES')))
                access_token = Hash.create_access_token(
                    data={'name': new_user.username, 'email': new_user.email},
                    expires_delta=access_token_expire
                )
                return {
                    'message': "Has iniciado sesión correctamente",
                    'accessToken': access_token,
                    'creation': datetime.now().strftime("%Y-%m-%d"),                
                    'username': new_user.username,
                    'email': new_user.email,
                    'image': new_user.image,
                    'id': new_user.id
                }
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está en uso",
            ) 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )
    
def service_recovery_password(email: str, db: Session):
    user_to_recover = User(email=email)  # Create a User object with the provided email
    user_found = user.get_user_by_email(user_to_recover, db)
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico no está registrado",
        ) 
    # Implement the logic to recover the password
    recovery_password=hashing.Hash.hash_password(email)
    user.update_recovery(recovery_password, user_found.id, db)
    return {
        'message': "Token para recuperar contraseña se generó correctamente",
        'username': user_found.username,
        'recovery': recovery_password
    }


def service_match_recovery(token : str, db: Session):
    try:
        user_found = user.get_user_by_recovery(token, db)
        if not user_found:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token no válido",
            ) 
        return {
            'message': "Token válido",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.detail}"
        )

def service_update_password(user_data: User, token: str, db: Session):
    try:
        user_found = user.get_user_by_recovery(token, db)
        if not user_found:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token no válido",
            ) 
        password_match = hashing.Hash.verify_password(user_data.password, user_found.password)
        if password_match:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña no puede ser igual a la anterior",
            )
        user_data.password = hashing.Hash.hash_password(user_data.password)
        user.update_user(user_data, user_found.id, db)
        recovery_password=hashing.Hash.hash_password(user_found.email)
        user.update_recovery(recovery_password, user_found.id, db)
        return {
            'message': "Contraseña actualizada correctamente",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.detail}"
        ) 

def generate_unique_username(db, user_provider):
    # Check if the current username is available
    if not user.get_user(db, user_provider.username):
        return user_provider.username

    # If the current username is taken, generate a new one
    while True:
        random_username = user_provider.username + str(np.random.randint(0, 1000))
        if not user.get_user(db, random_username):
            return random_username

def authenticate_user_check(db: Session, username: str, password: str):
    userData = user.get_user_check(db, username)
    if not userData:
        return False
    if not hashing.Hash.verify_password(password, userData.password):
        return False
    return userData

def authenticate_user_verify(db: Session, username: str, password: str):
    userData = user.get_user_verify(db, username)
    if not userData:
        return False
    if not hashing.Hash.verify_password(password, userData.password):
        return False
    return userData

def validar_lesson( lesson: Lesson ):
    image = process_image_from_base64(lesson.image)
    # valid if lesson.category is number or letter
    if lesson.category.strip() == "NUMEROS":
        result = gesture_recognition_number.get_gesture_prediction(image)
    else:
        result = gesture_recognition_letter.get_gesture_prediction(image)
    # result = gesture_recognition.get_gesture_prediction(image)   
    return result

def authenticate_and_create_token(db: Session, username: str, password: str):
        user = authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario o contraseña incorrectos",
                headers={'WWW.Authenticate': 'Bearer'}
            )
        user = authenticate_user_verify(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tu cuenta no está verificada"
            )

        access_token_expire = timedelta(minutes=int(config('ACCESS_TOKEN_EXPIRE_MINUTES')))
        access_token = Hash.create_access_token(
            data={'name': user.username, 'email': user.email},
            expires_delta=access_token_expire
        )

        return {
            'message': "Has iniciado sesión correctamente",
            'accessToken': access_token,
            'creation': user.creation.strftime("%Y-%m-%d"),
            'username': user.username,
            'email': user.email,
            'image': user.image,
            'id': user.id
        }

def service_update_user(user_update, current_user, db: Session):
    try:
        # Create a new UserUpdate object with the values that are different
        updated_values = {k: v for k, v in user_update.dict().items() if v is not None and current_user.get(k) != v}
        userData = user.get_user(db, current_user['username'])
        if not hashing.Hash.verify_password(updated_values['currentPassword'], userData.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña incorrecta"
            )
        updated_values.pop('currentPassword')
        if not updated_values:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No proporcionaste nueva información"
            )
        if updated_values.get('username'):
            user_conflict = user.get_user(db, user_update.username)
            if user_conflict:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El usuario no está disponible"
                )
        # remove the current password from the dictionary
        if updated_values.get('password'):
            updated_values['password'] = hashing.Hash.hash_password(updated_values['password'])
        updated_values = UserUpdate(**updated_values)
        user.update_user(updated_values, current_user['id'], db)
    except Exception as e:
        raise HTTPException(
            status_code=getattr(e, "status_code", status.HTTP_400_BAD_REQUEST),
            detail=f"{e.detail}"
        )
    
# PUNTAJE PERSONAL
def bring_personal_ranking_challenges_by_difficulty(db:Session, category: str, id: int):
    result = user.ranking_personal_challege_by_difficulty(db, category, id)
    result_dict = {
        'FACIL': {'dificultad': 'FACIL', 'retos': 0, 'lecciones': 0, 'puntos': 0, 'ranking': 0 },
        'MEDIO': {'dificultad': 'MEDIO', 'retos': 0, 'lecciones': 0, 'puntos': 0, 'ranking': 0 },
        'DIFICIL': {'dificultad': 'DIFICIL', 'retos': 0, 'lecciones': 0, 'puntos': 0, 'ranking': 0 }
    }
    columns = result.keys()
    for row in result:
        row_dict = dict(zip(columns, row))
        dificultad = row_dict['dificultad']
        result_dict[dificultad] = row_dict
    return result_dict