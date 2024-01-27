import datetime
from fastapi import HTTPException, status
import numpy as np
from sqlalchemy.orm import Session
from app.utils import hashing
from app.utils import gesture
from app.utils.proccess import improve_lighting, normalize, process_image_from_base64, resize, segment_hand, subtract_background
from app.repository import user
from app.models import models
from app.schemas.schemas import User_lesson, UserInDB, Lesson
from app.models.models import User
from decouple import config
from datetime import timedelta
from app.utils.hashing import Hash

model_path = "./model/gesture_recognizer.task"
gesture_recognition = gesture.GestureRecognitionService(model_path)

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

def authenticate_user_provider(db: Session, username: str, email: str, id: str):
    userData = user.get_user_by_name_and_email(db, username, email)
    if not userData:
        return False
    if not hashing.Hash.verify_password(id, userData.password):
        return False
    return userData

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
    result = gesture_recognition.get_gesture_prediction(image)   
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
            'id': user.id
        }