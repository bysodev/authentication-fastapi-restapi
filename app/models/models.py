from app.db.database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum, UniqueConstraint, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class Provider(Base):
    __tablename__ = 'provider'
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_name = Column(String(255))
    provider_id = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)  # Make this a unique field

    # Relationship to User
    user = relationship('User', back_populates='provider', uselist=False)  # Set uselist=False for one-to-one

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    token = Column(String(255), default="")
    image = Column(String(255), default="") 
    active = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    recovery_password = Column(String(255), default="")  # New field for recovery password
    creation = Column(DateTime, default=datetime.now)
    update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship to Provider
    provider = relationship('Provider', back_populates='user', uselist=False)  # Set uselist=False for one-to-one

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
    state_id = Column( Integer, ForeignKey('state.id') )
    points_reached = Column( Numeric )
    last_points_reached = Column( Numeric )
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
    PALABRAS = 'PALABRAS'
    NUMEROS = 'NUMEROS'

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

class ReachChallengesCustomized(Base):
    __tablename__ = 'challenges_customized'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column( Integer, ForeignKey('user.id') )
    id_category = Column( Integer, ForeignKey('category.id') )
    id_difficulty = Column( Integer, ForeignKey('difficulty.id') )
    bonus = Column( Integer )
    points = Column( Integer )
    end_points = Column( Integer )
    minutes_max = Column( Integer )
    seconds_max = Column( Integer )
    minutes = Column( Integer )
    seconds = Column( Integer )
    lives = Column( Integer ) 
    fails = Column( Integer ) 
    time_creation = Column( DateTime, default=datetime.now)
    time_update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    difficulty = relationship( 'Difficulty' )
    category = relationship( 'Category' )
    user = relationship( 'User')

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