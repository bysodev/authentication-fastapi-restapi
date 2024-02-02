from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SchemaDifficulty(BaseModel):
    name: str
    bonus: int

class SchemaCategory(BaseModel):
    name: str

class SchemaReachChallenges(BaseModel):
    id_challenge: int
    points: float
    minutes: int
    seconds: int
    fails: int
    streak: int
    state: str

class SchemaChallenge(BaseModel):
    number: int
    name: str
    category_id: int
    difficulty_id: int
    description: str
    points: int
    minutes_max: int
    seconds_max: int
    fails_max: int
    random: bool
    operation: bool
    spelled: bool
    supplement: bool
    content: List[str]
      
class PredictSign(BaseModel):
    category: str
    image: str 
    extension: str
    type: str
    char: str

class User(BaseModel):
    username: str
    password: str
    email: str

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

class Lesson(BaseModel):
    name: str
    section_id: int
    description: str
    content: List[str]  # Permite tanto strings como integers en la lista
    points: int
    random: bool
    max_time: int

class User_lesson(BaseModel):
    id_lesson: int
    points_reached: int
    state_id: int
    fails: int
    detail_fails: List[str | int] 

class User_challenge(BaseModel):
    id_challenge: int
    points_reached: int
    fails: int
    detail_fails: List[str | int] 

class Section(BaseModel):
    name: str
    description: str
    category_id: int