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
        if user.verified == False:
            # Si se encuentra un usuario con el token, establecer 'verified' en True
            user.verified = True
            db.commit()
            return user
        else:
            return True
    else:
        # Si no se encuentra un usuario con el token, puedes manejar el error o retorno apropiado aquí.
        return False

def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

def get_user_check(db: Session, username: str, token: str):
    user = db.query(User).filter(User.username == username, User.token == token).first()
    return user

def get_user_verify(db: Session, username: str):
    user = db.query(User).filter(User.username == username, User.verified == True).first()
    return user

def get_user_by_name_or_email(user: User , db:Session):
    # Realiza una sola consulta para buscar al usuario por nombre de usuario o correo electrónico.
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    # Verifica si se encontró un usuario.
    if existing_user:
        return True
    else:
        return False
    
def get_user_by_name_and_email(user: User , db:Session):
    # Realiza una sola consulta para buscar al usuario por nombre de usuario o correo electrónico.
    existing_user = db.query(User).filter((User.username == user.username) & (User.email == user.email)).first()
    # Verifica si se encontró un usuario.
    if existing_user:
        return True
    else:
        return False