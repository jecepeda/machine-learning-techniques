from models import get_db_session, ClusterN
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy import cluster
from sklearn import preprocessing
import sklearn.neighbors

def retrieve_data(db='incidences.db'):
    conn = sqlite3.connect(db)
    query_result = conn.execute("SELECT id, num_cluster, accidents, nivel_medio, carretera, causa_ppal, na_causa FROM ClustersN;")
    ret = [row for row in query_result]
    return ret

def insert_Hcluster(clusters, labels):
    session = get_db_session('sqlite:///incidences.db')
    for idx in range(len(clusters)):
        id = clusters[idx]
        clusterN = session.query(ClusterN).filter(ClusterN.id == id).first()
        clusterN.Hcluster = labels[idx]
    session.commit()



data = retrieve_data()


min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(data)

dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(data)
avSim = np.average(matsim)

print ("%s\t%6.2f" % ('Distancia Media', avSim))

clusters = cluster.hierarchy.linkage(matsim, method = 'ward')
cluster.hierarchy.dendrogram(clusters, color_threshold=10)
plt.show()

cut =(10)

labels = cluster.hierarchy.fcluster(clusters, cut, criterion = 'distance')

print ('Number of clusters %d' % (len(set(labels))))

session = get_db_session('sqlite:///incidences.db')
clusters = session.query(ClusterN.id).all()
new_clusters = [row[0] for row in clusters]
insert_Hcluster(new_clusters, labels)
