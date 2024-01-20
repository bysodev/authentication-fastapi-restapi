from sqlalchemy.orm import Session 
from app.models.models import Difficulty

def create_difficulty(new_dificulty: Difficulty , db:Session):
    db.add(new_dificulty)
    db.commit()
    db.refresh(new_dificulty)

def get_difficultys(db: Session):
    difficultys = db.query(Difficulty).all()
    return difficultys

def get_difficulty(db: Session, name: str):
    dificulty = db.query(Difficulty).filter(Difficulty.name == name).first()
    return dificulty
