from models import get_db_session, Test, Train
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn import neighbors
import pandas as pd
import matplotlib.pyplot as plt

'''
Obtenemos la sesion de la base de datos
y extraemos los datos obtenidos para tests
'''

session = get_db_session("sqlite:///incidences.db")
tests = session.query(Test.latitud, Test.longitud).all()
trains = session.query(Train.latitud, Train.longitud).all()

n = 150
knn_errors = [0 for 0 in range(1, n)]

for n_of_neighbours in range(1, n):
    classifier = neighbors.KNeighborsClassifier(
        n_of_neighbours, weights='distance')



print("Length of the tests: {}".format(len(tests)))
