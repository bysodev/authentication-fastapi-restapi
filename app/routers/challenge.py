from typing import Annotated, Any, Dict
from fastapi import HTTPException,APIRouter,Depends,status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.schemas import User, Lesson
from app.db.database import get_db
from sqlalchemy.orm import Session 
from datetime import timedelta
from decouple import config
from app.utils.hashing import Hash
from app.services.challenge import bring_challanges_by_category, service_new_challenge, bring_challenge, bring_challanges_by_user, bring_ranking_challenges_by_difficulty
import json
from app.schemas.schemas import SchemaChallenge


websocket_clients = []

router = APIRouter(
    prefix='/challenge',
    tags=['Challenges']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def new_challenge(challange: SchemaChallenge, db: Session = Depends(get_db)):
    challange_created = service_new_challenge(challange,db)
    if not challange_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='Un reto con el numero, nombre y categoria ya existe')
    return {"respuesta":"Challenge creado exitosamente", "data": challange_created}

@router.get('/all', status_code=status.HTTP_200_OK)
def search_challenges( db: Session = Depends(get_db)):
    return  bring_challenge( db )

@router.get('/search/', status_code=status.HTTP_200_OK)
def search_challenge_by_name( challenge: str, db: Session = Depends(get_db)):
    if challenge == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Parametro vacio')
    data = bring_challanges_by_category( db, challenge)
    return {"respuesta":"Challenge buscados correctamente", "data": data}

@router.get('/search/me', status_code=status.HTTP_200_OK)
def search_challenge_by_user( category: str, db: Session = Depends(get_db), current_user = Depends(Hash.get_current_user)):
    if category == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Parametro vacio')
    
    return bring_challanges_by_user( category, current_user.id, db )

@router.get('/ranking', status_code=status.HTTP_200_OK)
def search_ranking_challenge_by_user(  category: str, db: Session = Depends(get_db)):
    if category == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Falta el parametro de Categoria')
    
    return bring_ranking_challenges_by_difficulty(db, category)
