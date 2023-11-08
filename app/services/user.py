from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.utils import hashing
from app.utils import gesture
from app.utils.proccess import process_image_from_base64, get_prediction
from app.repository import user
from app.models import models
from app.schemas.schemas import UserInDB, Lesson
from app.models.models import User

model_path = "./model/sign_language_recognizer_25-04-2023.task"
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
            return { "username": new_user.username, "token": verify_hash }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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

def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

def get_user_check(db: Session, username: str, token: str):
    user = db.query(User).filter(User.username == username, User.token == token).first()
    return user

def get_user_verify(db: Session, username: str):
    user = db.query(User).filter(User.username == username, User.verified == True).first()
    return user
        
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not hashing.Hash.verify_password(password, user.password):
        return False
    return user

def authenticate_user_check(db: Session, username: str, password: str):
    user = get_user_check(db, username)
    if not user:
        return False
    if not hashing.Hash.verify_password(password, user.password):
        return False
    return user

def authenticate_user_verify(db: Session, username: str, password: str):
    user = get_user_verify(db, username)
    if not user:
        return False
    if not hashing.Hash.verify_password(password, user.password):
        return False
    return user

def validar_lesson( lesson: Lesson ):
    imagen = process_image_from_base64(lesson.imagen)
    result = gesture_recognition.get_gesture_prediction(imagen)   
    return result
