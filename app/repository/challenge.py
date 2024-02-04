from sqlalchemy.orm import Session, aliased
from app.models.models import Challenges, ReachChallenges, Category, Difficulty, User
from sqlalchemy import func, not_, select, text, column, bindparam, Integer, String, Numeric

def create_challenge(new_challenge: Challenges , db:Session):
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)

def start_challenge(category: str, difficulty: str, id: int, db: Session):
    challenges = db.query(Challenges)\
        .join(Category, ( Category.id == Challenges.category_id ) & ( Category.name == category ) )\
        .join(Difficulty, ( Difficulty.id == Challenges.difficulty_id ) & ( Difficulty.name == difficulty ) )\
        .filter( not_(  db.query(ReachChallenges).filter(ReachChallenges.id_user == id, ReachChallenges.id_challenge == Challenges.id).exists() ) )\
        .order_by(func.random()).first()
    print(challenges)
    return challenges

def get_challenges(db: Session):
    challenges = db.query(Challenges).all()
    return challenges

def ranking_challege_by_difficulty(db: Session, category: str):

    stmt = text("WITH RankedUsers AS ( SELECT diff.name AS dificultad, us.username, us.image, COUNT(reach.id) AS retos, COALESCE(SUM(reach.points), 0) + COALESCE(SUM(CASE WHEN les.last_points_reached > 0 THEN (les.points_reached + les.last_points_reached) / 2 ELSE les.points_reached END), 0) AS puntos, ROW_NUMBER() OVER (PARTITION BY diff.name ORDER BY COALESCE(SUM(reach.points), 0) + COALESCE(SUM(CASE WHEN les.last_points_reached > 0 THEN (les.points_reached + les.last_points_reached) / 2 ELSE les.points_reached END), 0) DESC) AS ranking, COUNT(les.id) AS lecciones"
            " FROM public.challenges AS chall"
            " LEFT JOIN public.reach_challenges AS reach ON chall.id = reach.id_challenge"
            " LEFT JOIN public.user AS us ON us.id = reach.id_user"
            " LEFT JOIN public.user_lesson AS les ON us.id = les.id_user"
            " JOIN public.category AS cate ON chall.category_id = cate.id AND cate.name=:categoria "
            " JOIN public.difficulty AS diff ON chall.difficulty_id = diff.id"
            "    WHERE reach.points IS NOT NULL"
            " GROUP BY diff.name, us.username, us.image)"
        " SELECT ran.*"
        " FROM RankedUsers as ran"
        " WHERE ranking <= 5;").\
        bindparams(categoria=category)
        
    stmt.columns(
        column('dificultad', String),
        column('username', String),
        column('image', String),
        column('retos', Integer),
        column('puntos', Numeric),
        column('lecciones', Integer)
    )
    result = db.execute(stmt)
    return result

def get_challenges_by_category(db: Session, category: str):
    challenges = db.query(Challenges).filter(Challenges.category == category)
    return challenges

def get_challenges_by_user_and_difficulty(db: Session, id: int):
    challenges = db.query(Category.name.label('categoria'), Difficulty.name.label('dificultad'), func.count( Challenges.id ).label('total') , func.count( ReachChallenges.id ).label('progreso'), func.sum( Challenges.points ).label('puntos') ).outerjoin(ReachChallenges, ( Challenges.id == ReachChallenges.id_challenge ) & ( ReachChallenges.id_user == id ) ).join(Category, (Challenges.category_id == Category.id) ).join(Difficulty, (Challenges.difficulty_id == Difficulty.id)).group_by(Challenges.category_id, Category.name, Difficulty.name).all()
    return challenges 

def get_challenges_by_user(db: Session, category: str, id: int):
    # challenges = db.query(Challenges.number, ReachChallenges.end_points).outerjoin(ReachChallenges, ReachChallenges.id_challenge == Challenges.id).all()
    challenges = db.query(Challenges, ReachChallenges.end_points, ReachChallenges.state.label('reach_state'), ReachChallenges.minutes, Difficulty.name.label('diffyculty_name'), Category.name.label('category_name')).outerjoin(ReachChallenges, ( Challenges.id == ReachChallenges.id_challenge ) & ( ReachChallenges.id_user == id ) ).join(Category, (Challenges.category_id == Category.id) & ( Category.name == category )).join(Difficulty, (Challenges.difficulty_id == Difficulty.id)).all()

    return challenges 

def get_challenge(db: Session, number: int, name: str):
    challenge = db.query(Challenges).filter((Challenges.number == number) | (Challenges.name == name)).first()
    return challenge

def get_challenge_id(id: int, db: Session):
    challenge = db.query(Challenges, Difficulty ).join(Difficulty, Challenges.difficulty_id == Difficulty.id ).filter((Challenges.id == id)).first()
    return challenge


# API ANTINGUA
# def ranking_challege_by_difficulty(db: Session):
    # diff = aliased( Difficulty )
    # us = aliased( User )
    # cate = aliased( Category )
    # chall = aliased( Challenges )
    # reach = aliased( ReachChallenges )

    # subquery = (
    #     select([
    #         diff.name.label('dificultad'),
    #         us.username.label('name'),
    #         func.count(reach.id).label('progreso'),
    #         func.coalesce(func.sum(reach.points), 0).label('puntos'),
    #         func.row_number().over(
    #             partition_by=diff.name,
    #             order_by=func.coalesce(func.sum(reach.points), 0).desc()
    #         ).label('ranking')
    #     ])
    #     .select_from(chall.outerjoin(reach, chall.c.id == reach.id_challenge, isouter=True)
    #                 .outerjoin(us, us.id == reach.id_user, isouter=True)
    #                 .outerjoin(cate, cate.id == chall.category_id)
    #                 .outerjoin(diff, diff.id == chall.difficulty_id)
    #     )
    #     .where(reach.points.isnot(None))
    #     .group_by(diff.name, us.c.username)
    #     # .alias('RankedUsers')
    # )
    # main_query = (
    #     select([subquery.c])
    #     .where(subquery.c.ranking <= 4)
    # )
    # result = db.execute(main_query)