from typing import Annotated, Any, Dict
from fastapi import HTTPException,APIRouter,Depends,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.schemas import User, PredictSign, User_lesson
from app.db.database import get_db
from sqlalchemy.orm import Session 
from datetime import timedelta
from decouple import config
from app.services.user_lesson import service_create_new
from app.utils.hashing import Hash
from app.services.user import service_new_user, service_verified_user, authenticate_user, authenticate_user_provider, validar_lesson, authenticate_user_verify
import json

websocket_clients = []

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def new_user(user: User, db: Session = Depends(get_db)):
    user_created = service_new_user(user,db)
    if not user_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='El usuario y/o correo electrónico ya se encuentran registrados')
    return {"respuesta":"Usuario creado exitosamente", "username": user_created["username"], "token": user_created["token"]}

@router.get('/verified', status_code=status.HTTP_200_OK)
def verify_user( token: str, db: Session = Depends(get_db)):
    user = service_verified_user(token,db)
    
    if user == True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='El usuario ya está verificado')
    if user == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Token de verificación incorrecto')
    return {"respuesta":"Usuario verificado exitosamente"}

@router.post('/login')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos",
            headers={'WWW.Authenticate': 'Bearer'}
        )
    user = authenticate_user_verify(db, form_data.username, form_data.password )

    if not user:  # Asumiendo que hay un atributo 'is_verified' no es válido
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Su cuenta no está verificada')

    access_token_expire = timedelta(minutes=int(config('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = Hash.create_access_token(data={'name': user.username, 'email': user.email}, expires_delta=access_token_expire)
    # access_token = Hash.create_access_token(data={'name': user.username}, expires_delta=access_token_expire)
    body = {'message': 'Se ha iniciado sesión correctamente', 'accessToken': access_token, 'creation': user.creation.strftime("%Y-%m-%d") , 'username': user.username, 'email': user.email, 'token_type': 'Bearer', 'id': user.id}
    response = JSONResponse(content=body)

    return response

@router.get('/users/me')
async def read_users_me(current_user = Depends(Hash.get_current_active_user)):
    return current_user

@router.post('/lesson/predict', status_code=status.HTTP_200_OK)
async def consult_lesson(lesson: PredictSign):
    try:
        if isinstance(lesson, dict):
            lesson = PredictSign(
                category=lesson['category'],
                image=lesson['image'],
                extension=lesson['extension'],
                type=lesson['type'],
                char=lesson['char']
            )
        result = validar_lesson(lesson)
        if result is None:
            raise HTTPException(status_code=400, detail="No se ha podido identificar la seña procesada")
        # Realiza otras validaciones aquí si es necesario
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/register/user_lesson', status_code=status.HTTP_201_CREATED)
async def new_user_lesson(user_lesson: User_lesson, current_user = Depends(Hash.get_current_active_user), db: Session = Depends(get_db)):
    try:
         # Agrega el id del usuario actual al objeto user_lesson
        user_lesson.id_user = current_user.id
        result = service_create_new(user_lesson, db)
        if result is None:
            raise HTTPException(status_code=400, detail="No se ha podido guardar la lección")
        # Realiza otras validaciones aquí si es necesario
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))