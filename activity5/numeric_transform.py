
# coding: utf-8

# In[1]:

# load models
import sys
sys.path.append('../')
from database.models import Incidenciaencia, DBSCANCluster, NumericCluster, get_db_session
from sqlalchemy import func


# In[2]:

# Load data
session = get_db_session('sqlite:///../incidences.db')


# In[3]:

# Defining methods to transform the data
def tf_nivel_medio(a):
    n = 0
    if a == "Rojo":
        n = 5
    elif a == "Blanco":
        n = 1
    else:
        n = 10

    return n

def tf_causa_ppal(a):
    n = 0

    if a == "Alcance":
        n = 1
    elif a == "Salida":
        n = 3
    else :
        n = 4

    return n

def tf_carretera(a):
    n = 0

    if "BI-" in a:
        n = 1
    elif "N-" in a:
        n = 2
    else:
        n = 3

    return n


# In[4]:

def transform_db(session):
    clusters = session.query(DBSCANCluster).all()
    for cluster in clusters:
        cln = NumericCluster(num_cluster = cluster.num_cluster)
        cln.accidents = cluster.accidents
        cln.nivel_medio = tf_nivel_medio(cluster.nivel_medio)
        cln.causa_ppal = tf_causa_ppal(cluster.causa_ppal)
        cln.carretera = tf_carretera(cluster.carretera)
        cln.na_causa = cluster.na_causa
        session.add(cln)  
    session.commit()


# In[5]:

s = get_db_session('sqlite:///../incidences.db')
transform_db(s)

