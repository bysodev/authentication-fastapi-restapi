from fastapi import HTTPException,APIRouter,Depends,status, Response, Cookie, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.schemas import User, Token, Lesson
from app.db.database import get_db
from sqlalchemy.orm import Session 
from datetime import datetime, timedelta
from typing import List
from decouple import config
from app.utils.hashing import Hash
from app.services.user import service_new_user, service_verified_user, get_user, authenticate_user, validar_lesson, authenticate_user_verify
import json
import concurrent.futures

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
            detail='Su cuenta no está verificada'
        )

    access_token_expire = timedelta(minutes=int(config('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = Hash.create_access_token(data={'name': user.username, 'email': user.email}, expires_delta=access_token_expire)

    body = {'message': 'Se ha iniciado sesión correctamente', 'token': access_token, 'username': user.username, 'email': user.email, 'token_type': 'Bearer', 'id': user.id}
    response = JSONResponse(content=body)

    return response

@router.get('/users/me/')
async def read_users_me(current_user = Depends(Hash.get_current_active_user)):
    return current_user

@router.post('/lesson/vocales', status_code=status.HTTP_200_OK)
async def consult_lesson(lesson: Lesson | None, current_user = Depends(Hash.get_current_active_user)):
    try:
        if isinstance(lesson, dict):
            lesson = Lesson(
                learn=lesson['learn'],
                imagen=lesson['imagen'],
                extension=lesson['extension'],
                tipo=lesson['tipo'],
                vocal=lesson['vocal']
            )
        result = validar_lesson(lesson)
        if result is None:
            raise HTTPException(status_code=400, detail="No se ha podido identificar la seña procesada")
        # Realiza otras validaciones aquí si es necesario
        print(result)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ruta WebSocket para la clasificación de imágenes en tiempo real
@router.websocket("/ws/lesson/vocales")
async def classify_images(websocket: WebSocket):
    await websocket.accept()
    # Agrega el cliente WebSocket a la lista de clientes conectados
    websocket_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)
            result = await consult_lesson(data_dict)
            # Envía el resultado de la clasificación de la imagen de vuelta al cliente
            await websocket.send_json(result)
    except WebSocketDisconnect:
        # Cuando el cliente se desconecta, elimina el WebSocket de la lista de clientes
        websocket_clients.remove(websocket)


# PRUEBA

@router.get('/prueba', status_code=status.HTTP_200_OK)
def get_usu(touken: Annotated[str | None, Cookie()] = None ):
    print({'touken: ': touken})
    return {touken}

@router.get('/', status_code=status.HTTP_200_OK)
def get_usuarios(response: Response, db:Session=Depends(get_db),token: Annotated[str | None, Cookie()] = None ):
    # response.set_cookie(key='token_siuu', value='SIUUUUUUUUUUUU', secure=False, samesite='lax', httponly=False, domain='http://localhost:3000')
    print(token)
    return {'token': token}
