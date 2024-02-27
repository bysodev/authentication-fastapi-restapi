from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.schemas import Provider, RecoveryRequest, User, PredictSign, User_lesson, UserUpdate
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.user_lesson import service_create_new, service_update_user_lesson
from app.utils.hashing import Hash
from app.services.user import (
    authenticate_and_create_token,
    authenticate_user_provider,
    service_match_recovery,
    service_new_user,
    service_recovery_password,
    service_update_password,
    service_update_user,
    service_verified_user,
    validar_lesson,
    bring_personal_ranking_challenges_by_difficulty
)

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.get('/ranking', status_code=status.HTTP_200_OK)
def search_ranking_challenge_by_user( category: str, current_user=Depends(Hash.get_current_active_user), db: Session = Depends(get_db)):
    id_user = current_user['id']
    if category == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Falta el parametro de Categoria')
    
    return bring_personal_ranking_challenges_by_difficulty(db, category, id_user)


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
        },
        status_code=201
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

@router.post('/loginProvider',  status_code=status.HTTP_201_CREATED)
def login_for_oauth_provider(user: Provider, db: Session = Depends(get_db)):
    user = authenticate_user_provider(user, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos",
            headers={'WWW.Authenticate': 'Bearer'}
        )
    return user

@router.post('/recovery', status_code=status.HTTP_200_OK)
def recovery_password(recovery_body: RecoveryRequest, db: Session = Depends(get_db)):
    """
    Recover a password.

    Args:
        email (str): User email.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Response data.
    """
    try:
        return service_recovery_password(recovery_body.email, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get('/recovery', status_code=status.HTTP_200_OK)
def recovery_password(token: str, db: Session = Depends(get_db)):
    """
    Recover a password.

    Args:
        token (str): Recovery token.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Response data.
    """
    return service_match_recovery(token, db)

@router.put('/recovery', status_code=status.HTTP_201_CREATED)
def recovery_password(user_data: User, token: str, db: Session = Depends(get_db)):
    """
    Recover a password.

    Args:
        token (str): Recovery token.
        new_password (str): New password.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Response data.
    """
    return service_update_password(user_data, token, db)

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
    return {"respuesta":"Usuario verificado exitosamente"}

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

@router.put('/profile')
async def update_user(user_update: UserUpdate, current_user=Depends(Hash.get_current_active_user), db: Session = Depends(get_db)):
    """
    Update user profile.

    Args:
        user_update (UserUpdate): The updated user information.
        current_user: The current authenticated user.
        db (Session): The database session.

    Raises:
        HTTPException: If there is an error updating the user profile.

    Returns:
        None
    """
    try:
        service_update_user(user_update, current_user, db)
        body = Hash.create_access_token(
            data={'name': user_update.username, 'email': current_user["email"]}
        )
        return JSONResponse(content={'message': "Usuario actualizado correctamente", 'refreshToken': body}, status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={'error': str(e)}
        )
    

@router.post("/refreshToken")
async def refresh_access_token(name:str, email: str):
    try:
        body = Hash.create_access_token(
            data={'name': name, 'email': email}
        )
        return JSONResponse(content={'message': "Token actualizado correctamente", 'refreshToken': body}, status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={'error': str(e)}
        )