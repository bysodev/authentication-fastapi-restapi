from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from app.models.models import Section

def create_section(new_section: Section , db:Session):
    db.add(new_section)
    db.commit()
    db.refresh(new_section)
    
def get_lesson_by_number(number: int, db: Session):
    return db.query(Section).filter(Section.number == number).first()

def get_all(db: Session):
    return db.query(Section).all()