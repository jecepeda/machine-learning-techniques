import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler

from models import retrieve_data

data = retrieve_data()

n_of_clusters = 110 # Optimal K value (from k-means)


def apply_spectral(datai, n_of_clustersi):

    #For later plotting
    colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
    colors = np.hstack([colors] * 20)

    plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05,
                    hspace=.01)

    plot_num = 1
    #Until here

    X = datai

    X = StandardScaler().fit_transform(X)

    spectral = cluster.SpectralClustering(n_clusters = n_of_clustersi, eigen_solver='arpack', affinity="nearest_neighbors")
    spectral.fit(X)

    if hasattr(spectral, '_labels'):
        labels = spectral.labels_.astype(np.int)
    else:
        labels = spectral.predict(X)

    #More plotting
    #plt.subplot(4, 1, plot_num)
    plt.scatter(X[:, 0], X[:, 1], color=colors[labels].tolist(), s=10)

    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.xticks(())
    plt.yticks(())
    plt.show()


apply_spectral(data, n_of_clusters)
