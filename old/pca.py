from models import get_db_session,  Cluster
from sklearn.decomposition import PCA
import sklearn.cluster
import numpy
import matplotlib.pyplot as plt
from sklearn import preprocessing

def retrieve_data(db='incidences.db'):
    conn = sqlite3.connect(db)
    query_result = conn.execute("SELECT id, num_cluster, accidents, nivel_medio, carretera, causa_ppal, na_causa FROM ClustersN;")
    ret = [row for row in query_result]
    return ret

states = retrieve_data()

#Normalization
min_max_scaler = preprocessing.MinMaxScaler()
states = min_max_scaler.fit_transform(states)
print (states)

#PCA Estimation
estimator = PCA(n_components=3) # Number of components left
X_pca = estimator.fit_transform(states)
print(X_pca)

plt.scatter([x[0] for x in X_pca], [x[1] for x in X_pca])
plt.show()
