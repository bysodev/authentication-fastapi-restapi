from sqlalchemy.orm import Session 
from app.models.models import User

def crear_usuario(nuevo_usuario: User , db:Session):
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

def obtener_usuarios(db:Session):
    data = db.query(User).all()
    return data