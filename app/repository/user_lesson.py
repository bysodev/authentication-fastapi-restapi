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
        .all()
    )
    return user_lesson

def get_user_lesson_by_lesson_id_and_user_id(lesson_id: int, user_id: int, db: Session):
    return db.query(User_lesson).filter(User_lesson.id_lesson == lesson_id, User_lesson.id_user == user_id).first()

def update_user_lesson(user_lesson_id: int, state_id: int, score: int, fails: int, detail_fails: list, db: Session):
    user_lesson = db.query(User_lesson).filter(User_lesson.id == user_lesson_id).first()
    if user_lesson:
        user_lesson.state_id = state_id
        user_lesson.fails = fails
        user_lesson.detail_fails = detail_fails
        user_lesson.last_points_reached = score
        db.commit()
        db.refresh(user_lesson)