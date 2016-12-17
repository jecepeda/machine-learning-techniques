
# coding: utf-8

# In[1]:

# Load the data
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from datetime import datetime


# In[2]:

# Create the main sqlalchemy class
Base = declarative_base()


# In[3]:

# First Model corresponds to the incidences obtained in the database
class Incidencia(Base):
    __tablename__ = "incidences"

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


# In[4]:

class AccidentDBScan(Base):
    __tablename__ = 'accidents-dbscan'
    
    id = Column(Integer, primary_key=True)
    longitud = Column(Float, default=1.0)
    latitud = Column(Float, default=1.0)
    num_cluster = Column(Integer, nullable=True)
    foreign_accident = Column(Integer, default=0)


# In[5]:

class AccidentKMeans(Base):
    __tablename__ = 'accidents-kmeans'
    
    id = Column(Integer, primary_key=True)
    longitud = Column(Float, default=1.0)
    latitud = Column(Float, default=1.0)
    num_cluster = Column(Integer, nullable=True)
    foreign_accident = Column(Integer, default=0)


# In[6]:

class DBSCANCluster(Base):
    __tablename__ = "dbscan-clusters"
    
    id = Column(Integer, primary_key=True)
    num_cluster = Column(Integer, default=0)
    accidents = Column(Integer, default=0)
    nivel_medio = Column(String, default='unknown')
    carretera = Column(String, default='unknown')
    causa_ppal = Column(String, default='unknown')
    na_causa = Column(Integer, default=0)


# In[7]:

class NumericCluster(Base):
    __tablename__ = "numeric-clusters"
    
    id = Column(Integer, primary_key=True)
    num_cluster = Column(Integer, default=0)
    accidents = Column(Integer, default=0)
    nivel_medio = Column(Integer, default=0)
    carretera = Column(Integer, default=0)
    causa_ppal = Column(Integer, default=0)
    na_causa = Column(Integer, default=0)


# In[8]:

class HierarchicalCluster(Base):
    __tablename__ = "hierarchical-clusters"
    
    id = Column(Integer, primary_key=True)
    num_cluster = Column(Integer, default=0)
    accidents = Column(Integer, default=0)
    nivel_medio = Column(Integer, default=0)
    carretera = Column(Integer, default=0)
    causa_ppal = Column(Integer, default=0)
    na_causa = Column(Integer, default=0)


# In[9]:

# Functions to create the database and obtain the session given a path

def create_db(path_to_db):
    engine = create_engine(path_to_db)
    Base.metadata.create_all(engine)

def get_db_session(path_to_db='sqlite:///../incidences.db'):
    engine = create_engine(path_to_db)
    Base.metadata.bind = engine
    DBSession = session.sessionmaker(bind=engine)
    return DBSession()

