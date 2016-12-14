#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from sklearn.cluster import AgglomerativeClustering



# 0. Load Data
import loaddata
states = loaddata.load_data_usa("2009pivot.csv")

# maybe standarization ....

#1. Clustering
#http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html#sklearn.cluster.AgglomerativeClustering	
model = AgglomerativeClustering(linkage="average", affinity='cityblock', n_clusters=3)
model.fit(states)

print model.labels_

# 5. Show the usa Map
import mapausa
mapausa.show_usa_map(model.labels_)





