from sqlalchemy.orm import Session 
from app.models.models import ReachChallenges

def create_reach_challenge(new_reach_challenge: ReachChallenges , db:Session):
    db.add(new_reach_challenge)
    db.commit()
    db.refresh(new_reach_challenge)

def get_reach_challenges(db: Session):
    challenges = db.query(ReachChallenges).all()
    return challenges

def get_reach_challenge(db: Session, id: int):
    dificulty = db.query(ReachChallenges).filter(ReachChallenges.id == id).first()
    return dificulty

def get_reach_challenge_by_user(db: Session, id: int):
    dificulty = db.query(ReachChallenges).filter(ReachChallenges.id_user == id).first()
    return dificulty

def get_reach_challenge_by_challenge(db: Session, id: int):
    dificulty = db.query(ReachChallenges).filter(ReachChallenges.id_challenge == id).first()
    return dificulty