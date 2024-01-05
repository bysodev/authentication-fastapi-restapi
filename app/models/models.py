from app.db.database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum
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
    PALABRAS = 1
    NUMEROS = 2
    MIXTOS = 3
    ESPECIALES = 4

class Category(Base):
    __tablename__ = 'category'
    id = Column( Integer, primary_key=True, autoincrement=True )
    name = Column( Enum(EnumCategory), nullable=False )

class Challenges(Base):
    __tablename__ = 'challenges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # username = Column(String, nullable=True)
    number = Column(Integer)
    name = Column(String(100))
    category_id = Column( Integer, ForeignKey('category.id') )
    difficulty_id = Column( Integer, ForeignKey('difficulty.id') )
    description = Column(String(255))
    points = Column( Integer )
    bonus = Column( Integer )
    minutes_max = Column( Integer )
    seconds_max = Column( Integer )
    fails_max = Column( Integer ) 
    state = Column( Boolean, default=True)
    time_creation = Column( DateTime, default=datetime.now)
    time_update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    difficulty = relationship( 'Difficulty' )
    category = relationship( 'Category' )

class EnumDifficulty( enum.Enum ):
    EASY = 1
    MEDIUM = 2
    DIFFICULT = 3

class Difficulty(Base):
    __tablename__ = 'difficulty'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column( Enum(EnumDifficulty), nullable=False )

class ReachChallenges(Base):
    __tablename__ = 'reach_challenges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column( Integer, ForeignKey('user.id') )
    id_lesson = Column( Integer, ForeignKey('challenges.id') )
    points = Column( Numeric )
    bonus = Column( Integer )
    end_points = Column( Numeric )
    minutes = Column( Integer )
    seconds = Column( Integer )
    faults = Column( Integer, default=0 )
    streak = Column( Integer, default=0 )
    time_creation = Column( DateTime, default=datetime.now)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)