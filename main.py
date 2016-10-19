import sqlite3
import matplotlib.pyplot as plt
from sklearn import neighbors
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import DBSCAN as dbscan

def retrieve_data(db='incidences.db', data='*', tipo='Accidente'):
    conn = sqlite3.connect(db)
    query_result = conn.execute("SELECT {} FROM Incidencia WHERE tipo = '{}';".format(data, tipo))
    ret= [row for row in query_result]

    return ret

def plot_data(data, labels = 'b', title= 'default'):
    plt.scatter([row[0] for row in data],[row[1] for row in data], c=labels)
    plt.title(title)
    plt.show()

def load_and_plot_data():
    data = retrieve_data(data="longitud, latitud")
    plot_data(data)
    return data

def plot_cluster_data(accident_locations, minimum_points, eps=0.10):
    labels = dbscan(eps=eps, min_samples=minimum_points).fit_predict(accident_locations)
    n_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    title = "dbscan: eps:{} Clusters:{}".format(eps, n_of_clusters)
    plot_data(accident_locations, labels, title)
    
def plot_eps(data):
    dist = neighbors.DistanceMetric.get_metric('euclidean')
    mat_sim = dist.pairwise(data)
    minimum_points = 10

    graph = kneighbors_graph(data, minimum_points, include_self=False)
    array_graph = graph.toarray()
    seq = []
    for i, _ in enumerate(data):
        for j in range(len(data)):
            if array_graph[i][j] != 0:
                seq.append(mat_sim[i][j])
    seq.sort()
    plt.plot(seq)
    plt.show()

if __name__ == "__main__":
    data = load_and_plot_data()
    plot_cluster_data(data, minimum_points=10, eps=0.0180)
