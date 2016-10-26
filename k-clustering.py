from models import plot_data, retrieve_data
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
import math
from sklearn.datasets import make_blobs

data = retrieve_data()
X = [row[0] for row in data]
y = [row[1] for row in data]
print(X)
print(y)

n_of_elements = 7930
init = 'random'
iterations = 1
max_iter = 300
tol = 1e-04
random_state = 0

def n_of_clusters_and_distortion(data, iters=10):
    sqrt_elements = int(math.sqrt(n_of_elements))
    print(sqrt_elements)
    range_clusters = range(sqrt_elements, sqrt_elements + iters)
    distortions = []
    silhouettes = []
    for i in range_clusters:
        km = KMeans(i, init, n_init=iterations ,max_iter=max_iter, tol = tol,random_state = random_state)
        print("{} {}".format(sqrt_elements, i))
        labels = km.fit_predict(X)
        distortions.append(km.inertia_)
        silhouettes.append(metrics.silhouette_score(X, labels))
    plot_distortion(range_clusters, distortions)
    plot_silhouette(range_clusters, silhouettes)

def plot_distortion(data, distortions, title="Distortions"):
    plt.plot(data, distortions, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortions')
    plt.title(title)
    plt.show()

def plot_silhouette(data, silhouettes, title="Silhouette"):
    plt.plot(data, silhouettes, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette')
    plt.title(title)
    plt.show()


n_of_clusters_and_distortion(data)
