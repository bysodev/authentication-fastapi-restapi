from app.db.database import Base, engine
from sqlalchemy import Column, ARRAY, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    token = Column(String(255), default="")
    refresh = Column(String(255), default="")
    creation = Column( DateTime, default=datetime.now)
    update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    estado = Column( Boolean, default=False)
    verified = Column( Boolean, default=False)

class Lesson(Base):
    __tablename__ = 'lesson'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    section_id = Column( Integer, ForeignKey('section.id') )
    description = Column(String(255))
    content = Column(ARRAY(String, dimensions=1))  # Cambiado a ARRAY
    points = Column( Integer )
    random = Column( Boolean, default=False)
    state_id = Column( Integer, ForeignKey('state.id'), default=1 )
    max_time = Column(Integer)
    time_creation = Column( DateTime, default=datetime.now)
    time_update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    section = relationship('Section', back_populates='lessons')
    user_lessons = relationship('User_lesson', back_populates='lesson')

class User_lesson(Base):
    __tablename__ = 'user_lesson'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column( Integer, ForeignKey('user.id') )
    id_lesson = Column( Integer, ForeignKey('lesson.id') )
    points_reached = Column( Numeric )
    state_id = Column( Integer, ForeignKey('state.id') )
    fails = Column( Integer )
    detail_fails = Column(ARRAY(String, dimensions=1))  # Cambiado a ARRAY
    time_creation = Column( DateTime, default=datetime.now)
    time_update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    lesson = relationship('Lesson', back_populates='user_lessons')

class Section(Base):
    __tablename__ = 'section'
    id = Column( Integer, primary_key=True, autoincrement=True )
    name = Column( String(255), nullable=False )
    description= Column(String(255))
    category_id = Column( Integer, ForeignKey('category.id') )
    lessons = relationship('Lesson', back_populates='section')

class EnumCategory( enum.Enum ):
    PALABRAS = 1
    NUMEROS = 2
    MIXTOS = 3
    ESPECIALES = 4

class EnumState( enum.Enum ):
    BLOQUEADO = 1
    DISPONIBLE = 2
    RECUPERAR = 3
    COMPLETADO = 4
    
class Category(Base):
    __tablename__ = 'category'
    id = Column( Integer, primary_key=True, autoincrement=True )
    name = Column( Enum(EnumCategory), nullable=False )

class State(Base):
    __tablename__ = 'state'
    id = Column( Integer, primary_key=True, autoincrement=True )
    name = Column( Enum(EnumState), nullable=False )

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