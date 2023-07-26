from app.db.database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # username = Column(String, nullable=True)
    nombre = Column(String(255))
    apellido = Column(String(255))
    direccion = Column(String(255))
    telefono = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    creation = Column( DateTime, default=datetime.now)
    update = Column( DateTime, default=datetime.now, onupdate=datetime.now)
    estado = Column( Boolean, default=False)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)