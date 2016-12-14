# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 13:25:54 2016

@author: FranciscoP.Romero
"""

# cargar datos y primer gráfico sin clustering.

import csv
import matplotlib.pyplot as plt
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
    
#def function plotdata
def plotdata(data,labels,name): 
    fig, ax = plt.subplots()
    plt.scatter([row[0] for row in data], [row[1] for row in data], c=labels)
    ax.grid(True)
    fig.tight_layout()
    plt.title(name)
    plt.show()
    
def plot_confusion_matrix(cm, y_true, y_pred, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(set(y_true)))
    plt.xticks(tick_marks, set(y_pred), rotation=45)
    plt.yticks(tick_marks, set(y_true))
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
#0 .Load and Plot data
c,data = loaddata("datos.csv")
plotdata(data,c,'basic')


#1. Clustering: k-means
import sklearn.cluster
k = 3
centroids, labels, z =  sklearn.cluster.k_means(data, k, init="k-means++" )
plotdata(data,labels, 'kmeans')
## add 1 to name correspondence
labels = [l+1 for l in labels]

# compute the confussion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_true=c, y_pred=labels)
np.set_printoptions(precision=2)

# plot and show the confussion matrix
print('Confusion matrix, without normalization')
print(cm)
plt.figure()
plot_confusion_matrix(cm, c, labels)


# show the classificacion report 
from sklearn.metrics import classification_report
print(classification_report(y_true=c, y_pred=labels))


# Normalize the confusion matrix by row (i.e by the number of samples
# in each class)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
print('Normalized confusion matrix')
print(cm_normalized)
plt.figure()
plot_confusion_matrix(cm_normalized, c, labels, title='Normalized confusion matrix')

plt.show()


