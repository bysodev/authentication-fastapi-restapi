from fastapi import HTTPException,APIRouter,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from sqlalchemy.orm import Session 
from decouple import config
from app.utils.hashing import Hash
from app.services.reach_challenge import service_new_reach_challenge, bring_reach_challenges, bring_reach_challanges_by_id
import json
from app.schemas.schemas import SchemaReachChallenges


websocket_clients = []

router = APIRouter(
    prefix='/reach_challenge',
    tags=['Reach Challenges']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def new_reach_challenge(reach_challange: SchemaReachChallenges, db: Session = Depends(get_db)):
    challange_created = service_new_reach_challenge(reach_challange,db)
    if not challange_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='Conflictos al crear este logro de reto')
    return {"respuesta":"Reach Challenge creado exitosamente", "data": challange_created}

@router.get('/all', status_code=status.HTTP_200_OK)
def search_reach_challenges( db: Session = Depends(get_db)):
    return  bring_reach_challenges(db)

@router.get('/search/reach_challange/{reach_challange}', status_code=status.HTTP_200_OK)
def search_reach_challenge_by_user( reach_challange: int, db: Session = Depends(get_db)):
    if reach_challange == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Parametro vacio')
    
    return  bring_reach_challanges_by_id( db, reach_challange)