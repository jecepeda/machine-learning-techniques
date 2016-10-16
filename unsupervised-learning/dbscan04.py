# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 16:34:34 2016

"""
# -*- coding: utf-8 -*-
import codecs
import numpy
from sklearn.cluster import DBSCAN
from sklearn import preprocessing 
import sklearn.neighbors
import matplotlib.pyplot as plt


# ....
def load_data(path,all):
        
    f = codecs.open(path, "r", "utf-8")
    data = []
    count = 0
    for line in f:
        if count > 0: 
		row = line.split(",")
		if all != 1: 
			row.pop(0)
 			row.pop(0)
		if row != []:
			data.append(map(float, row))
        count += 1
 
   
    return data
    
#0. Loading data 
#0.1 load the data to cluster
data = load_data("dbscan04.csv",0)
#0.2 load all the data 
alldata= numpy.asarray(load_data("dbscan04.csv", 1))

#0.3 Preprocessing -> normalization
min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(data)


# 1. Parametrization	
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(data)

minPts=4
from sklearn.neighbors import kneighbors_graph
A = kneighbors_graph(data, minPts, include_self=False)
Ar = A.toarray()

seq = []
for i,s in enumerate(data):
    for j in range(len(data)):
        if Ar[i][j] != 0:
            seq.append(matsim[i][j])
            
seq.sort()
plt.plot(seq)
plt.show()
    

# 2. DBSCAN Execution
db = DBSCAN(eps=0.05, min_samples=minPts).fit(data)
core_samples_mask = numpy.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# 3. Validation
from sklearn import metrics
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))

# 4. Visualaztion. Plotting the data
unique_labels = set(labels)
colors = plt.cm.Spectral(numpy.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Utilizamos blanco para el ruido
        col = 'w'
           
    class_member_mask = (labels == k)
    xy = data[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=17)

    xy = data[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=5)

plt.title('Numero de clusteres obtenidos: %d' % n_clusters_)
plt.show()

#5. Clustering description
# 5.1 Create the list of cluster. Each cluster a list with elements
for i in range(0,n_clusters_):
    exec 'group%s = []' %(i)

# 5.2 for each element assign its cluster (removing outliers)
for index, x in numpy.ndenumerate(labels):
    if x!=-1: 
        exec 'group%s.append(alldata[index])' %(x)


# 5.3 Computers basics descriptors
for i in range(0,n_clusters_):
    exec 'mean%s = numpy.mean(group%s, axis=0) ' %(i,i)
    exec 'median%s = numpy.median(group%s, axis=0) ' %(i,i)
    exec 'std%s = numpy.std(group%s, axis=0) ' %(i,i)
    exec 'amin%s = numpy.amin(group%s, axis=0) ' %(i,i)
    exec 'amax%s = numpy.amax(group%s, axis=0) ' %(i,i)
    
# 5.4 Computing filtered descriptors
for i in range(0,n_clusters_):
    exec 'numminorstas%s = numpy.asarray(group%s)[:,0].tolist().count(1)' %(i,i)
    exec 'nummhyc%s = numpy.asarray(group%s)[:,0].tolist().count(2)' %(i,i)
    exec 'nummlisboa%s = numpy.asarray(group%s)[:,1].tolist().count(1)' %(i,i)
    exec 'nummoporto%s = numpy.asarray(group%s)[:,1].tolist().count(2)' %(i,i)
    exec 'nummotrazona%s = numpy.asarray(group%s)[:,1].tolist().count(3)' %(i,i)
    


