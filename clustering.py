from sklearn import neighbors
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import DBSCAN as dbscan
from sklearn import metrics
import numpy as np
from models import retrieve_data, plot_data

def load_and_plot_data():
    data = retrieve_data(data="longitud, latitud")
    plot_data(data)
    return data

def plot_cluster_data(accident_locations, minimum_points, eps=0.10):
    labels = dbscan(eps=eps, min_samples=minimum_points).fit_predict(accident_locations)
    n_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    title = "dbscan: eps:{} Clusters:{}".format(eps, n_of_clusters)
    print(labels)
    plot_data(accident_locations, labels, title)
    print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(np.asarray(data), labels))

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
    plot_cluster_data(data, minimum_points=10, eps=0.01)
