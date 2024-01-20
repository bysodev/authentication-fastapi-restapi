from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from app.models.models import Category, Lesson, Section

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