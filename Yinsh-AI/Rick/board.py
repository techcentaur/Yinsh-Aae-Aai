from math import cos, sin, pi, isclose
import numpy as np
import matplotlib.pyplot as plt
K = 1
ROUND = 3
TRUNC = 4
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return float('{0:.{1}f}'.format(f, n))
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))


class Board:
	def __init__(self, size=5):
		self.make_board_coordinates(size)
		# E - Empty; BR; WR; BM; WM

		self.state = {}
		for k in self.points:
			self.state[k] = 'E'

		print(self.get_neighbours((0, 0)))


	def make_board_coordinates(self, size):
		points = {}

		for n in range(size+1):
			if not n:
				points[(0.0, 0.0)] = (0.0, 0.0)
			else:
				for m in range(6):
					y = round(truncate(n*K*(cos(m*(pi/3))), TRUNC), ROUND)
					x = round(truncate(n*K*(sin(m*(pi/3))), TRUNC), ROUND)
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
		points = {}
		for i in range(6):
			points[i] = []
			theta = (i*(pi/3)) + (pi/6)
			for j in range(1, 11):
				x2 = round(truncate(x1 + j*K*cos(theta), TRUNC), ROUND)
				y2 = round(truncate(y1 + j*K*sin(theta), TRUNC), ROUND)

				if (x2, y2) in self.points_inverse:
					points[i].append((x2, y2))
		# xli = []
		# yli = []
		# for k in self.points:
		# 	xli.append(self.points[k][0])
		# 	yli.append(self.points[k][1])
		# x = np.array(xli)
		# y = np.array(yli)
		# plt.scatter(x, y)
		
		# xli = []
		# yli = []
		# for k in points:
		# 	xli.append(k[0])
		# 	yli.append(k[1])
		# x = np.array(xli)
		# y = np.array(yli)
		# plt.scatter(x, y, color='red')
		# plt.show()
		# print(points)
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


	def get_neighbours(self, point):
		points_to_go = []
		points_in_lines = self.lines(point)

		for key in points_in_lines:
			marker_jump = 0
			for p_inv in points_in_lines[key]:
				p = self.points_inverse[p_inv]
				if marker_jump == 0:
					if self.state[p] is 'E':
						points_to_go.append(p)
					elif self.state[p] is 'BR' or self.state[p] is 'WR':
						break
					elif self.state[p] is 'WM' or self.state[p] is 'BM':
						marker_jump += 1
				elif marker_jump == 1:
					if self.state[p] is 'E':
						points_to_go.append(p)
						break
					elif self.state[p] is 'BR' or self.state[p] is 'WR':
						break

		print(points_to_go)

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
		for k in points_to_go:
			xli.append(self.points[k][0])
			yli.append(self.points[k][1])
		x = np.array(xli)
		y = np.array(yli)
		plt.scatter(x, y, color='red')
		plt.show()

		return points_to_go

if __name__ == '__main__':
	b = Board()