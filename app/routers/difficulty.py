from fastapi import HTTPException,APIRouter,Depends,status
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.services.difficulty import service_new_difficulty, bring_difficulties
from app.schemas.schemas import SchemaDifficulty

websocket_clients = []

router = APIRouter(
    prefix='/difficulty',
    tags=['Difficulties']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def new_difficulty(difficulty: SchemaDifficulty, db: Session = Depends(get_db)):
    difficulty_created = service_new_difficulty(difficulty,db)
    if not difficulty_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='Una categoria con es enombre ya existe')
    return {"respuesta":"Categoria creada exitosamente", "data": difficulty_created}

@router.get('/all', status_code=status.HTTP_200_OK)
def verify_user( db: Session = Depends(get_db) ):
    return  bring_difficulties( db )