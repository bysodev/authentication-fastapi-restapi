from sqlalchemy.orm import Session 
from app.models.models import User

def crear_usuario(nuevo_usuario: User , db:Session):
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

def verify_user_by_token(token: str, db: Session):
    # Buscar el usuario por el token
    user = db.query(User).filter(User.token == token).first()

    if user:
        # Si se encuentra un usuario con el token, establecer 'verified' en True
        user.verified = True
        db.commit()
        return user
    else:
        # Si no se encuentra un usuario con el token, puedes manejar el error o retorno apropiado aquí.
        return None

def obtener_usuarios(db:Session):
    data = db.query(User).all()
    return data