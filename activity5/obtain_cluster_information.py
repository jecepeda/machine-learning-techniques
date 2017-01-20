
# coding: utf-8

# In[1]:

# load models
import sys
sys.path.append('../')
from database.models import Incidencia, AccidentDBScan, DBSCANCluster, get_db_session, NumericCluster
from sqlalchemy import func


# In[2]:


def obtain_characteristic(session, cluster, item, conditions):
    ''' 
        This function is intended to make less effort to write code
        It's basically a Join query between Incidencia and AccidentDBSCan models
        where you pass the data you want to obtain, and more optional conditions.
        
        returns the query
    '''
    accidents = session.query(item).filter(
        Incidencia.id == AccidentDBScan.foreign_accident,
        AccidentDBScan.num_cluster == cluster)
    for condition in conditions:
        accidents = accidents.filter(condition)
    return accidents


# In[3]:

'''
    Insert the value obtained from each cluster into a new table called DBSCANCluster
    We had to use join queries to obtain the information of the incidences
'''
def insert_cluster_values(session):
    clusters = session.query(AccidentDBScan.num_cluster).distinct().all()
    for cluster in clusters:
        n_cluster = cluster[0]
        cl = DBSCANCluster(num_cluster=n_cluster)
        # Obtain the number of accidents
        cl.accidents = session.query(func.count(AccidentDBScan.id)).filter(
            AccidentDBScan.num_cluster == n_cluster).first()[0]        
        cl.nivel_medio = obtain_characteristic(session,
                                               n_cluster,
                                               func.max(Incidencia.nivel),
                                               [Incidencia.nivel != 'unknown']).first()[0]
        cl.causa_ppal = obtain_characteristic(session,
                                              n_cluster,
                                              func.max(Incidencia.causa),
                                              [Incidencia.causa != 'unknown']).first()[0]
        cl.carretera = obtain_characteristic(session,
                                             n_cluster,
                                             func.max(Incidencia.carretera),
                                             [Incidencia.carretera != 'unknown']).first()[0]
        query = obtain_characteristic(session,
                                      n_cluster,
                                      func.count(Incidencia.causa),
                                      [Incidencia.nivel != 'unknown'])
        query = query.filter(Incidencia.causa == cl.causa_ppal)
        cl.na_causa = query.first()[0]
        session.add(cl)
    session.commit()


# In[4]:

s = get_db_session('sqlite:///../incidences.db')


# In[5]:

insert_cluster_values(s)

