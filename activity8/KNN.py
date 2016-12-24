
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors
import pandas as pd
from random import uniform

import sys
sys.path.append('../')
from database.models import get_db_session, AccidentDBScan


# In[2]:

# Obtain accidents
session = get_db_session('sqlite:///../incidences.db')
accidents = session.query(AccidentDBScan.longitud, 
                          AccidentDBScan.latitud,
                          AccidentDBScan.num_cluster).all()

print('Number of accidents = {}'.format(len(accidents)))


# In[4]:

# Function for obtain random accidents to train KNN
def shuffle_accidents(p, accidents):
    train = []
    test = []
    for accident in accidents:
        if uniform(0, 1) < p:
            train.append(accident)
        else:
            test.append(accident)
    return [train, test]


# In[4]:

# We repeat the process of choosing the best K 60 times
# to obtain the average number of errors

train_p = 0.6
repetitions = 60
k_errors = [0 for x in range(repetitions)]

for rep in range(repetitions):
    train, test = shuffle_accidents(train_p, accidents)
    lat_and_lon_train = [x[:2] for x in train]
    lat_and_lon_test = [x[:2] for x in test]
    zone_train = [x[2] for x in train]
    zone_test = [x[2] for x in test]
    for n_neighbors in range(1, repetitions):
        clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
        clf.fit(lat_and_lon_train, zone_train)
        Z = clf.predict(lat_and_lon_test)
        err = (zone_test != Z).sum() / len(test)
        k_errors[n_neighbors] += err


# In[5]:

errors = list(map(lambda x : x / repetitions, k_errors))


# In[6]:

# Plot the result

plt.title('Selection of best K (distance)')
plt.ylabel('Error')
plt.xlabel('K')
plt.xlim(1, repetitions)
plt.plot(errors)
plt.show()


# We choose K=2 to apply KNN to work accidents.

# In[8]:

train_p = 0.6
train, test = shuffle_accidents(train_p, accidents)
lat_and_lon_train = [list(x[:2]) for x in train]
lat_and_lon_test = [list(x[:2]) for x in test]
zone_train = [x[2] for x in train]

clf = neighbors.KNeighborsClassifier(2, weights='distance')
clf.fit(lat_and_lon_train, zone_train)
Z = clf.predict(lat_and_lon_test)


# In[9]:

x_min, x_max = min([x[0] for x in train]) - 1, max([x[0] for x in train]) + 1
y_min, y_max = min([x[1] for x in train]) - 1, max([x[1] for x in train]) + 1
print("X Min {}. X Max {}".format(x_min, x_max))
print("Y Min {}. Y Max {}".format(y_min, y_max))
h = 0.1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
print("XX class {} YY class {}".format(xx.__class__, yy.__class__))
print("Z class {}".format(Z.__class__))


# In[10]:

cmap = ListedColormap(plt.cm.Paired(np.linspace(0, 1, len(np.unique(Z)))))
print("Cmap class {}".format(cmap.__class__))


# In[11]:

Z = Z.reshape(xx.shape)
print(Z.__class__)


# In[15]:

plt.figure()
from IPython.core.debugger import Tracer
Tracer()() #this one triggers the debugger
plt.pcolormesh(xx, yy, Z, cmap=cmap)


# In[ ]:



