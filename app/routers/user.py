from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.schemas import User, PredictSign, User_lesson
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.user_lesson import service_create_new, service_update_user_lesson
from app.utils.hashing import Hash
from app.services.user import (
    authenticate_and_create_token,
    service_new_user,
    service_verified_user,
    authenticate_user,
    authenticate_user_provider,
    validar_lesson,
    authenticate_user_verify,
)

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def new_user(user: User, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (User): User data.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Response data.
    """
    user_created = service_new_user(user, db)
    if not user_created:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='El usuario y/o correo electrónico ya se encuentran registrados'
        )
    return JSONResponse(
        content={
            "data": user_created,
            "message": "Usuario creado exitosamente"
        }
    )

@router.get('/verified', status_code=status.HTTP_200_OK)
def verify_user(token: str, db: Session = Depends(get_db)):
    """
    Verify a user.

    Args:
        token (str): Verification token.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Response data.
    """
    user = service_verified_user(token, db)

    if user == True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='El usuario ya está verificado'
        )
    if user == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token de verificación incorrecto'
        )
    return JSONResponse(
        content={
            "data": user,
            "message": "Usuario verificado exitosamente"
        }
    )

@router.post('/login', status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login to get an access token.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Form data. Defaults to Depends().
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        JSONResponse: Response data.
    """
    body = authenticate_and_create_token(db, form_data.username, form_data.password)
    return JSONResponse(content=body)

@router.get('/users/me')
async def read_users_me(current_user=Depends(Hash.get_current_active_user)):
    """
    Get the current user.

    Args:
        current_user (User, optional): Current user. Defaults to Depends(Hash.get_current_active_user).

    Returns:
        User: Current user.
    """
    return JSONResponse(
        content={
            "data": current_user,
            "message": "Usuario recuperado con éxito"
        }
    )

@router.post('/lesson/predict', status_code=status.HTTP_200_OK)
async def consult_lesson(lesson: PredictSign, current_user=Depends(Hash.get_current_active_user)):
    """
    Consult a lesson.

    Args:
        lesson (PredictSign): Lesson data.

    Returns:
        dict: Response data.
    """
    try:
        if isinstance(lesson, dict):
            lesson = PredictSign(
                category=lesson['category'],
                image=lesson['image'],
                extension=lesson['extension'],
                type=lesson['type'],
                char=lesson['char']
            )
        result = validar_lesson(lesson)
        if result is None:
            return JSONResponse(
            content={
                "data": {"result": "none"},
                "message": "No se ha podido identificar la seña procesada"
            }
            )

        # Realiza otras validaciones aquí si es necesario
        return JSONResponse(
            content={
                "data": result,
                "message": "Lección recuperada con éxito"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post('/register/user_lesson', status_code=status.HTTP_201_CREATED)
async def new_user_lesson(user_lesson: User_lesson, current_user=Depends(Hash.get_current_active_user), db: Session = Depends(get_db)):
    """
    Register a new user lesson.

    Args:
        user_lesson (User_lesson): User lesson data.
        current_user (User, optional): Current user. Defaults to Depends(Hash.get_current_active_user).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Response data.
    """
    try:
        # Agrega el id del usuario actual al objeto user_lesson
        id_user = current_user['id']
        new_user_lesson = {
            "id_user": id_user,
            "last_points_reached": 0,
            **user_lesson.model_dump()
        }
        result = service_create_new(new_user_lesson, db)
        # Realiza otras validaciones aquí si es necesario
        return JSONResponse(
            content={
                "data": result,
                "message": "Lección registrada con éxito"
            },
            status_code=status.HTTP_201_CREATED
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put('/update/user_lesson')
async def update_user_lesson(user_lesson: User_lesson, current_user=Depends(Hash.get_current_active_user), db: Session = Depends(get_db)):
    try:
        status_update = service_update_user_lesson(user_lesson, current_user['id'], db)
        return status_update
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
