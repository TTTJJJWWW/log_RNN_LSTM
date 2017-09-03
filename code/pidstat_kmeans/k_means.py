import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  
  
def eucl_distance(vector1, vector2):  
  return np.sqrt(np.sum(np.power(vector2 - vector1, 2)))  
  
# init centroids with random samples  
def init_centroids(dataSet, k):  
  numSamples, dim = dataSet.shape  
  centroids = np.zeros((k, dim))  
  for i in range(k):  
    index = int(np.random.uniform(0, numSamples))  
    centroids[i, :] = dataSet[index, :]  
  return centroids  
  
# k-means cluster  
def kmeans(dataSet, k):  
  numSamples = dataSet.shape[0]  
  # first column stores which cluster this sample belongs to,  
  # second column stores the error between this sample and its centroid  
  clusterAssment = np.mat(np.zeros((numSamples, 2)))  
  clusterChanged = True  

  # step 1: init centroids  
  centroids = init_centroids(dataSet, k)  
  while clusterChanged:  
    clusterChanged = False  
    for i in xrange(numSamples):  
      minDist  = 100000.0  
      minIndex = 0  

      # step 2: for each centroid find the centroid who is closest  
      for j in range(k):  
        distance = eucl_distance(centroids[j, :], dataSet[i, :]) 		
        if distance < minDist:  
          minDist  = distance  
          minIndex = j  
		  
      # step 3: update its cluster  
      if clusterAssment[i, 0] != minIndex:  
        clusterChanged = True  
        clusterAssment[i, :] = minIndex, minDist**2  

    # step 4: update centroids  
    for j in range(k):  
      pointsInCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == j)[0]]  
      centroids[j, :] = np.mean(pointsInCluster, axis = 0)  
  #print clusterAssment
  return centroids, clusterAssment  
  
# show your cluster only available with 2-D data  
def show_cluster(dataSet, k, centroids, clusterAssment, node):  
  numSamples, dim = dataSet.shape  
  if dim != 2:  
    print "Sorry, the dimension of your data is not 2!"  
    return 1  
  mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
  if k > len(mark):  
    print "Sorry! Your k is too large! please contact Zouxy"  
    return 1  

  # draw all samples  
  for i in xrange(numSamples):  
    markIndex = int(clusterAssment[i, 0])  
    plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])  
  mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb'] 
	
  # draw the centroids  
  for i in range(k):  
    plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12) 
  plt.savefig('pidstat-kmeans-%s.png' % node)	
  plt.show()  
	