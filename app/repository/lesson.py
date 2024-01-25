from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from app.models.models import Category, Lesson, Section, State, User_lesson

def create_lesson(new_lesson: Lesson , db:Session):
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    
def get_lesson_by_number(number: int, db: Session):
    return db.query(Lesson).filter(Lesson.id == number).first()

def get_lesson_category_by_number(number: int, db: Session):
    lesson_category = (
        db.query(Lesson,  Category.name.label('category_name'))
        .join(Section, Lesson.section_id == Section.id)
        .join(Category, Section.category_id == Section.id)
        .filter(Lesson.id == number)
        .first()
    )
    return lesson_category

def get_all(db: Session):
    return db.query(Lesson).all()

def get_lessons_by_section(section_id: int, db: Session):
    return db.query(Lesson).filter(Lesson.section_id == section_id).all()

def get_state_by_user_lesson(id_lesson: int, id_user: int, db: Session):
    return db.query(Lesson, User_lesson).join(User_lesson, Lesson.id == User_lesson.id_lesson).filter(User_lesson.id_lesson == id_lesson, User_lesson.id_user == id_user).first()
    # return db.query(Lesson, State).join(State, Lesson.state_id == State.id).filter(Lesson.id == lesson_id, State.id_user == user_id).first()