# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:01:44 2016

@author: FranciscoP.Romero
"""

import matplotlib.pyplot as plt

# 0. Data: Generating syntetic data
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=200, noise=0.05,random_state=0)
# plot the data
plt.scatter(X[:,0], X[:,1])
plt.show()

# 1. Settiqng Parameters


# 2. DBSCAN execution
from sklearn.cluster import DBSCAN
# how are chosen eps and minpts??
db = DBSCAN(eps=0.2, min_samples=5, metric='euclidean')
y_db = db.fit_predict(X)

#3. Validation/Evaluation
# Only using silhouette coefficient
from sklearn import metrics
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, y_db))
      
     
# 4. Plot results

plt.scatter(X[y_db==0,0], X[y_db==0,1], c='lightblue', marker='o', s=40, label='cluster 1')
plt.scatter(X[y_db==1,0], X[y_db==1,1], c='red', marker='s', s=40, label='cluster 2')
plt.legend()
plt.show()
