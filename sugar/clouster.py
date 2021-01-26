"""Calculate cloustering."""
# Math libs
import numpy as np
from sklearn import cluster

def km_clust(array, n_clusters):

    # Create a line array, the lazy way
    X = array.reshape((-1, 1))
    # Define the k-means clustering problem
    k_m = cluster.KMeans(n_clusters=n_clusters, n_init=2)
    # Solve the k-means clustering problem
    k_m.fit(X)
    # Get the coordinates of the clusters centres as a 1D array
    values = k_m.cluster_centers_.squeeze()
    # Get the label of each point
    labels = k_m.labels_
    return(values, labels)


def cloustering(img,n):
  # Group similar grey levels using n clusters
  values, labels = km_clust(img, n_clusters = n)
  # Create the segmented array from labels and values
  img_segm = np.choose(labels, values)
  # Reshape the array as the original image
  img_segm.shape = img.shape
  # Get the values of min and max intensity in the original image
  vmin, vmax = np.nanpercentile(img_segm, (1,99))
  return img_segm,vmin,vmax
