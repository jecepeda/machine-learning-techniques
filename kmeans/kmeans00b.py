# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 17:14:12 2016
"""
from sklearn.cluster import KMeans
from sklearn import metrics

# 0. Generating syntethic data (blobs)
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, 
                  shuffle=True, random_state=0)
                  
# plotting the generated data                  
import matplotlib.pyplot as plt
plt.scatter(X[:,0], X[:,1], c='white',s=50)
plt.grid()
plt.show()

# 1. Preprocessing 

# none

# 2. Setting parameters (ad-hoc)

# parameters
init = 'random' # initialization method 
iterations = 10 # to run 10 times with different random centroids to choose the final model as the one with the lowest SSE
max_iter = 300 # maximum number of iterations for each single run
tol = 1e-04 # controls the tolerance with regard to the changes in the within-cluster sum-squared-error to declare convergence
random_state = 0 # random


distortions = []
silhouettes = []

for i in range(2, 11):
    km = KMeans(i, init, n_init = iterations ,max_iter= max_iter, tol = tol,random_state = random_state)
    labels = km.fit_predict(X)
    distortions.append(km.inertia_)
    silhouettes.append(metrics.silhouette_score(X, labels))

# Plot distoritions    
plt.plot(range(2,11), distortions, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.show()

# Plot Silhouette
plt.plot(range(2,11), silhouettes , marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Silohouette')
plt.show()

      
