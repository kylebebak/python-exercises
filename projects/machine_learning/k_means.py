import numpy as np
# for optimizing computations with high dimensional points






max_iterations = 2

# def dist_np(p1, p2):
# 	return np.sqrt(sum((p1 - p2) ** 2))

def dist(p1, p2):
	return pow(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2), .5)

def get_centroid(points):
	# returns a tuple
	d0 = 0
	d1 = 0

	n = 0
	for point in points:
		n += 1
		d0 += point[0]
		d1 += point[1]

	return (d0 / float(n), d1 / float(n))







def k_means(k, points, clusters = None):

	if clusters is None:
		clusters = list()

	if len(clusters) == 0:
		pass
		# initialize by selecting random points for the k clusters and computing their centroids

	elif len(clusters) != k:
		raise Exception("k must match the number of clusters")



	iterations = 0

	while iterations < max_iterations:

		iterations += 1
		changes = 0

		for p, point in enumerate(points):

			closest_cluster_dist = float("inf")
			current_cluster_index = point[1]
			closest_cluster_index = current_cluster_index

			for c, cluster in enumerate(clusters):

				d = dist(cluster[0], point[0])
				if d < closest_cluster_dist:
					closest_cluster_dist = d
					closest_cluster_index = c

			if closest_cluster_index != current_cluster_index:
				point[1] = closest_cluster_index
				clusters[closest_cluster_index][1].append(p)
				if current_cluster_index != -1:
					clusters[current_cluster_index][1].remove(p)

				changes += 1


		if changes == 0:
			print 'iterations: ' + str(iterations)
			return points, clusters

		for cluster in clusters:
			cluster[0] = get_centroid(points[index][0] for index in cluster[1])
			# the economy of list comprehensions!

	print 'iterations: ' + str(iterations)
	return points, clusters













# this program could be rewritten so that each point is an instance of a class, with fields for its position and the cluster to which it belongs, if any. clusters could also be instances of classes, with fields for their centroids and a set of all the points belonging to them, either as indices into a points array, or, more robustly, as references to point objects






points = [[(25,125), 0], [(44,105), 1], [(29,97), 2], [(35,63), 3], [(55,63), 4], [(42,57), 5], [(23,40), 6], [(64,37), 7], [(33,22), 8], [(55,20), 9], [(28,145), -1], [(50,130), -1], [(65,140), -1], [(38,115), -1], [(55,118), -1], [(50,90), -1], [(43,83), -1], [(63,88), -1], [(50,60), -1], [(50,30), -1]]


clusters = list()

for point in points[0:10]:
	clusters.append([point[0], [point[1]]])


points, clusters = k_means(10, points, clusters)

print clusters
