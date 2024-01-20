from sqlalchemy.orm import Session 
from app.models.models import Category

def create_category(new_category: Category , db:Session):
    print(f'Vamos a insertar la nueva categoria: {new_category}')
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

def get_categories(db: Session):
    categorys = db.query(Category).all()
    return categorys

def get_category(db: Session, name: str):
    challenge = db.query(Category).filter(Category.name == name ).first()
    return challenge
