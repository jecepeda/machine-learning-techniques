# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 08:32:57 2016

@author: FranciscoP.Romero
"""

# cargar datos y primer gráfico sin clustering.

import csv
import matplotlib.pyplot as plt



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
    

import re
TAG_RE = re.compile(r'<[^>]*>')
def remove_tags(text):
    return TAG_RE.sub('', text)
    
def loadtraffic():
    X = []
    lat = 0
    lng = 0
    f = open("./inctrafico.xml")
    for linea in f:
      cadena = linea.split("><")
      for c in cadena:
         if c.find("longitud") != -1:
			  lng = float(remove_tags("<" + c + ">").strip())
         elif c.find("latitud") != -1:
			  lat = float(remove_tags("<" + c + ">").strip())
         elif c.find("/incidenciaGeolocalizada") != -1:
		  if lat > 0 :
			data = [lng, lat]
			X.append(data)
    
    c = [0 for x in range(len(data))]
    
    return c, X

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

# dbscan
# setting parameters
labels = sklearn.cluster.DBSCAN(eps=0.08, min_samples=10).fit_predict(data)
plotdata(data,labels, 'dbscan')

#hierarchical clustering
model = sklearn.cluster.AgglomerativeClustering(n_clusters=3,linkage="complete", affinity='euclidean')
labels = model.fit_predict(data)
plotdata(data,labels, 'hierarchical ward')

from scipy import cluster
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(data)
clusters = cluster.hierarchy.linkage(matsim, method = 'single')
labels = cluster.hierarchy.fcluster(clusters, 21, criterion = 'distance')
plotdata(data,labels, 'hierarchical single')


# expectation maximization
from sklearn.mixture import GMM
classifier = GMM(n_components=3,covariance_type='full', init_params='wc', n_iter=20)
classifier.fit(data)
labels =  classifier.predict(data)
plotdata(data,labels,'em')


# pca + k-means (doubtful results)
from sklearn.decomposition import PCA
estimator = PCA (n_components = 2)
X_pca = estimator.fit_transform(data)
centroids, labels, z =  sklearn.cluster.k_means(X_pca, n_clusters=3, init="k-means++" )
plotdata(data,labels,'pca+k')

                       
                       