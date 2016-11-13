# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 17:14:12 2016
"""

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
k = 3 # number of clusters
init = 'random' # initialization method 
iterations = 10 # to run 10 times with different random centroids to choose the final model as the one with the lowest SSE
max_iter = 300 # maximum number of iterations for each single run
tol = 1e-04 # controls the tolerance with regard to the changes in the within-cluster sum-squared-error to declare convergence
random_state = 0 # random

# 3. Clustering execution
from sklearn.cluster import KMeans
km = KMeans(k, init, n_init = iterations ,max_iter= max_iter, tol = tol,random_state = random_state)
y_km = km.fit_predict(X)

# 3. Validation
from sklearn import metrics
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, y_km))
      
print('Distortion: %.2f' % km.inertia_)

#4 . Visualization
plt.scatter(X[:,0], X[:,1], c=y_km,s=50)
plt.grid()
plt.show()
      
      
