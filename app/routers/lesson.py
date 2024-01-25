from fastapi import HTTPException,APIRouter,Depends,status
from app.schemas.schemas import Lesson
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.services.lesson import service_get_category_by_number, service_get_state_by_user_lesson, service_new_lesson, service_get_by_number, service_get_all
from fastapi import HTTPException

from app.utils.hashing import Hash

router = APIRouter(
    prefix='/lesson',
    tags=['Lesson']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def new_lesson(lesson: Lesson, db: Session = Depends(get_db)):
    """
    Create a new lesson.

    Args:
        lesson (Lesson): The lesson object containing the lesson details.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        The created lesson.
    """
    try:
        created_lesson = service_new_lesson(lesson, db)
        return {
            "data": created_lesson,
            "message": "Lección creada correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/get/by/number', status_code=status.HTTP_200_OK)
def get_by_number(number: int, db: Session = Depends(get_db)):
    """
    Retrieve a lesson by its number.

    Args:
        number (int): The number of the lesson.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the lesson data, status code, and message.

    Raises:
        HTTPException: If the lesson is not found or an internal server error occurs.
    """
    try:
        lesson = service_get_by_number(number, db)
        if lesson is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se ha encontrado la lección")
        return {
            "data": lesson,
            "message": "Lección recuperada con éxito"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/get/lessonCategory/by/number', status_code=status.HTTP_200_OK)
def get_by_number(number: int, db: Session = Depends(get_db)):
    """
    Retrieve a lesson category by its number.

    Args:
        number (int): The number of the lesson category.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the lesson category data, status code, and message.

    Raises:
        HTTPException: If the lesson category is not found or if there is a server error.
    """
    try:
        lesson = service_get_category_by_number(number, db)
        if lesson is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se ha encontrado la lección")
        lesson_dict = {key: getattr(lesson.Lesson, key) for key in lesson.Lesson.__dict__ if not key.startswith('_')}
        lesson_dict["category_name"] = lesson.category_name.name
        return {
            "data": lesson_dict,
            "message": "Categoría de lección recuperada correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get('/get', status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    """
    Retrieve all lessons from the database.

    Args:
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the retrieved lessons, status code, and message.
    """
    try:
        lessons = service_get_all(db)
        return {
            "data": lessons,
            "message": "Todas las lecciones se recuperaron con éxito"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get('/get/by/user_lesson', status_code=status.HTTP_200_OK)
def get_state_by_user_lesson(id_lesson: int, current_user = Depends(Hash.get_current_active_user), db: Session = Depends(get_db)):
    try:
        user_lesson = service_get_state_by_user_lesson(id_lesson, current_user['id'], db)
        return {
            "data": user_lesson,
            "message": "Lecciones recuperadas correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))