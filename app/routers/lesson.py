from fastapi import HTTPException,APIRouter,Depends,status, WebSocket, WebSocketDisconnect
from app.schemas.schemas import Lesson
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.services.lesson import service_get_category_by_number, service_new_lesson, service_get_by_number, service_get_all

router = APIRouter(
    prefix='/lesson',
    tags=['Lesson']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def new_lesson(lesson: Lesson, db: Session = Depends(get_db)):
    return service_new_lesson(lesson,db)

@router.get('/get/by/number', status_code=status.HTTP_200_OK)
def get_by_number(number: int, db: Session = Depends(get_db)):
    lesson = service_get_by_number(number,db)
    if lesson is None:
            raise HTTPException(status_code=400, detail="No se ha encontrado la lección")
    return lesson

@router.get('/get/lessonCategory/by/number', status_code=status.HTTP_200_OK)
def get_by_number(number: int, db: Session = Depends(get_db)):
    lesson = service_get_category_by_number(number, db)
    if lesson is None:
        raise HTTPException(status_code=400, detail="No se ha encontrado la lección")
    lesson_dict = {key: getattr(lesson.Lesson, key) for key in lesson.Lesson.__dict__ if not key.startswith('_')}
    lesson_dict["category_name"] = lesson.category_name.name

    return lesson_dict

@router.get('/get', status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    return service_get_all(db)

