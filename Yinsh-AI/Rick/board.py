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

	def __init__(self, size=5, other_player=1):
		self.player = other_player - 1
		# player 1 is white, player 2 is black
		# self.player = 1 -> white
		# self.player = 0 -> black
		self.size = size
		# E - Empty; BR; WR; BM; WM

		self.rings = {1: [], 0: []}
		self.state = {}
		for k in self.points:
			self.state[k] = 'E'

		self.__utility__ = None

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


	def normie_f(self):
		self.state[(1,3)] = 'WR'
		self.rings[1].append((1,3))
		self.state[(2,1)] = 'WR'
		self.rings[1].append((2, 1))
		self.state[(2,5)] = 'WR'
		self.rings[1].append((2, 5))
		self.state[(0,0)] = 'WR'
		self.rings[1].append((0, 0))
		self.state[(3,4)] = 'WR'
		self.rings[1].append((3, 4))
		self.state[(3,8)] = 'BR'
		self.rings[0].append((3, 8))
		self.state[(2,9)] = 'BR'
		self.rings[0].append((2,9))
		self.state[(3,13)] = 'BR'
		self.rings[0].append((3,13))
		self.state[(4,7)] = 'BR'
		self.rings[0].append((4,7))
		self.state[(1,5)] = 'BR'
		self.rings[0].append((1,5))
		self.state[(3,3)] = 'BM'
		self.state[(4,3)] = 'WM'
		self.state[(4,2)] = 'WM'
		self.state[(4,1)] = 'WM'
		self.state[(4,0)] = 'WM'
		self.state[(5,29)] = 'WM'
		self.state[(5,24)] = 'BM'

		return True


	def display_board(self):
		E = []
		WM = []
		BM = []
		WR = []
		BR = []
		for p, v in self.state.items():
			if v is 'E':
				E.append(self.points[p])
			elif v is 'WM':
				WM.append(self.points[p])
			elif v is 'BM':
				BM.append(self.points[p])
			elif v is 'WR':
				WR.append(self.points[p])
			elif v is 'BR':
				BR.append(self.points[p])
		plt.scatter(np.array([x for (x,y) in E]), np.array([y for (x,y) in E]), color='grey')
		plt.scatter(np.array([x for (x,y) in BM]), np.array([y for (x,y) in BM]), color='orange')
		plt.scatter(np.array([x for (x,y) in BR]), np.array([y for (x,y) in BR]), color='red')
		plt.scatter(np.array([x for (x,y) in WM]), np.array([y for (x,y) in WM]), color='green')
		plt.scatter(np.array([x for (x,y) in WR]), np.array([y for (x,y) in WR]), color='blue')
		plt.show()

	def display_direction_lines(self, l, inverse=True):
		xli = []
		yli = []
		for k in self.points:
			xli.append(self.points[k][0])
			yli.append(self.points[k][1])
		x = np.array(xli)
		y = np.array(yli)
		plt.scatter(x, y)

		if inverse:
			xx=[]
			yy=[]
			for k,v in l.items():
				for vv in v:
					xx.append(vv[0])
					yy.append(vv[1])
			plt.scatter(np.array(xx), np.array(yy), color='brown')
		else:
			xx=[]
			yy=[]
			for k,v in l.items():
				for vv in v:
					vvv = self.points[vv]
					xx.append(vvv[0])
					yy.append(vvv[1])
			plt.scatter(np.array(xx), np.array(yy), color='brown')

		plt.show()

	def get_neighbours(self):
		neighbour_boards = []

		for ring in self.rings[self.player]:
			points_to_go = {}
			points_in_lines = self.lines(ring)
			# points_in_lines = {'0':[(1.2343, 2.00)], '1': [()] ...}

			# See which positions it is possible to go
			for key in points_in_lines:
				points_to_go[key] = []

				marker_jump = 0
				for p_inv in points_in_lines[key]:
					p = self.points_inverse[p_inv]
					if marker_jump == 0:
						if self.state[p] is 'E':
							points_to_go[key].append(p_inv)
						elif self.state[p] is 'BR' or self.state[p] is 'WR':
							break
						elif self.state[p] is 'WM' or self.state[p] is 'BM':
							marker_jump += 1
					elif marker_jump == 1:
						if self.state[p] is 'E':
							points_to_go[key].append(p_inv)
							break
						elif self.state[p] is 'BR' or self.state[p] is 'WR':
							break
							
			# Get neighbours board by moving the particular positions. Wubba Lubba Dub Dub!
			for key in points_in_lines:
				for point1 in points_to_go[key]:
					flip_markers = []
					for point2 in points_in_lines[key]:
						if point1 == point2:
							neighbour_boards.append(self.make_board(ring, self.points_inverse[point2], flip_markers))
						else:
							if self.state[self.points_inverse[point2]] is 'E':
								pass
							else:
								flip_markers.append(self.points_inverse[point2])

		return neighbour_boards

	def make_board(self, point_at_ring, point_to_go, flip_markers):
		new_board = Board()
		new_board.state = self.state.copy()
		new_board.state[point_to_go] = self.state[point_at_ring]
		
		if self.state[point_at_ring] is 'WR':
			new_board.state[point_at_ring] = 'WM'
		elif self.state[point_at_ring] is 'BR':
			new_board.state[point_at_ring] = 'BM'

		for mark in flip_markers:
			if self.state[mark] is 'WM':
				new_board.state[mark] = 'BM'
			elif self.state[mark] is 'BM':
				new_board.state[mark] = 'WM'

		return new_board

	@property
	def utility(self):
		if self.__utility__ is not None:
			return self.__utility__
		else:
			return self.__utility_function__()

	def __utility_function__(self):
		all_lines = self.all_lines() # get all directional lines
		
		player1_markers = 0
		player2_markers = 0

		for vertical_line_index in [18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 31]:
			for coordinate in all_lines[vertical_line_index]:
				mark = self.state[self.points_inverse[coordinate]]
				if mark is 'WM':
					player1_markers += 1
				elif mark is 'BM':
					player2_markers += 1 

		p1 = 0; p1_row = 0; player1_continous_flag = False
		p2 = 0; p2_row = 0; player2_continous_flag = False

		for line in all_lines:
			for point in line:
				if self.state[self.points_inverse[point]] is 'WM':
					p1 += 1
					player1_continous_flag = True; player2_continous_flag = False
					if p1 >= 5 and player1_continous_flag:
						# 5 continous markers -> a row, give high score
						p1_row = 20
						break
				elif self.state[self.points_inverse[point]] is 'BM':
					p2 += 1
					player1_continous_flag = False; player2_continous_flag = True
					if p2 >= 5 and player2_continous_flag:
						# 5 continous markers -> a row, give low score
						p2_row = -20
						break
				else:
					p1 = 0; p2 = 0
					player1_continous_flag = False; player2_continous_flag = False


		player1_score = player1_markers + p1_row
		player2_score = player2_markers + p2_row
		print(player1_score)
		print(player2_score)

		if self.player:
			score = player2_score - player1_score
		else:
			score = player1_score - player2_score

		self.__utility__ = score
		return self.__utility__

if __name__ == '__main__':
	b = Board()
	b.normie_f()
	# b.display_board()
	# b.get_neighbours((3,4))
	# b.display_board()
	# print(b.utility)
	b.display_board()
	# print(len(b.get_neighbours()))
	for n in b.get_neighbours():
		n.display_board()