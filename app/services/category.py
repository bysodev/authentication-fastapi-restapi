from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import category
from app.models import models

def service_new_category(new_category, db: Session):
    category_dict = new_category.dict()
    print( category_dict )

    try:
        new_category = models.Category(**category_dict)
       
        if not category.get_category(db, category_dict["name"] ):
            category.create_category(new_category, db)
            return category_dict
    except Exception as e:
        print(f"Error al crear el reto {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la Categoria {e}"
        )

def bring_categories( db: Session ):
    try:
        return category.get_categories( db )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al hacer la busqueda de las categroias {e}"
        )