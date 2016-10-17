import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics

def execute_main():
    load_and_plot_data();

def retrieve_data(db='incidences.db', data='*', tipo='Accidente'):
    ret = []
    conn = sqlite3.connect(db)
    d = conn.execute("SELECT "+ data +" FROM Incidencia WHERE tipo='"+ tipo +"';")
    for row in d:
        ret.append(row)

    return ret

def plot_data(data):
    plt.scatter([row[0] for row in data],[row[1] for row in data])
    plt.title('Accidentes Graph')
    plt.show()

def load_and_plot_data():
    data = retrieve_data(data="longitud, latitud")
    plot_data(data)

def sil_coeff():
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(np.asarray(data), labels))

if __name__ == "__main__":
    execute_main()

