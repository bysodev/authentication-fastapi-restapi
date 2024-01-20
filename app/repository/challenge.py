from sqlalchemy.orm import Session 
from app.models.models import Challenges, ReachChallenges, Category, Difficulty
from sqlalchemy import func

def create_challenge(new_challenge: Challenges , db:Session):
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)

def get_challenges(db: Session):
    challenges = db.query(Challenges).all()
    return challenges

def get_challenges_by_category(db: Session, category: str):
    challenges = db.query(Challenges).filter(Challenges.category == category)
    return challenges

def get_challenges_by_user_and_difficulty(db: Session, id: int):
    challenges = db.query(Category.name.label('categoria'), Difficulty.name.label('dificultad'), func.count( Challenges.id ).label('total') , func.count( ReachChallenges.id ).label('progreso'), func.sum( Challenges.points ).label('puntos') ).outerjoin(ReachChallenges, ( Challenges.id == ReachChallenges.id_challenge ) & ( ReachChallenges.id_user == id ) ).join(Category, (Challenges.category_id == Category.id) ).join(Difficulty, (Challenges.difficulty_id == Difficulty.id)).group_by(Challenges.category_id, Category.name, Difficulty.name) .all()
    return challenges 

def get_challenges_by_user(db: Session, category: str, id: int):
    # challenges = db.query(Challenges.number, ReachChallenges.end_points).outerjoin(ReachChallenges, ReachChallenges.id_challenge == Challenges.id).all()
    challenges = db.query(Challenges, ReachChallenges.end_points, ReachChallenges.state.label('reach_state'), ReachChallenges.minutes, Difficulty.name.label('diffyculty_name'), Category.name.label('category_name')).outerjoin(ReachChallenges, ( Challenges.id == ReachChallenges.id_challenge ) & ( ReachChallenges.id_user == id ) ).join(Category, (Challenges.category_id == Category.id) & ( Category.name == category )).join(Difficulty, (Challenges.difficulty_id == Difficulty.id)).all()

    return challenges 

def get_challenge(db: Session, number: int, name: str):
    challenge = db.query(Challenges).filter((Challenges.number == number) | (Challenges.name == name)).first()
    return challenge
