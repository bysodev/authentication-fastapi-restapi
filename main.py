from fastapi import Depends, FastAPI, HTTPException, status
# ''' Necesario para temas de nuestros tokens '''
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# from jose import JWTError, jwt 
# from decouple import config
from app.routers import user
from app.db.database import Base,engine

# from passlib.context import CryptoContext
 

app = FastAPI()

app.include_router(user.router)


#---------------------------------- 

# class Data(BaseModel):
#     name: str
 
# @app.get('/prueba') 
# async def prueba():
#     return config('SECRET_KEY')

# @app.post('/receive')
# async def receive(data: Data): 
#     return {'data': data}

# @app.get("/test/{item_id}")
# async def test(item_id: str, query: int): # http://localhost:8000/test/Bryan?query=21
#     return {'Hello': item_id} 