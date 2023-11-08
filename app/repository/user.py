from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from app.models.models import User

def create_user(new_user: User , db:Session):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

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
    
def get_user_by_name_or_email(user: User , db:Session):
    # Realiza una sola consulta para buscar al usuario por nombre de usuario o correo electrónico.
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    # Verifica si se encontró un usuario.
    if existing_user:
        return True
    else:
        return False