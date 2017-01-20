
# coding: utf-8

# In[5]:

import numpy as np

from sklearn import neighbors

import sys
sys.path.append('../')
from database.models import get_db_session, AccidentDBScan, WorkZone, Incidencia


# In[6]:

#Obtain workzones KNN
session2007 = get_db_session('sqlite:///../incidencesAux.db')
works = session2007.query(WorkZone.num_cluster).all()
works_cluster = [i[0] for i in works]


# In[7]:

# Obtain KNN of accidents
session2006 = get_db_session('sqlite:///../incidences.db')
K = 2
accidents = session2006.query(Incidencia).filter(Incidencia.tipo == 'Accidente').all()
db_accidents = session2006.query(AccidentDBScan.longitud, 
                          AccidentDBScan.latitud,
                          AccidentDBScan.num_cluster).all()
accident_set = [x[:2] for x in db_accidents]
zones = [x[2] for x in db_accidents]
lat_and_lon_works = [(inc.longitud, inc.latitud) for inc in accidents]
clf = neighbors.KNeighborsClassifier(K, weights='distance')
clf.fit(accident_set, zones)
accidents_cluster = clf.predict(lat_and_lon_works)


# In[ ]:

#Obtain the knn zones without roadworks
no_coincidence = [i for i in accidents_cluster if i not in works_cluster]


# In[ ]:

#Obtain the accident type in the clusters without roadworks
types_y = []
for index, accident in enumerate(accidents):
    if accidents_cluster[index] in set(no_coincidence):
        types_y.append(accident.causa)
        
cause_y = [i for i in set(types_y)]
cause_ammount_y = [0]*len(cause_y)

for acc in types_y:
    cause_ammount_y[cause_y.index(acc)] = cause_ammount_y[cause_y.index(acc)] + 1
    



# In[ ]:

#Obtain the accident type in the clusters with roadworks
types_n = []
for index, accident in enumerate(accidents):
    if accidents_cluster[index] not in set(no_coincidence):
        types_n.append(accident.causa)
        
cause_n = [i for i in set(types_n)]
cause_ammount_n = [0]*len(cause_n)

for acc in types_n:
    cause_ammount_n[cause_n.index(acc)] = cause_ammount_n[cause_n.index(acc)] + 1


# In[ ]:

#We normalise the data
total_y = sum(cause_ammount_y)
total_n = sum(cause_ammount_n)

for index in range(len(cause_y)):
    cause_ammount_n[index] = cause_ammount_n[index]/total_n
    cause_ammount_y[index] = cause_ammount_y[index]/total_y

print(cause_y)
print(cause_ammount_y)
print(cause_ammount_n)
print('As we can see, there are way more "vuelco", "tijera camión" and "atropello" in the ones with roadworks')


# As we can see, there are way more "vuelco", "tijera camión" and "atropello" in the ones with roadworks
