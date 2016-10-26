# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 08:32:57 2016

@author: FranciscoP.Romero
"""

import csv
import matplotlib.pyplot as plt
import sklearn.neighbors
import numpy as np


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


# 0. load and plot data (datos.csv)
c,data = loaddata("datos.csv")
labels = [0 for x in range(len(data))]
plotdata(data,labels,'basic')


# 1. setting parameters
k = 3
init = "k-means++"

# 2. Execute clustering 

import sklearn.cluster
centroids, labels, z =  sklearn.cluster.k_means(data, k, init)

# 3. Plot the results
plotdata(data,labels, 'kmeans')

# 4. Validation
from sklearn import metrics
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))

                       
                       