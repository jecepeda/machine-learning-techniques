# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 08:32:57 2016

@author: FranciscoP.Romero
"""

# cargar datos y primer gráfico sin clustering.

import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics


# def function load data
def loaddata(filename):
    f = open(filename,'r')
    reader = csv.reader(f)
    c = []
    data = []
    for row in reader:
       data.append([float(row[1]), float(row[2])])
       c.append(int(row[0]))
       
    f.close()
    return c, data
    


def plotdata(data,labels,name): #def function plotdata
#colors = ['black']
    fig, ax = plt.subplots()
    plt.scatter([row[0] for row in data], [row[1] for row in data], c=labels)
    ax.grid(True)
    fig.tight_layout()
    plt.title(name)
    plt.show()


#load and plot data
c,data = loaddata("datos.csv")
#c,data = loadtraffic()
labels = [0 for x in range(len(data))]
plotdata(data,labels,'basic')
#k-means
import sklearn.cluster
k = 3
centroids, labels, z =  sklearn.cluster.k_means(data, k, init="k-means++" )
plotdata(data,labels, 'kmeans')
# 4. Validation
print("Silhouette Coefficient (k-means): %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))

# dbscan
# setting parameters
labels = sklearn.cluster.DBSCAN(eps=0.08, min_samples=10).fit_predict(data)
plotdata(data,labels, 'dbscan')
print("Silhouette Coefficient (dbscan): %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))
      
# expectation maximization
from sklearn.mixture import GMM
classifier = GMM(n_components=3,covariance_type='full', init_params='wc', n_iter=20)
classifier.fit(data)
labels =  classifier.predict(data)
plotdata(data,labels,'em')
print("Silhouette Coefficient (EM): %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))
      
from sklearn import cluster      
spectral = cluster.SpectralClustering(n_clusters=3, eigen_solver='arpack', affinity="nearest_neighbors")
labels = spectral.fit_predict(data)
plotdata(data,labels,'spectral')
print("Silhouette Coefficient (Spectral): %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))
                      
                       