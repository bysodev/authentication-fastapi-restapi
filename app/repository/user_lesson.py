from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from app.models.models import Lesson, State, User_lesson

def create_new(new_section: User_lesson , db:Session):
    db.add(new_section)
    db.commit()
    db.refresh(new_section)
    
def get_by_number(number: int, db: Session):
    return db.query(User_lesson).filter(User_lesson.number == number).first()

def get_all(db: Session):
    return db.query(User_lesson).all()

def get_detail_user_lesson(user_id: int, section_id: int, db: Session):
    user_lesson = (
        db.query(User_lesson,  State.name.label('state_name'))
        .join(Lesson, User_lesson.id_lesson == Lesson.id)
        .join(State, User_lesson.state_id == State.id)
        .filter(User_lesson.id_user == user_id, Lesson.section_id == section_id)
        .first()
    )
    return user_lesson