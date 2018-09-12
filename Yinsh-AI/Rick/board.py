from math import cos, sin, pi, isclose
import numpy as np
import matplotlib.pyplot as plt
K = 1
ROUND = 4

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return float('{0:.{1}f}'.format(f, n))
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))


class Board:
	def __init__(self, size=5):
		points = {}

		for n in range(size+1):
			if not n:
				points[(0, 0)] = (0, 0)
			else:
				for m in range(6):
					y = n*K*(cos(m*(pi/3)))
					x = n*K*(sin(m*(pi/3)))
					points[(n, m*n)] = (x, y)

		for key in range(2, size+1):
			for i in range(6):
				(x1, y1) = points[(key, i*key)]
				(x2, y2) = points[(key, (((i+1)*key) % (key*6)))]

				for t in range(1, key):
					x = (x1*(key - t) + x2*t) / key
					y = (y1*(key - t) + y2*t) / key

					points[(key, key*i + t)] = (x, y)
		for i in [(size, i*size) for i in range(6)]:
			points.pop(i)
		self.points = points
		self.points_inverse = {v:k for k,v in self.points.items()}


	def lines(self, point):
		x1, y1 = self.points[point]
		points = []
		for i in range(6):
			theta = (i*(pi/3)) + (pi/6)
			for j in range(1, 11):
				x2 = x1 + j*K*cos(theta)
				y2 = y1 + j*K*sin(theta)
				for k in self.points_inverse:
					if isclose(x2, k[0], rel_tol=1e-04) and isclose(y2, k[1], rel_tol=1e-04):
						points.append((x2, y2))
				# if (x2, y2) in self.points_inverse:
				# 	points.append((x2, y2))
		xli = []
		yli = []
		for k in self.points:
			xli.append(self.points[k][0])
			yli.append(self.points[k][1])
		x = np.array(xli)
		y = np.array(yli)
		plt.scatter(x, y)
		
		xli = []
		yli = []
		for k in points:
			xli.append(k[0])
			yli.append(k[1])
		x = np.array(xli)
		y = np.array(yli)
		plt.scatter(x, y, color='red')
		plt.show()

		return points


	def display_points(self, points):
		xli = []
		yli = []
		for k in points:
			xli.append(k[0])
			yli.append(k[1])
		x = np.array(xli)
		y = np.array(yli)
		plt.scatter(x, y)
		plt.show()


	def display(self):
		xli = []
		yli = []
		for k in self.points:
			xli.append(self.points[k][0])
			yli.append(self.points[k][1])
		x = np.array(xli)
		y = np.array(yli)
		plt.scatter(x, y)
		plt.show()
