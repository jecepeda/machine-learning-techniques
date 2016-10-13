from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from datetime import datetime

Base = declarative_base()

class Incidencia(Base):
    __tablename__ = "incidencia"

    id = Column(Integer, primary_key=True)
    tipo = Column(String, default="unknown")
    autonomia = Column(String, default="unknown")
    provincia = Column(String, default="unknown")
    matricula = Column(String, default="unknown")
    causa = Column(String, default="unknown")
    fecha_hora_ini = Column(DateTime, datetime.now())
    nivel = Column(String, default="unknown")
    carretera = Column(String, default="unknown")
    pk_inicial = Column(Float, default=1)
    pk_final = Column(Float, default=1)
    sentido = Column(String, default=1)
    longitud = Column(Float, default=1.0)
    latitud = Column(Float, default=1.0)

def create_db(path_to_db):
    engine = create_engine(path_to_db)
    Base.metadata.create_all(engine)

def get_db_session(path_to_db):
    engine = create_engine(path_to_db)
    Base.metadata.bind = engine
    DBSession = session.sessionmaker(bind=engine)
    return DBSession()
