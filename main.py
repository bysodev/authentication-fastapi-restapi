from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
# ''' Necesario para temas de nuestros tokens '''
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# from jose import JWTError, jwt 
# from decouple import config
from app.routers import user, challenge, category, difficulty, reach_challenge
from app.db.database import Base,engine




# from passlib.context import CryptoContext
 

app = FastAPI()

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print('Creación de tablas exitosa')
    except Exception as e:
        print(f'Existe un Error: {e}')

create_tables()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
    "*",
 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"]
)
app.include_router(user.router)
app.include_router(challenge.router )
app.include_router(reach_challenge.router )
app.include_router(category.router )
app.include_router(difficulty.router )

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
