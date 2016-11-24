# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:27:43 2016

@author: asus
"""

import numpy as np
from sklearn import preprocessing 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.mixture import GMM
from sklearn import metrics
import seaborn as sns

filename = "DatosCluster.csv"
type_client = {1:"Distribuidor Minorista", 2:"Hotel y Cafeterias"}
region = {1:"Lisboa", 2:"Oporto", 3:"Otros"}

#0.0 Load Data from a csv file
def load_data(filename):
    f = open(filename, "r")
    data = []
    for l in f.readlines():
        row = l.split(",")
        data.append(map(float,row))

    return np.array(data, np.int32)
    

#0.1 Get only cost data 
data = load_data(filename)
cost_data = data[:, 2:]
N = len(data)

R = np.corrcoef(np.transpose(cost_data))

sns.set(style="white")
mask = np.zeros_like(R, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
f, ax = plt.subplots(figsize=(8, 8))
cmap = sns.diverging_palette(200, 10, as_cmap=True)
sns.heatmap(R, mask=mask, cmap=cmap, vmax=.8,
            square=True, xticklabels=2, yticklabels=2,
            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)


#1.0 Data normalizazion
min_max_scaler = preprocessing.MinMaxScaler()
datanorm = min_max_scaler.fit_transform(cost_data)


#2.0 Principal Component Analysis
estimator = PCA (n_components = 2)
X_pca = estimator.fit_transform(datanorm)
print "-- Porcentaje de variabilidad explicada: %.4f" % np.sum(estimator.explained_variance_ratio_)
print estimator.explained_variance_ratio_
#plt.plot(X_pca[:,0], X_pca[:,1],'x')


#3.0 Best GMM parameters
lowest_bic = np.infty
bic = []
best_cv = 'full'
best_k = 3
cv_types = ['spherical', 'tied', 'diag', 'full']

for cv_type in cv_types:
    for k in range(1, 7):
        gmm = GMM(n_components=k, covariance_type=cv_type, init_params='wc', n_iter=20)
        gmm.fit(X_pca)
        bic.append(gmm.bic(X_pca))
        if bic[-1] < lowest_bic:
            lowest_bic = bic[-1]
            best_cv = cv_type
            best_k = k


#3.1 Final GMM
EM = GMM(n_components=best_k, covariance_type=best_cv, init_params='wc', n_iter=30)
EM.fit(X_pca)
labels =  EM.predict(X_pca)
n_clusters = best_k - (1 if -1 in labels else 0)


#4.0 Plot clusters
colors = ['blue', 'red', 'green', 'orange', 'brown', 'black']
numbers = np.arange(N)
    
fig, ax = plt.subplots()    
plt.xlim(-0.2, 1.5)
plt.ylim(-1, 0.3)

for i in range(N):
    plt.text(X_pca[i,0], X_pca[i,1], numbers[i], color=colors[labels[i]])
    
ax.grid(True)
fig.tight_layout()
plt.show()


#5.0 Validation
print("-- Silhouette Coefficient: %0.3f\n" % metrics.silhouette_score(datanorm, labels))


#6.0 Results about cost data
labels_l = map(None, labels)
print "-- Numero de clientes por grupo:"
for idx in range(n_clusters):
    print "En el grupo %d (%s) hay %d clientes." % (idx, colors[idx], labels_l.count(idx)) 

print ""
type_per_cluster = {}

for idx in range(N):
    k = labels[idx]    
    
    if k not in type_per_cluster:
        type_per_cluster[k] = []
        
    client = data[idx, :]
    l = type_per_cluster[k]
    l.append(map(None, client))
    
print "-- Distribucion segun el tipo de cliente y region:"
for k in range(n_clusters):
    print "Cluster %d:" % k
    l = type_per_cluster[k]
    l = np.array(l)
    
    l_type = map(None, l[:,0])
    l_region = map(None, l[:,1])
    n_retail = l_type.count(1)
    n_hotel = l_type.count(2)
    n_lisboa = l_region.count(1)
    n_oporto = l_region.count(2)
    n_otros = l_region.count(3)
    
    print "\tTipo--> %s:%d\t%s:%d" % (type_client[1], n_retail, type_client[2], n_hotel)
    print "\tRegion--> %s:%d\t%s:%d\t%s:%d" % (region[1], n_lisboa, region[2], n_oporto, region[3], n_otros)
    
    fresh = np.mean(l[:,2])
    milk = np.mean(l[:,3])
    grocery = np.mean(l[:,4])
    frozen = np.mean(l[:,5])
    paper = np.mean(l[:,6])
    delic = np.mean(l[:,7])
    
    print_l = (fresh, milk, grocery, frozen, paper, delic)    
    print "\tFresco:%0.3f\tLacteos:%0.3f\tUltramarinos:%0.3f" % print_l[0:3]
    print "\tCongelados:%0.3f\tPapeleria:%0.3f\tDelicatessen:%0.3f\n" % print_l[3:6]
    
    
    
    
