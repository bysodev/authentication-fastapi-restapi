from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.utils import hashing
from app.repository import user
from app.models import models
from app.schemas.schemas import UserInDB
from app.models.models import User

def service_crear_usuario(usuario, db: Session):
    usuario = usuario.dict()
    password_hash = hashing.Hash.hash_password(usuario["password"]),
    try:
        nuevo_usuario = models.User(
            # username=usuario["username"],
            # password=Hash.hash_password(usuario["password"]),
            password=password_hash,
            nombre=usuario["nombre"],
            apellido=usuario["apellido"],
            direccion=usuario["direccion"],
            telefono=usuario["telefono"],
            email=usuario["email"],
        )
        user.crear_usuario(nuevo_usuario, db)
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error creando usuario {e}"
        )

def service_view_usuarios(db:Session):
    data = db.query(User).all()
    return data
    # user.obtener_usuarios(db)

# def get_user(db: Session, nombre: str):
#     if nombre in db:
#         user_data = db[nombre]
#         return UserInDB(**user_data)

def get_user(db: Session, nombre: str):
    user = db.query(User).filter(User.nombre == nombre).first()
    return user
        
def authenticate_user(db: Session, nombre: str, password: str):
    user = get_user(db, nombre)
    if not user:
        return False
    if not hashing.Hash.verify_password(password, user.password):
        return False
    
    return user

