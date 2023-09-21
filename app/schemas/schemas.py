from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Lesson(BaseModel):
    learn: str
    imagen: str 
    extension: str
    vocal: str
    tipo: str

class User(BaseModel):
    username: str
    password: str
    email: str

# class UserVerify():



class UserCors(BaseModel):
    nombre: str
    apellido: str
    email: str
    estado: bool

class UserInDB(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nombre: str or None = None
    
# class UpdateUser(BaseModel): #Schema 
#     username:str = None 
#     password:str = None 
#     nombre:str = None 
#     apellido:str = None 
#     direccion:str = None 
#     telefono:int = None 
#     correo:str = None 

'''En este caso, se establece orm_mode = True en la configuración. Esto indica que el modelo se utilizará en el contexto de una consulta a la base de datos mediante SQLAlchemy, y permite que los atributos del modelo se muestren en modo ORM, lo que facilita la conversión de los resultados de la consulta en objetos de tipo ShowUser.'''
# class ShowUser(BaseModel):
#     username:str 
#     nombre:str 
#     correo:str 
#     class Config():
#         orm_mode = True 