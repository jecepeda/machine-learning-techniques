from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()

class Incidencia(Base):
    __tablename__ = "incidencia"

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    autonomia = Column(String)
    matricula = Column(String)
    causa = Column(String)
    fecha_hora_ini = Column(DateTime)
    nivel = Column(String)
    carretera = Column(String)
    pk_inicial = Column(Integer)
    pk_final = Column(Integer)
    sentido = Column(String)
    longitud = Column(Float)
    latitud = Column(Float)
