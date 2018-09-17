from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import copy

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

	def __init__(self, player=2, size=5):
		self.player = player - 1
		# player 1 is white -> 0, player 2 is black -> 1
		self.size = size
		# E - Empty; BR; WR; BM; WM

		self.rings = {1: [], 0: []}
		self.state = {}
		for k in self.points:
			self.state[k] = 'E'
		self.moves = [None, None, [], []]
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
		plt.scatter(np.array([x for (x,y) in BM]), np.array([y for (x,y) in BM]), color='green')
		plt.scatter(np.array([x for (x,y) in BR]), np.array([y for (x,y) in BR]), color='blue')
		plt.scatter(np.array([x for (x,y) in WM]), np.array([y for (x,y) in WM]), color='orange')
		plt.scatter(np.array([x for (x,y) in WR]), np.array([y for (x,y) in WR]), color='red')
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

	def execute_move(self, moves):
		lines = self.lines(moves[0])
		line = None
		idx = None
		for idx, line in lines.items():
			if self.points[moves[1]] in line:
				idx = line.index(self.points[moves[1]])
				break

		for p in line[:idx]:
			if self.state[self.points_inverse[p]] is 'BM':
				self.state[self.points_inverse[p]] = 'WM'
			elif self.state[self.points_inverse[p]] is 'WM':
				self.state[self.points_inverse[p]] = 'BM'
		
		if self.state[moves[0]]  is 'WR':
			self.state[moves[0]] = 'WM'
			self.state[moves[1]] = 'WR'
		elif self.state[moves[0]]  is 'BR':
			self.state[moves[0]] = 'BM'
			self.state[moves[1]] = 'BR'

		self.rings[int(not bool(self.player))].remove(moves[0])
		self.rings[int(not bool(self.player))].append(moves[1])

		for (p1, p2) in moves[2]:
			lines = self.lines(p1)
			line = None
			idx = None
			for idx, line in lines.items():
				if self.points[p2] in line:
					idx = line.index(self.points[p2])
					break
			
			for p in [self.points[p1]] + line[:idx+1]:
				self.state[self.points_inverse[p]] = 'E'
		
		for pp in moves[3]:
			self.state[pp] = 'E'
			self.rings[int(not bool(self.player))].remove(pp)

		while True:
			util = self.__utility_function__()
			if util is not False:
				break

	def make_board(self, point_at_ring, point_to_go, flip_markers):
		new_board = Board(player = (1 + (1 - self.player)))
		new_board.state = self.state.copy()
		new_board.state[point_to_go] = self.state[point_at_ring]
		
		new_board.rings = copy.deepcopy(self.rings)
		new_board.rings[self.player].remove(point_at_ring)
		new_board.rings[self.player].append(point_to_go)
		new_board.moves[0] = point_at_ring
		new_board.moves[1] = point_to_go
		
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
			while True:
				util = self.__utility_function__()
				if util is not False:
					return self.__utility__

	def __utility_function__(self):
		# print('calcultatin utility...')
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

		# print('all lines are: ', len(all_lines))
		for inddd, line in enumerate(all_lines):
			for indx, point in enumerate(line):
				if self.state[self.points_inverse[point]] is 'WM':
					p1 += 1
					p2 = 0
					if p1 == 1:
						start_row = indx
						with open('starter_row', 'w') as f:
							f.write(str(start_row) + " " + str(point))
					player1_continous_flag = True; player2_continous_flag = False
					if p1 >= 5 and player1_continous_flag:
						# 5 continous markers -> a row, give high score
						with open('print out row', 'w') as f:
							f.write(str(line) + " " + str(start_row))
						self.moves[2].append((self.points_inverse[line[start_row]], self.points_inverse[line[start_row+4]]))
						for index, p in enumerate(line[start_row: start_row+5]):
							self.state[self.points_inverse[p]] = 'E'

						with open('rings', 'w') as f:
							f.write(str(self.rings))
						x = randint(0, len(self.rings[self.player])-1)
						self.moves[3].append(self.rings[self.player][x])
						self.state[self.rings[self.player][x]] = 'E'
						del self.rings[self.player][x]
						p1_row = 20
						return False
				elif self.state[self.points_inverse[point]] is 'BM':
					p2 += 1
					p1 = 0
					if p2 == 1:
						start_row = indx
					player1_continous_flag = False; player2_continous_flag = True
					if p2 >= 5 and player2_continous_flag:
						# 5 continous markers -> a row, give low score
						self.moves[2].append((self.points_inverse[line[start_row]], self.points_inverse[line[start_row+4]]))
						for index, p in enumerate(line[start_row: start_row+5]):
							self.state[self.points_inverse[p]] = 'E'

						x = randint(0, len(self.rings[self.player])-1)
						self.moves[3].append(self.rings[self.player][x])
						self.state[self.rings[self.player][x]] = 'E'
						del self.rings[self.player][x]

						p2_row = -20
						return False
				else:
					p1 = 0
					p2 = 0
					player1_continous_flag = False; player2_continous_flag = False
		# print('out of loop')
		player1_score = player1_markers + p1_row
		player2_score = player2_markers + p2_row
		# print(player1_score)
		# print(player2_score)

		if self.player:
			score = player1_score - player2_score
		else:
			score = player2_score - player1_score

		self.__utility__ = score
		# print(score)
		# print(self.__utility__)
		return self.__utility__

