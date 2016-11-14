import sqlite3
import matplotlib.pyplot as plt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from datetime import datetime

Base = declarative_base()

class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(Integer, primary_key=True)
    num_cluster = Column(Integer, default=0)
    accidents = Column(Integer, default=0)
    nivel_medio = Column(String, default='unknown')
    carretera = Column(String, default='unknown')
    causa_ppal = Column(String, default='unknown')

class Incidencia(Base):
    __tablename__ = "incidencia"

    id = Column(Integer, primary_key=True)
    tipo = Column(String, default="unknown")
    autonomia = Column(String, default="unknown")
    provincia = Column(String, default="unknown")
    matricula = Column(String, default="unknown")
    causa = Column(String, default="unknown")
    fechahora_ini = Column(DateTime, default=None)
    nivel = Column(String, default="unknown")
    carretera = Column(String, default="unknown")
    pk_inicial = Column(Float, default=1)
    pk_final = Column(Float, default=1)
    sentido = Column(String, default=1)
    longitud = Column(Float, default=1.0)
    latitud = Column(Float, default=1.0)
    num_cluster = Column(Integer, nullable=True)

def create_db(path_to_db):
    engine = create_engine(path_to_db)
    Base.metadata.create_all(engine)

def get_db_session(path_to_db):
    engine = create_engine(path_to_db)
    Base.metadata.bind = engine
    DBSession = session.sessionmaker(bind=engine)
    return DBSession()

def retrieve_data(db='incidences.db', data='latitud, longitud', tipo='Accidente'):
    conn = sqlite3.connect(db)
    query_result = conn.execute("SELECT {} FROM Incidencia WHERE tipo = '{}';".format(data, tipo))
    ret= [row for row in query_result]
    return ret

def plot_data(data, labels = 'b', title= 'default'):
    plt.scatter([row[0] for row in data],[row[1] for row in data], c=labels)
    plt.title(title)
    plt.show()
