# -*- coding: utf-8 -*-

# 1. Load data
f = open("municipios.csv", "r")
data = []
for l in f.readlines():
    row = l.split(",")
    data.append(map(float,row)) 
    


#1. Data normalizazion
#http://scikit-learn.org/stable/modules/preprocessing.html
from sklearn import preprocessing 
min_max_scaler = preprocessing.MinMaxScaler()
datanorm = min_max_scaler.fit_transform(data)

#2. Principal Component Analysis
from sklearn.decomposition import PCA
estimator = PCA (n_components = 2)
X_pca = estimator.fit_transform(datanorm)

import matplotlib.pyplot as plt
plt.plot(X_pca[:,0], X_pca[:,1],'x')


#3. Hierarchical Clustering
# 3.1. Compute the similarity matrix
import sklearn.neighbors
import numpy
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(datanorm)
avSim = numpy.average(matsim)
print "%s\t%6.2f" % ('Average Distance', avSim)

# 3.2. Building the Dendrogram	
from scipy import cluster
clusters = cluster.hierarchy.linkage(matsim, method = 'complete')
# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.hierarchy.dendrogram.html
cluster.hierarchy.dendrogram(clusters, color_threshold=0)
plt.show()

cut = 15 # !!!! ad-hoc
labels = cluster.hierarchy.fcluster(clusters, cut , criterion = 'distance')
print 'Number of clusters %d' % (len(set(labels)))

colors = numpy.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
colors = numpy.hstack([colors] * 20)


fig, ax = plt.subplots()
# ad-hoc
plt.xlim(-1.5, 1.5)
plt.ylim(-1, 0.4)

for i in range(len(X_pca)):
    plt.text(X_pca[i][0], X_pca[i][1], 'x', color=colors[labels[i]])  
    
ax.grid(True)
fig.tight_layout()
plt.show()





from sklearn import metrics
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print('Estimated number of clusters: %d' % n_clusters_)
#print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
#print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
#print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
#print("Adjusted Rand Index: %0.3f"
 #     % metrics.adjusted_rand_score(labels_true, labels))
#print("Adjusted Mutual Information: %0.3f"
#    % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(datanorm, labels))
      

for c in range(1,n_clusters_):
    print 'Group', c
    for i in range(len(datanorm[0])):
        column = [row[i] for j,row in enumerate(data) if labels[j] == c]
        if len(column) != 0:
            print i, numpy.mean(column)