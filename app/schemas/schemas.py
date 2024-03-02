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

class SchemaReachCustomizedChallenges(BaseModel):
    category: str
    difficulty: str
    minutes_max: int
    seconds_max: int
    minutes: int
    seconds: int
    lives: int
    fails: int

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
    username: str = None
    password: str = None
    email: str = None
    image: str = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    image: Optional[str] = None
    currentPassword: Optional[str] = None
    password: Optional[str] = None
    only: Optional[bool] = None

class RecoveryRequest(BaseModel):
    email: str

class UserInDB(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nombre: str or None = None

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

class Provider(BaseModel):
    username: str
    password: str
    email: str
    image: str
    provider_name: str