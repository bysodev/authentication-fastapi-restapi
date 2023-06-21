from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import JWTError, jwt
from decouple import config
from app.schemas.schemas import TokenData, UserInDB, Token
from app.services.user import get_user
from app.db.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #Se configura el contexto para utilizar el esquema de hash "bcrypt" y se permite la detección automática de esquemas hash desaprobados.
oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')

class Hash():
    
    def hash_password(password):
        return pwd_context.hash(password)
    
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token( data: dict, expires_delta: timedelta or None = None ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow * timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, config('SECRET_KEY'), algorithm=config('ALGORITMO'))
        return encode_jwt
    
    async def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail='Could not validate credentials', headers={'WWW.Authenticate': 'Bearer'})
        try:
            payload = jwt.decode(token, config('SECRET_KEY'), algorithms=[config('ALGORITMO')])
            nombre: str = payload.get('sub')
            if nombre is None:
                raise credential_exception
            # token_data = TokenData(nombre)
        except JWTError:
            raise credential_exception
        
        user = get_user(db, nombre=nombre)
        # user = get_user(db, nombre=token_data.nombre)
        if user is None:
            raise credential_exception
        
        return user
    
    async def get_current_active_user(current_user = Depends(get_current_user)):
        if current_user.estado:
            raise HTTPException(status_code=400, detail='Inactive user')
        return current_user