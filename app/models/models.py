from app.db.database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum, UniqueConstraint, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # username = Column(String, nullable=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    token = Column(String(255), default="")
    refresh = Column(String(255), default="")
    creation = Column( DateTime, default=datetime.now)
    update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    estado = Column( Boolean, default=False)
    verified = Column( Boolean, default=False)

# class Lesson(Base):
#     __tablename__ = 'lesson'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     # username = Column(String, nullable=True)
#     number = Column(Integer)
#     name = Column(String(100))
#     category = Column(String(50))
#     description = Column(String(255))
#     points = Column( Integer )
#     time_creation = Column( DateTime, default=datetime.now)
#     time_update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
#     state = Column( Boolean, default=True)

# class ReachLesson(Base):
#     __tablename__ = 'reach_lesson'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     # username = Column(String, nullable=True)
#     id_user = Column( Integer, ForeignKey('user.id') )
#     id_lesson = Column( Integer, ForeignKey('lesson.id') )
#     points = Column( Numeric )
#     minutes_max = Column( Integer )
#     seconds_max = Column( Integer )
    
#     fails_max = Column( Integer )
#     end_points = Column( Numeric )
#     time_creation = Column( DateTime, default=datetime.now)

class EnumCategory( enum.Enum ):
    PALABRAS = 'PALABRAS'
    NUMEROS = 'NUMEROS'

class Category(Base):
    __tablename__ = 'category'
    id = Column( Integer, primary_key=True, autoincrement=True )
    name = Column( Enum(EnumCategory), nullable=False )

class Challenges(Base):
    __tablename__ = 'challenges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # username = Column(String, nullable=True)
    number = Column(Integer, unique=True)
    name = Column(String(100), unique=True)
    category_id = Column( Integer, ForeignKey('category.id') )
    difficulty_id = Column( Integer, ForeignKey('difficulty.id') )
    description = Column(String(255))
    points = Column( Integer )
    minutes_max = Column( Integer )
    seconds_max = Column( Integer )
    fails_max = Column( Integer ) 
    random = Column( Boolean, default=False)
    operation = Column( Boolean, default=False)
    spelled = Column( Boolean, default=False)
    supplement = Column( Boolean, default=False)
    state = Column( Boolean, default=True)
    content = Column(ARRAY(String, dimensions=1))
    time_creation = Column( DateTime, default=datetime.now)
    time_update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    UniqueConstraint("number", "name", name="unique_leccion")
    difficulty = relationship( 'Difficulty' )
    category = relationship( 'Category' )

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class EnumDifficulty( enum.Enum ):
    FACIL = 'FACIL'
    MEDIO = 'MEDIO'
    DIFICIL = 'DIFICIL'

class EnumStateChallenge( enum.Enum ):
    RECUPERAR = 'RECUPERAR'
    COMPLETADO = 'COMPLETADO'

class Difficulty(Base):
    __tablename__ = 'difficulty'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column( Enum(EnumDifficulty), nullable=False )
    bonus = Column( Integer, default=0 )

class ReachChallenges(Base):
    __tablename__ = 'reach_challenges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column( Integer, ForeignKey('user.id') )
    id_challenge = Column( Integer, ForeignKey('challenges.id') )
    points = Column( Numeric )
    bonus = Column( Integer )
    end_points = Column( Numeric )
    minutes = Column( Integer )
    seconds = Column( Integer )
    fails = Column( Integer, default=0 )
    streak = Column( Integer, default=0 )
    state = Column( Enum(EnumStateChallenge), nullable=False)
    time_creation = Column( DateTime, default=datetime.now)
    challenge = relationship( 'Challenges' )
    user = relationship( 'User')

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)