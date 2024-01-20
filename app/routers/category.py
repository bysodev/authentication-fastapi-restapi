from fastapi import HTTPException,APIRouter,Depends,status
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.services.category import service_new_category, bring_categories
from app.schemas.schemas import SchemaCategory

websocket_clients = []

router = APIRouter(
    prefix='/category',
    tags=['Categories']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def new_category(category: SchemaCategory, db: Session = Depends(get_db)):
    category_created = service_new_category(category,db)
    if not category_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail='Una categoria con es enombre ya existe')
    return {"respuesta":"Categoria creada exitosamente", "data": category_created}

@router.get('/all', status_code=status.HTTP_200_OK)
def verify_user( db: Session = Depends(get_db) ):
    return  bring_categories( db )