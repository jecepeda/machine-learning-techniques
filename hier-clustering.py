import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy import cluster
from sklearn import preprocessing
import sklearn.neighbors

def retrieve_data(db='incidences.db'):
    conn = sqlite3.connect(db)
    query_result = conn.execute("SELECT *  FROM ClustersN;")
    ret= [row for row in query_result]
    return ret

data = retrieve_data()

states = retrieve_data()

min_max_scaler = preprocessing.MinMaxScaler()
states = min_max_scaler.fit_transform(states)

dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(states)
avSim = np.average(matsim)

print ("%s\t%6.2f" % ('Distancia Media', avSim))

clusters = cluster.hierarchy.linkage(matsim, method = 'ward')
cluster.hierarchy.dendrogram(clusters, color_threshold=10)
plt.show()


