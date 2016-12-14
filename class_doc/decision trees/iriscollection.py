# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:12:47 2015

@author: paskualf
"""

from sklearn.datasets import load_iris
from sklearn import tree

# THE IRIS DATA SET: https://archive.ics.uci.edu/ml/datasets/Iris
iris = load_iris()
print(iris.feature_names)

# elements
iris.data
#class to predict
iris.target

# http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)




# plot the decision tree: 
# http://nbviewer.jupyter.org/github/kittipatkampa/python_dev/blob/master/demo_decision_tree_v1.ipynb
from sklearn.externals.six import StringIO  
import pydot 

# It is necessary to install GraphViz
# http://www.graphviz.org/Download..php


## Extract the decision tree logic from the trained model
dot_data = StringIO() 
tree.export_graphviz(clf, out_file=dot_data,  
                         feature_names=iris.feature_names,  
                         class_names=iris.target_names,  
                         filled=True, rounded=True,  
                         special_characters=True)

## convert the logics into graph
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 

## This will plot decision tree in pdf file
graph.write_pdf(path="iris.pdf") 