# if __name__ == '__main__':
	# b = Board()
	# b.normie_f()
	# b.display_board()
	# b.get_neighbours((3,4))
	# b.display_board()
	# print(b.utility)
	# print(b.player)
	# b.display_board()
	# print(len(b.get_neighbours()))
	# for n in b.get_neighbours():
	# 	n.display_board()
	# print(b.utility)
	# b.display_board()
	# b.execute_move([(1,3), (0,0), [], []])	
	# b.display_board()

	# b.execute_move([(3,4), (5,3), [((4,2), (4,0))], [(0,0)]])

	# b.display_board()

def parse_move(move):
	ms = move.split()
	msp = []
	parsed_moves = [None, None, [], []]
	for i in range(int(len(ms)/3)):
		msp.append(ms[i*3:(i+1)*3])

	row = [None, None]
	for index, i in enumerate(msp):
		if i[0] == 'S':
			parsed_moves[0] = (int(i[1]), int(i[2]))
		elif i[0] == 'M':
			parsed_moves[1] = (int(i[1]), int(i[2]))
		elif i[0] == 'RS':
			row[0] = (int(i[1]), int(i[2]))
		elif i[0] == 'RE':
			row[1] = (int(i[1]), int(i[2]))
			if row[0] and row[1]:
				parsed_moves[2].append((row[0], row[1]))
		elif i[0] == 'X':
			parsed_moves[3].append((int(i[1]), int(i[2])))
	return parsed_moves

def parse_move_reverse(move, in_list=False):

	ms = []
	ms.append('S {} {}'.format(move[0][0], move[0][1]))
	ms.append('M {} {}'.format(move[1][0], move[1][1]))
	for i in move[2]:
		ms.append('RS {} {}'.format(i[0][0], i[0][1]))
		ms.append('RE {} {}'.format(i[1][0], i[1][1]))
	for i in move[3]:
		ms.append('X {} {}'.format(i[0], i[1]))

	if not in_list:
		return " ".join(ms)
	else:
		return ms



if __name__ == '__main__':
	# print(parse_move("RS 3 5 RE 3 10 X 5 26 S 3 8 M 4 7"))
	b = Board()
	b.normie_f()
	b.display_board()

# print(parse_move('S 3 2 M 3 7 RS 2 8 RE 2 2 X 3 7'))
# print(parse_move_reverse(parse_move('S 3 2 M 3 7 RS 2 8 RE 2 2 X 3 7')))
# print(parse_move_reverse(parse_move('S 3 2 M 3 7 RS 2 8 RE 2 2 X 3 7'), True))
