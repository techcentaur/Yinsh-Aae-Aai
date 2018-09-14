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
	points = {}
	size = 5

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
	for i in [(5, i*5) for i in range(6)]:
		points.pop(i)
	points = points
	points_inverse = {v:k for k,v in points.items()}

	def __init__(self, size=5):
		self.size = size
		# E - Empty; BR; WR; BM; WM

		self.state = {}
		for k in self.points:
			self.state[k] = 'E'

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
				else:
					break
		return points


	def all_lines(self):
		lines = []
		for i in range(3):
			angles = ((pi/2)-(i*(pi/3)), (pi/2)-((i+1)*(pi/3)))
			for j in range(self.size):
				if not j:
					x1, y1 = self.points[(self.size-1, (i*(self.size-1))+j)]
				else:
					x1, y1 = self.points[(self.size, (i*(self.size))+j)]
				for theta in angles:
					if not round(truncate(cos(theta), TRUNC), ROUND):
						continue 
					line = []
					line.append((x1, y1))
					for k in range(1, 11):
						x2 = round(truncate(x1 - k*K*cos(theta), TRUNC), ROUND)
						y2 = round(truncate(y1 - k*K*sin(theta), TRUNC), ROUND)
						if (x2, y2) in self.points_inverse:
							line.append((x2, y2))
						else:
							break
					lines.append(line)
				if not j and i != 2:
					del lines[-1]
		for i in range(-self.size+1, self.size):
			if i < 0:
				i = (self.size*6 + i)
			if not i:
				x1, y1 = self.points[(self.size-1, 0)]
			else:
				x1, y1 = self.points[(self.size, i)]
			line = []
			line.append((x1, y1))
			for k in range(1, 11):
				x2 = x1
				y2 = round(truncate(y1 - k*K, TRUNC), ROUND)
				if (x2, y2) in self.points_inverse:
					line.append((x2, y2))
				else:
					break
			lines.append(line)
		for i in range(6):
			lines.append([self.points[(self.size, (self.size*i)+1+j)] for j in range(self.size-1)])
		return lines


	def display_points(self, points):
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
		points_to_go = {}
		points_in_lines = self.lines(point)
		# points_in_lines = {'0':[(1.2343, 2.00)], '1': [()] ...}

		# See which positions it is possible to go
		for key in points_in_lines:
			points_to_go[key] = []

			marker_jump = 0
			for p_inv in points_in_lines[key]:
				p = self.points_inverse[p_inv]
				if marker_jump == 0:
					if self.state[p] is 'E':
						points_to_go[key].append(p)
					elif self.state[p] is 'BR' or self.state[p] is 'WR':
						break
					elif self.state[p] is 'WM' or self.state[p] is 'BM':
						marker_jump += 1
				elif marker_jump == 1:
					if self.state[p] is 'E':
						points_to_go[key].append(p)
						break
					elif self.state[p] is 'BR' or self.state[p] is 'WR':
						break

		neighbour_boards = []
		# Get neighbours board by moving the particular positions. Wubba Lubba Dub Dub!
		for key in points_in_lines:
			for point1 in points_to_go[key]:
				flip_markers = []
				for point2 in points_in_lines[key]:
					if point1 == point2:
						# point_current is ring and will be marker
						# _point is empty and will be ring
						# flip the markers in the flip_markers																						p
						neighbour_boards.append(self.make_board(point, point2, flip_markers))
					else:
						if self.state[point2] is 'E':
							pass
						else:
							flip_markers.append(point2)

		return neighbour_boards


	def make_board(self, point_at_ring, point_to_go, flip_markers):
		new_board = Board()
		new_board.state = self.state
		new_board.state[point_to_go] = self.state[point_at_ring]
		
		if self.state[point_at_ring] is 'WR':
			new_board.state[point_at_ring] = 'WM'
		else:
			new_board.state[point_at_ring] = 'BM'

		for mark in flip_markers:
			if self.state[mark] is 'WM':
				new_board.state[mark] = 'BM'
			else:
				new_board.state[mark] = 'WM'

		return new_board


	def utility_function(self):
		all_lines = self.all_lines()

		player1_markers = 0
		player2_markers = 0
		player1_continous_flag = False
		player2_continous_flag = False

		for line in all_lines:
			for point in line:
				if self.state[point] is 'BM':
					player1_markers += 1
					player1_continous_flag = True
					player2_continous_flag = False
					if player1_markers >= 5 and player1_continous_flag:
						# 5 continous markers in a row, instantly do this
						break
				elif self.state[point] is 'WM':
					player2_markers += 1
					player1_continous_flag = False
					player2_continous_flag = True
					if player2_markers >= 5 and player2_continous_flag:
						# 5 continous markers in a row, never do this
						break
				else:
					player1_continous_flag = False
					player2_continous_flag = False


		player1_markers = 0
		player2_markers = 0

		# for only vertical lines:
		

if __name__ == '__main__':
	b = Board()