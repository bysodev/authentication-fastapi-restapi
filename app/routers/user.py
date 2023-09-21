from fastapi import HTTPException,APIRouter,Depends,status, Response, Cookie
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
from app.services.user import service_crear_usuario, service_verified_usuario, service_view_usuarios, authenticate_user, validar_lesson, authenticate_user_verify

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: User, db: Session = Depends(get_db)):
    token_verif = service_crear_usuario(usuario,db)
    return {"respuesta":"Usuario creado satisfactoriamente!!", "username": token_verif["username"], "token": token_verif["token"]}

@router.get('/verified', status_code=status.HTTP_200_OK)
def verify_usuario( token: str, db: Session = Depends(get_db)):
    user = service_verified_usuario(token,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Token de verificación incorrecto')
    return {"respuesta":"Usuario verificado exitosamente"}

# @router.post('/token', response_model=Token)
@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print('HOLSAAAAAAAAAAAAAAAAA')
    print({form_data.username, form_data.password})
    # validar si el usuario esta en base (no si esta verificado)
    user = authenticate_user(db, form_data.username, form_data.password )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect username or password', 
                            headers={'WWW.Authenticate': 'Bearer'})

    # validar si el usuario esta en base (si esta verificado)
    user = authenticate_user_verify(db, form_data.username, form_data.password )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Su cuenta no esta verificada') 

    access_token_expire = timedelta(minutes= int( config('ACCESS_TOKEN_EXPIRE_MINUTES')) ) # secods=Para segundos
    # return access_token_expire
    access_token = Hash.create_access_token(data={'name': user.username, 'email': user.email}, expires_delta=access_token_expire)

    conteent = {'respuesta': 'Iniciandoe Sesión ', 'access_token': access_token, 'username': user.username, 'email': user.email , 'token_type': 'Bearer'}
    response = JSONResponse( content=conteent )
    response.set_cookie(key='toukenee', value=access_token, samesite='lax')
    return response
    # return {'access_token': access_token, 'token_type': 'Bearer'}

# @router.get('/users/me/', response_model=User)
@router.get('/users/me/')
async def read_users_me(current_user = Depends(Hash.get_current_active_user)):
    return current_user

@router.post('/lesson/vocales', status_code=status.HTTP_200_OK)
def consult_lesson(lesson: Lesson | None, current_user = Depends(Hash.get_current_active_user)):
    # print(lesson)
    validar_lesson(lesson)
    return 'OK'

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
    return service_view_usuarios(db)