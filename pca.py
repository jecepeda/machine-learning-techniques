from models import get_db_session,  Cluster
from sklearn.decomposition import PCA
from sklearn import preprocessing


#Get 
states = [] #Get all data without labels in vectors, then into a vector

#Normalization
minmaxscaler = preprocessing.MinMaxScaler()
states = min_max_scaler.fit_transform(states)
print (states)

#PCA Estimation
estimator = PCA (n_components = 3) # Number of components left 
Xpca = estimator.fit_transform(states)
print (X_pca)

#3. k-means clustering
k = 3
centroids, labels, z =  sklearn.cluster.k_means(states, k, init="k-means++" )

#4.  plot 
colors = ['blue', 'red', 'green']
numbers = numpy.arange(len(X_pca))

fig, ax = plt.subplots()

for i in range(len(X_pca)):
    plt.text(X_pca[i][0], X_pca[i][1], numbers[i], color=colors[labels[i]]) 
   
plt.xlim(-1, 4)
plt.ylim(-0.2, 1)


ax.grid(True)
fig.tight_layout()

plt.show()

