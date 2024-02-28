from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from app.models.models import Provider, User
from app.schemas.schemas import UserUpdate
from sqlalchemy import text, column, bindparam, Integer, String, Numeric


def create_user(new_user: User , db:Session):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

def create_provider(provider: Provider, db: Session):
    db.add(provider)
    db.commit()
    db.refresh(provider)

def verify_user_by_token(token: str, db: Session):
    # Buscar el usuario por el token
    user = db.query(User).filter(User.token == token).first()
    if user:
        if user.verified == False:
            # Si se encuentra un usuario con el token, establecer 'verified' en True
            user.verified = True
            db.commit()
            return user
        else:
            return True
    else:
        # Si no se encuentra un usuario con el token, puedes manejar el error o retorno apropiado aquí.
        return False

def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

def get_user_check(db: Session, username: str, token: str):
    user = db.query(User).filter(User.username == username, User.token == token).first()
    return user

def get_user_verify(db: Session, username: str):
    user = db.query(User).filter(User.username == username, User.verified == True).first()
    return user

def get_provider_by_user_id(id: str, db: Session ):
    return db.query(Provider).filter(Provider.provider_id == id).first()

def get_user_by_id(user_id: int , db:Session):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_name_or_email(user: User , db:Session):
    # Realiza una sola consulta para buscar al usuario por nombre de usuario o correo electrónico.
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    # Verifica si se encontró un usuario.
    if existing_user:
        return True
    else:
        return False
        
def get_user_by_email(user: User , db:Session):
    # Realiza una sola consulta para buscar al usuario por nombre de usuario o correo electrónico.
    return db.query(User).filter(User.email == user.email).first()

def get_user_by_recovery(recovery_password: str, db:Session):
    return db.query(User).filter(User.recovery_password == recovery_password).first()

def update_recovery(recovery_password: str, id:int , db:Session):
    db.query(User).filter(User.id == id).update({"recovery_password": recovery_password})
    db.commit()

def update_user(user: UserUpdate, id:int , db:Session):
    user_dict = {k: v for k, v in user.model_dump().items() if v is not None}
    db.query(User).filter(User.id == id).update(user_dict)
    db.commit()
    return db.query(User).filter(User.id == id).first()

def ranking_personal_challege_by_difficulty(db: Session, category: str, id: int):
    stmt = text("WITH UserStats AS ("
                    " SELECT"
                        " us.id,"
                        " diff.name AS dificultad,"
                        " COUNT(reach.id) AS retos,"
                        " COALESCE(SUM(reach.points), 0) + COALESCE(SUM(CASE WHEN les.last_points_reached > 0 THEN (les.points_reached + les.last_points_reached) / 2 ELSE les.points_reached END), 0) AS puntos,"
                        " ROW_NUMBER() OVER (PARTITION BY diff.name ORDER BY COALESCE(SUM(reach.points), 0) + COALESCE(SUM(CASE WHEN les.last_points_reached > 0 THEN (les.points_reached + les.last_points_reached) / 2 ELSE les.points_reached END), 0) DESC) AS ranking,"
                        " COUNT(les.id) AS lecciones"
                    " FROM "
                    " public.challenges AS chall "
                    " LEFT JOIN public.reach_challenges AS reach ON chall.id = reach.id_challenge "
                    " LEFT JOIN public.user AS us ON us.id = reach.id_user "
                    " FULL OUTER JOIN public.user_lesson AS les ON us.id = les.id_user "
            " JOIN public.category AS cate ON chall.category_id = cate.id AND cate.name=:categoria "
            " JOIN public.difficulty AS diff ON chall.difficulty_id = diff.id"
                " WHERE (reach.points IS NOT NULL OR les.points_reached IS NOT NULL)"
            " GROUP BY diff.name, us.id)"
        " SELECT userStats.* FROM UserStats AS userStats WHERE userStats.id=:id;").\
        bindparams(categoria=category, id=id)
            
        
    stmt.columns(
        column('dificultad', String),
        column('retos', Integer),
        column('puntos', Numeric),
        column('lecciones', Integer)
    )
    result = db.execute(stmt)
    return result

# " JOIN public.category AS cate ON chall.category_id = cate.id AND cate.name=:categoria "
