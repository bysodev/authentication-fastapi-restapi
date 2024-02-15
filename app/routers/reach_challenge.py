from fastapi import HTTPException,APIRouter,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from sqlalchemy.orm import Session 
from decouple import config
from app.utils.hashing import Hash
from app.services.reach_challenge import service_new_reach_challenge, bring_reach_challenges, bring_reach_challanges_by_id, service_new_reach_customized_challenge 
import json
from app.schemas.schemas import SchemaReachChallenges, SchemaReachCustomizedChallenges


websocket_clients = []

router = APIRouter(
    prefix='/reach_challenge',
    tags=['Reach Challenges']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def new_reach_challenge(reach_challange: SchemaReachChallenges, current_user=Depends(Hash.get_current_active_user),  db: Session = Depends(get_db)):
    id_user = current_user['id']
    new_user_challenge = { 
        "id_user": id_user,
        "state": "COMPLETADO",
        **reach_challange.model_dump()
    }
    challange_created = service_new_reach_challenge(new_user_challenge,db)
    if not challange_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='Conflictos al crear este logro de reto')
    return {"respuesta":"Reach Challenge creado exitosamente", "data": challange_created}

@router.post('/customized/register', status_code=status.HTTP_201_CREATED)
def new_reach_challenge(reach_challange: SchemaReachCustomizedChallenges, current_user=Depends(Hash.get_current_active_user),  db: Session = Depends(get_db)):
    id_user = current_user['id']
    new_user_challenge_customized = { 
        "id_user": id_user,
        "state": "COMPLETADO",
        **reach_challange.model_dump()
    }
    print('DESDE AQUI LO PERSONALIZADO')
    challange_customized_created = service_new_reach_customized_challenge(new_user_challenge_customized,db)
    print(challange_customized_created)
    if not challange_customized_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='Conflictos al crear este logro de reto')
    return {"respuesta":"Reach Challenge Customized creado exitosamente", "data": challange_customized_created}

@router.get('/all', status_code=status.HTTP_200_OK)
def search_reach_challenges( db: Session = Depends(get_db)):
    return  bring_reach_challenges(db)

@router.get('/search/reach_challange/{reach_challange}', status_code=status.HTTP_200_OK)
def search_reach_challenge_by_user( reach_challange: int, db: Session = Depends(get_db)):
    if reach_challange == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Parametro vacio')
    
    return  bring_reach_challanges_by_id( db, reach_challange)