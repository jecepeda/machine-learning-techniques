#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  06kmeans.py
#  

import codecs
import numpy
import sklearn.cluster
from sklearn import metrics
from mapausa import show_usa_map

# 0. Load Data
f = codecs.open("./2009pivot.csv", "r", "utf-8")
states = []
count = 0
for line in f:
	if count > 0: 
		# remove double quotes
		row = line.replace ('"', '').split(",")
		row.pop(0)
		if row != []:
			states.append(map(float, row))
	count += 1
	

#1. Preprocessing

# normalization
# dimensionality reduction

	
#2. Setting parameters
k = 3 #??? 



# 2. Clustering execution

# 2.1 random inicialization
centroids, labels, z =  sklearn.cluster.k_means(states, k, init="random" )

# 2.2 k-means ++ 
centroidsplus, labelsplus, zplus =  sklearn.cluster.k_means(states, k, init="k-means++" )


# 3. Validation

print("Silhouette Coefficient (Random): %0.3f"
      % metrics.silhouette_score(numpy.asarray(states), labels))

print("Silhouette Coefficient (Kmeans++): %0.3f"
      % metrics.silhouette_score(numpy.asarray(states), labels))


# 4. Show results
print("Random initialiation")
show_usa_map(labels)

print("Kmeans ++")
show_usa_map(labelsplus)




#print labels
#print labels2
