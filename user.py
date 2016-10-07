from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime

Base = declarative_base()

class Incidencia(Base):
    __tablename__ = "incidencia"

    id = Column(Integer, primary_key=True)
    tipo = Column(String, default="unknown")
    autonomia = Column(String, default="unknown")
    matricula = Column(String, default="unknown")
    causa = Column(String, default="unknown")
    fecha_hora_ini = Column(DateTime, default=datetime.now())
    nivel = Column(String, default="unknown")
    carretera = Column(String, default="unknown")
    pk_inicial = Column(Integer, default=1)
    pk_final = Column(Integer, default=1)
    sentido = Column(String, default=1)
    longitud = Column(Float, default=1.0)
    latitud = Column(Float, default=1.0)
