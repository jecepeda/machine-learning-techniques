# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 16:59:08 2015

@author: FranciscoP.Romero
"""
import codecs
import pylab
import scipy.cluster.hierarchy as sch
import sklearn.neighbors
import numpy
from sklearn import preprocessing 

# 0. Load Data
f = codecs.open("2009pivot.csv", "r", "utf-8")
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


#states = preprocessing.normalize(states) 
min_max_scaler = preprocessing.MinMaxScaler()
states = min_max_scaler.fit_transform(states)

dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
D = dist.pairwise(states)
D2 = dist.pairwise(numpy.transpose(states))

print D.shape
print D2.shape


# Compute and plot first dendrogram.
fig = pylab.figure(figsize=(8,8))
ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
Y = sch.linkage(D, method='ward')
Z1 = sch.dendrogram(Y, orientation='right')
ax1.set_xticks([])
ax1.set_yticks([])

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Y = sch.linkage(D2, method='centroid')
Z2 = sch.dendrogram(Y)
ax2.set_xticks([])
ax2.set_yticks([])



# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
idx2 = Z2['leaves']
D = D[idx1,:]
D = D[:,idx2]
im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu)


axmatrix.set_xticks(range(D2.shape[0]))
axmatrix.set_xticklabels(idx2, minor=False)
axmatrix.xaxis.set_label_position('bottom')
axmatrix.xaxis.tick_bottom()

pylab.xticks(rotation=-90, fontsize=8)

axmatrix.set_yticks(range(D.shape[0]))
axmatrix.set_yticklabels(idx1, minor=False)
axmatrix.yaxis.set_label_position('right')
axmatrix.yaxis.tick_right()


# Plot colorbar.
#axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
#pylab.colorbar(im, cax=axcolor)

fig.show()
fig.savefig('dendrogram.png')