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

def service_crear_usuario(usuario, db: Session):
    usuario = usuario.dict()
    password_hash = hashing.Hash.hash_password(usuario["password"]),
    verify_hash = hashing.Hash.hash_verify()
    print(verify_hash)
    try:
        nuevo_usuario = models.User(
            username=usuario["username"],
            password=password_hash,
            email=usuario["email"],
            token=verify_hash
        )
        user.crear_usuario(nuevo_usuario, db)
        return { "username": usuario["username"], "token": verify_hash }
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error creando usuario {e}"
        )

def service_verified_usuario(token: str, db: Session):
    print(token)
    try:
        return user.verify_user_by_token(token, db)
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error verificando usuario {e}"
        )

def service_view_usuarios(db:Session):
    data = db.query(User).all()
    return data
    # user.obtener_usuarios(db)

# def get_user(db: Session, nombre: str):
#     if nombre in db:
#         user_data = db[nombre]
#         return UserInDB(**user_data)

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
