from math import cos, sin, pi
import numpy as np
# import matplotlib.pyplot as plt
from random import randint
import copy



def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return float('{0:.{1}f}'.format(f, n))
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))


class Board:
	def __init__(self, player, size, row_length):
		self.player = player - 1
		# player 1 is white -> 0, player 2 is black -> 1
		# E - Empty; BR; WR; BM; WM
		self.size = size
		self.row_length = row_length
		self.init_board_config()

		self.rings = {1: [], 0: []}
		self.state = {}
		for k in self.points:
			self.state[k] = 'E'

		self.reach_neighbs_moves = ""
		self.__utility__ = None
		self.__eval__ = None

	def init_board_config(self):
		K = 1
		ROUND = 3
		TRUNC = 4

		self.points = {}

		for n in range(self.size+1):
			if not n:
				self.points[(0, 0)] = (0, 0)
			else:
				for m in range(6):
					y = round(truncate(n*K*(cos(m*(pi/3))), TRUNC), ROUND)
					x = round(truncate(n*K*(sin(m*(pi/3))), TRUNC), ROUND)
					self.points[(n, m*n)] = (x, y)

		for key in range(2, self.size+1):
			for i in range(6):
				(x1, y1) = self.points[(key, i*key)]
				(x2, y2) = self.points[(key, (((i+1)*key) % (key*6)))]

				for t in range(1, key):
					x = (x1*(key - t) + x2*t) / key
					y = (y1*(key - t) + y2*t) / key

					y = round(truncate(y, TRUNC), ROUND)
					x = round(truncate(x, TRUNC), ROUND)
					self.points[(key, key*i + t)] = (x, y)

		for i in [(self.size, i*(self.size)) for i in range(6)]:
			self.points.pop(i)

		self.points_inverse = {v:k for k,v in self.points.items()}


	def lines(self, point):
		K = 1
		ROUND = 3
		TRUNC = 4
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
		K = 1
		ROUND = 3
		TRUNC = 4
		lines = []
		for i in range(3):
			angles = ((pi/2)-(i*(pi/3)), (pi/2)-((i+1)*(pi/3)))
			for j in range(self.size):
				if not j:
					# print(self.points)
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

	def get_move_string(self, _type, point):
		return "{} {} {} ".format(_type, point[0], point[1])

	def get_move_list(self, _move_string):
		_move_split = _move_string.split()
		_move_triple_list = []
		for i in range(0, len(_move_split), 3):
			_move_triple_list += [" ".join(_move_split[i: i+3])]

		return _move_triple_list

	def get_neighbours(self):
		# f = open('neigbhs', 'a')
		neighbour_boards = []

		for ring in self.rings[self.player]:
			# f.write(str("----------ring --------") + str(ring) + "\n")
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
			
			for key in points_in_lines:
				for point1 in points_to_go[key]:
					flip_markers = []
					for point2 in points_in_lines[key]:
						if point1 == point2:
							# f.write(str("Do ") + str(ring) + " " + str(self.points_inverse[point2]) + " " + str(flip_markers) + "\n") 
							neighbour_boards.append(self.make_board(ring, self.points_inverse[point2], flip_markers))
						else:
							if self.state[self.points_inverse[point2]] is 'E':
								pass
							else:
								flip_markers.append(self.points_inverse[point2])

		# f.close()
		return neighbour_boards

	def make_board(self, point_at_ring, point_to_go, flip_markers):
		new_board = Board(player = (1 + (1 - self.player)), size=self.size, row_length=self.row_length)
		# f.write(str(self.player)+ " it neighs player " +  str(new_board.player) + "\n")
		
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

		new_board.rings = copy.deepcopy(self.rings)
		# f.write("[] New board rings: " + str(new_board.rings) + "\n")
		
		new_board.rings[self.player].remove(point_at_ring)
		new_board.rings[self.player].append(point_to_go)
		# f.write("[] New board rings change: " + str(new_board.rings) + "\n")


		new_board.reach_neighbs_moves += self.get_move_string("S", point_at_ring)
		new_board.reach_neighbs_moves += self.get_move_string("M", point_to_go)

		# f.write("String : "+ str(new_board.reach_neighbs_moves) + "\n")

		# Now check if the newly made board has rows made up in them
		total_lines = self.all_lines()

		start_index1 = 0; start_index2 = 0
		end_index1 = 0; end_index2 = 0

		count1 = 0; count2 = 0
		for each_line in total_lines:
			count1 = 0; count2 = 0; start_index1 = 0; start_index2 = 0; end_index1 = 0; end_index2 = 0
			for each_point in each_line:
				if new_board.state[self.points_inverse[each_point]] is 'WM':
					count1 += 1
					count2 = 0
					if count1 == 1:
						start_index1 = each_line.index(each_point)
					if count1 == self.row_length:
						# f.write("WM board state of row: " + str(new_board.state) + "with line" + str(each_line) + "\n")
						# f.write("[]Removal: Start WM[] \n")
						# f.write("Rings:: " + str(new_board.rings) + "\n")
						# f.write("State:: " + str(new_board.state) + "\n")

						string_move = self.get_move_string("RS", self.points_inverse[each_line[start_index1]])
						new_board.reach_neighbs_moves += string_move

						end_index1 = each_line.index(each_point)
						string_move = self.get_move_string("RE", self.points_inverse[each_line[end_index1]])
						new_board.reach_neighbs_moves += string_move
						
						# f.write("WM remove 5 rings as " + str(new_board.reach_neighbs_moves) + "\n")

						for ep in each_line[start_index1: end_index1+1]:
							new_board.state[self.points_inverse[ep]] = 'E'

						string_move = self.get_move_string("X", new_board.rings[0][0])
						new_board.reach_neighbs_moves += string_move

						new_board.state[new_board.rings[0][0]] = 'E'
						new_board.rings[0].remove(new_board.rings[0][0])

						# f.write("WM new state board: " + str(new_board.state) + "\n")
						# f.write("[*] Did: " + str(new_board.reach_neighbs_moves))
						# f.write("[]Removal: End WM[] \n")
						# f.write("Rings:: " + str(new_board.rings) + "\n")
						# f.write("State:: " + str(new_board.state) + "\n")

						count1 = 0
						break
				
				elif new_board.state[self.points_inverse[each_point]] is 'BM':
					count2 += 1
					count1 = 0
					if count2 == 1:
						start_index2 = each_line.index(each_point)
					if count2 == self.row_length:
						# f.write("BM board state of row: " + str(new_board.state) + "with line" + str(each_line) + "\n")
						# f.write("[]Removal: Start BM[] \n")
						# f.write("Rings:: " + str(new_board.rings) + "\n")
						# f.write("State:: " + str(new_board.state) + "\n")

						try:
							string_move = self.get_move_string("RS", self.points_inverse[each_line[start_index2]])
						except IndexError:
							break

						new_board.reach_neighbs_moves += string_move

						end_index2 = each_line.index(each_point)
						string_move = self.get_move_string("RE", self.points_inverse[each_line[end_index2]])
						new_board.reach_neighbs_moves += string_move

						# f.write("BM remove 5 rings as " + str(new_board.reach_neighbs_moves) + "\n")

						for ep in each_line[start_index2: end_index2+1]:
							new_board.state[self.points_inverse[ep]] = 'E'

						string_move = self.get_move_string("X", new_board.rings[1][0])
						new_board.reach_neighbs_moves += string_move
						
						new_board.state[new_board.rings[1][0]] = 'E'
						new_board.rings[1].remove(new_board.rings[1][0])

						# f.write("BM new state board: " + str(new_board.state) + "\n")
						# f.write("[]Removal: End BM[] \n")
						# f.write("Rings:: " + str(new_board.rings) + "\n")
						# f.write("State:: " + str(new_board.state) + "\n")


						count2 = 0
						break

				else:
					count1 = 0
					count2 = 0

		return new_board

	@property
	def eval(self):
		if self.__eval__ is not None:
			return self.__eval__
		else:
			return self.__eval_it__()

	def __eval_it__(self):
		total_lines = self.all_lines()
		p1_mark = 0; p2_mark = 0

		leng = len(total_lines)
		indexes = [-2, -5]
		for i in range(2*(self.size)-1):
			indexes.append(-(self.size+i+1))

		# if self.size==5:
		# 	vertical_lines = [18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 31]
		# else:
		vertical_lines = [x+leng for x in indexes]

		for verti in vertical_lines:
			for coord in total_lines[verti]:
				mark = self.state[self.points_inverse[coord]]
				if mark is 'WM':
					p1_mark += 1
				elif mark is 'BM':
					p2_mark += 1

		p1 = 0; p1_row = 0
		p2 = 0; p2_row = 0

		_amount = 2

		for each_line in total_lines:
			for each_point in each_line:
				if self.state[self.points_inverse[each_point]] is 'WM':
					p1 = p1 + 1
					p2_row = p2_row + _amount*(p2+p2)
					p2 = 0
				elif self.state[self.points_inverse[each_point]] is 'BM':
					p2 = p2 + 1
					p1_row = p1_row + _amount*(p1+p1)
					p1 = 0
				else:
					p1_row = p1_row + (p1+p1)
					p2_row = p2_row + (p2+p2)
					p1 = 0
					p2 = 0

		player1_score = _amount*2*p1_mark + p1_row + 100*(self.size-len(self.rings[0]))
		player2_score = _amount*2*p2_mark + p2_row + 100*(self.size-len(self.rings[1]))

		if self.player:
			score = player1_score - player2_score
		else:
			score = player2_score - player1_score

		self.__eval__ = score
		# print(score)
		return score



	def execute_move(self, todo_moves_string):
		todo_move_list = self.get_move_list(todo_moves_string)

		for todo_index in range(0, len(todo_move_list)):
			if todo_move_list[todo_index].startswith("S"):
				_S = todo_move_list[todo_index].split()
				_M = todo_move_list[todo_index + 1].split()

				select_ring = (int(_S[1]), int(_S[2]))
				move_ring = (int(_M[1]), int(_M[2]))
				
				directed_lines = self.lines(select_ring)
				
				for direction, each_line in directed_lines.items():
					if self.points[move_ring] in each_line:
						end_index = each_line.index(self.points[move_ring])
						for p in each_line[:end_index]:
							if self.state[self.points_inverse[p]] is 'BM':
								self.state[self.points_inverse[p]] = 'WM'
							elif self.state[self.points_inverse[p]] is 'WM':
								self.state[self.points_inverse[p]] = 'BM'
						break
				if self.player:
					his_mark = 'WR'
				else:
					his_mark = 'BR'

				if self.state[select_ring]  == his_mark:
					self.state[select_ring] = 'WM'
				
				self.state[move_ring] = 'WR'
				
				self.rings[int(not bool(self.player))].remove(select_ring)
				self.rings[int(not bool(self.player))].append(move_ring)

			elif todo_move_list[todo_index].startswith("RS"):
				_RS = todo_move_list[todo_index].split()
				_RE = todo_move_list[todo_index+1].split()
				_X = todo_move_list[todo_index+2].split()

				ring_start = (int(_RS[1]), int(_RS[2]))
				ring_end = (int(_RE[1]), int(_RE[2]))
				ring_remove = (int(_X[1]), int(_X[2]))

				directed_lines = self.lines(ring_start)
				for direction, each_line in directed_lines.items():
					each_line = [self.points[ring_start]] + each_line
					if self.points[ring_end] in each_line:
						end_index = each_line.index(self.points[ring_end])
						for p in each_line[0: end_index+1]:
							self.state[self.points_inverse[p]] = 'E'
						break
				# with open('shitt', 'a') as f:
					# f.write(str(self.rings) + " " + str(self.player) + "\n\n")

				self.rings[int(not bool(self.player))].remove(ring_remove)

				# with open('shitt', 'a') as f:
					# f.write(str(self.rings) + " " + str(self.player) + "\n\n")


	def state_six(self):
		total_lines = self.all_lines()	
		state_six_execution = ""
		
		if self.player:
			my_mark = 'BM'
			my_dash = 1
		else:
			my_mark = 'WM'
			my_dash = 0

		start_index1 = 0; start_index2 = 0
		end_index1 = 0; end_index2 = 0

		count1 = 0; count2 = 0
		for each_line in total_lines:
			for each_point in each_line:
				if self.state[self.points_inverse[each_point]] == my_mark:
					count1 += 1
					count2 = 0
					if count1 == 1:
						start_index1 = each_line.index(each_point)
					if count1 == self.row_length:
						# f = open('last', 'a')
						string_move = self.get_move_string("RS", self.points_inverse[each_line[start_index1]])
						state_six_execution += string_move

						end_index1 = each_line.index(each_point)
						string_move = self.get_move_string("RE", self.points_inverse[each_line[end_index1]])
						state_six_execution += string_move
						
						for ep in each_line[start_index1: end_index1+1]:
							self.state[self.points_inverse[ep]] = 'E'

						# f.write("rings before" + str(self.rings) + "\n\n")
						string_move = self.get_move_string("X", self.rings[my_dash][0])
						state_six_execution += string_move
						self.state[self.rings[my_dash][0]] = 'E'
						self.rings[my_dash].remove(self.rings[my_dash][0])
						# f.write("rings after" + str(self.rings) + "\n\n")
						# f.write("Sham!" + str(self.reach_neighbs_moves) + "\n\n\n")

						# f.close()
						count1 = 0
						break

				else:
					start_index1 = 0; start_index2 = 0
					end_index1 = 0; end_index2 = 0
					count1 = 0; count2 = 0

			if len(self.rings[my_dash]) <= 2:
				break

		return state_six_execution


	def get_rings(self):
		rings = {1:[], 0:[]}
		for key, val in self.state.items():
			if val is 'WR':
				rings[0].append(key)
			elif val is 'BR':
				rings[1].append(key)

		return rings


	def coolfunc(self):
		self.state[(0,0)] = 'WM'
		self.state[(2,0)] = 'WM'
		self.state[(1,3)] = 'WM'
		self.state[(2,6)] = 'WM'
		self.state[(1,5)] = 'WM'
		self.state[(2,9)] = 'WM'
		self.state[(3,13)] = 'WM'
		self.state[(4,17)] = 'WM'
		self.state[(1,0)] = 'WR'
		self.state[(4,3)] = 'WR'
		self.state[(5,1)] = 'WR'
		self.state[(5,2)] = 'BR'
		self.state[(5,3)] = 'BR'
		self.state[(5,4)] = 'BR'
		self.rings = {0: [(1,0), (4,3), (5,1)], 1: [(5,2), (5,3), (5,4)]}
		self.player = 0

# if __name__ == '__main__':
# 	b = Board()
# 	b.coolfunc()
# 	b.display_board()
# 	nbs = b.get_neighbours()

# 	print("rings: " + str(b.rings))
# 	print("rings func: "+ str(b.get_rings()))
# 	print("length neigh" + str(len(nbs)))
# 	for nei in nbs:
# 		print("eval" + str(nei.eval))
# 		print("how to" + nei.reach_neighbs_moves)
# 		print("rings: " + str(nei.rings))
# 		print("rings func: "+ str(nei.get_rings()))
# 		print(nei.display_board())

if __name__=="__main__":
	b = Board(0, 6, 5)
	# li = b.all_lines()
	# leng = len(li)
	# indexes = [-2, -5] 
	# for i in range(2*(6)-1):
	# 	indexes.append(-(6+i+1))
	# for i in indexes:
	# 	b.display_points(li[i])
