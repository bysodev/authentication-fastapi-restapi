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
from app.services.user import service_crear_usuario, service_view_usuarios, authenticate_user, validar_lesson

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.get('/prueba', status_code=status.HTTP_200_OK)
def get_usu(touken: Annotated[str | None, Cookie()] = None ):
    print({'touken: ': touken})
    return {touken}

@router.post('/', status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario:User,db:Session = Depends(get_db)):
    service_crear_usuario(usuario,db)
    return {"respuesta":"Usuario creado satisfactoriamente!!"}

@router.get('/', status_code=status.HTTP_200_OK)
def get_usuarios(response: Response, db:Session=Depends(get_db),token: Annotated[str | None, Cookie()] = None ):
    # response.set_cookie(key='token_siuu', value='SIUUUUUUUUUUUU', secure=False, samesite='lax', httponly=False, domain='http://localhost:3000')
    print(token)
    return {'token': token}
    return service_view_usuarios(db)

# @router.post('/token', response_model=Token)
@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print('HOLSAAAAAAAAAAAAAAAAA')
    print({form_data.username, form_data.password})
    user = authenticate_user(db, form_data.username, form_data.password )
    # return user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect username or password', 
                            headers={'WWW.Authenticate': 'Bearer'})
    # return user

    access_token_expire = timedelta(minutes= int( config('ACCESS_TOKEN_EXPIRE_MINUTES')) ) # secods=Para segundos
    # return access_token_expire
    access_token = Hash.create_access_token(data={'sub': user.nombre}, expires_delta=access_token_expire)

    conteent = {'access_token': access_token, 'token_type': 'Bearer'}
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
