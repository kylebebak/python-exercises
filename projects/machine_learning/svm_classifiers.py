w = (-1, 1)
b = -2
margin = 1

points = [((5,10), 1), ((7,10), 1), ((1,8), 1), ((3,8), 1), ((7,8), 1), ((1,6), 1), ((3,6), 1), ((3,4), 1), ((5,8), -1), ((5,6), -1), ((7,6), -1), ((1,4), -1), ((5,4), -1), ((7,4), -1), ((1,2), -1), ((3,2), -1)]


def dot_product(v1, v2):

	sum = 0
	for i in range(len(v1)):
		sum += v1[i] * v2[i]

	return sum


def sign(x):
	if x >= 0:
		return 1
	return -1



# this applies the so-called hinge loss, which adds a linear slack cost to any point not at least margin distance away from the decision boundary
for point in points:
	y = point[1]
	prediction = sign(y) * (dot_product(point[0], w) + b)

	slack = max(0, 1 - prediction)

	print point[0], slack




