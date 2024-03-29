import gc
import sys
from board import Board

class Algo:
	def __init__(self):
		self.depth = 1

	def print_alp_bet(self, alp, bet):
		print("alpha: ", alp, ":: beta: ", bet)
		return True

	def min_max(self, board):
		depth = 0
		alpha_init = sys.float_info.min
		beta_init = sys.float_info.max

		child_val, brd = self.max_value(board, alpha_init, beta_init, depth)

		return brd

	def is_terminal(self, depth):
		return depth >= self.depth

	def max_value(self, board, alpha, beta, depth):
		if self.is_terminal(depth):
			return board.eval, board
		
		neighbs = board.get_neighbours()
		for b in neighbs:
			child_value, brd = self.min_value(b, alpha, beta, depth+1)
			
			alpha = max(alpha, child_value)
			if alpha >= beta:
				return child_value, brd

		# if len(neighbs) == 0:
		# 	board.display_board()
		# 	with open('cool bug', 'a') as f:
		# 		f.write(str(board.state) + "\n\n" + str(board.player) + "\n\n" + str(board.reach_neighbs_moves) + "\n\n" + str(board.rings))


		max_eval = [x.eval for x in neighbs]
		max_e =  max(max_eval)

		return max_e, neighbs[max_eval.index(max_e)]


	def min_value(self, board, alpha, beta, depth):
		if self.is_terminal(depth):
			return board.eval, board

		neighbs = board.get_neighbours()

		for b in neighbs:
			child_value, brd = self.max_value(b, alpha, beta, depth+1)

			beta = min(beta, child_value)
			if alpha >= beta:
				return child_value, brd

		min_lss = [x.eval for x in neighbs]
		min_e =  min(min_lss)
		return min_e, neighbs[min_lss.index(min_e)]

		
# if __name__ == '__main__':
# 	b = Board()
# 	# b.state = {(3, 15): 'E', (1, 3): 'WM', (4, 8): 'WM', (3, 0): 'WM', (2, 8): 'E', (5, 13): 'BM', (5, 26): 'E', (4, 22): 'BM', (3, 7): 'E', (2, 5): 'BM', (5, 23): 'WR', (5, 28): 'WR', (5, 8): 'E', (4, 0): 'BM', (4, 19): 'E', (3, 10): 'E', (5, 18): 'E', (4, 13): 'BR', (3, 16): 'WM', (1, 1): 'BM', (4, 10): 'E', (3, 2): 'WM', (2, 6): 'BM', (5, 11): 'WM', (4, 5): 'E', (1, 4): 'BM', (4, 16): 'E', (3, 9): 'E', (2, 3): 'BM', (5, 21): 'WM', (4, 2): 'BM', (5, 3): 'BM', (3, 12): 'E', (5, 16): 'WR', (4, 15): 'E', (3, 1): 'WM', (2, 11): 'BM', (5, 29): 'BR', (5, 14): 'E', (5, 27): 'E', (4, 21): 'WM', (3, 4): 'E', (2, 4): 'BM', (5, 9): 'E', (4, 7): 'E', (5, 6): 'BM', (4, 18): 'BM', (3, 11): 'E', (2, 1): 'WM', (5, 19): 'E', (4, 12): 'E', (5, 1): 'E', (3, 17): 'E', (3, 14): 'BM', (1, 2): 'BM', (4, 9): 'E', (3, 3): 'BM', (2, 9): 'BM', (5, 12): 'BR', (4, 4): 'BM', (1, 5): 'WM', (4, 23): 'E', (3, 6): 'E', (2, 2): 'BM', (5, 22): 'E', (4, 1): 'BM', (5, 4): 'BM', (0, 0): 'BM', (3, 13): 'BM', (5, 17): 'BM', (4, 14): 'BM', (2, 10): 'E', (5, 24): 'E', (1, 0): 'WR', (4, 20): 'WR', (4, 11): 'E', (3, 5): 'E', (2, 7): 'BM', (4, 6): 'E', (5, 7): 'E', (4, 17): 'E', (3, 8): 'BM', (2, 0): 'WM', (4, 3): 'WM', (5, 2): 'BR'}
# 	b.display_board()
# 	a = Algo().min_max(b)
# 	# a.display_board()
# # 	# print(a.reach_neighbs_moves)

# class SecretAlgo:
# 	def __init__(self):
# 		self.counter = 0
# 		self.rings = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]

# 	def algorithm(self, board):
# 		if not self.counter:
# 			for ring in rings:
# 				ring_number = ring[0]
# 				score = 0
# 				for i in range(1, 5):
# 					if board.state[(6, (ring_number*6)+i)] in ['WM', 'BM']:
# 						score = score + 1
# 				if (board.player and board.state[(6, (ring_number*6)+5)] == 'BM') or (not board.player and board.state[(6, (ring_number*6)+5)] == 'WM'):
# 					score = score - 10
# 				for i in range(1, 6):
# 					if (board.player and board.state[(6, (ring_number*6)+i)] == 'BR') or (not board.player and board.state[(6, (ring_number*6)+i)] == 'WR'):
# 						score = score - 10
# 			self.rings = sorted(self.rings, key=lambda k: k[1])

# 		to_play = self.rings[self.counter][0]
# 		self.counter = (self.counter + 1) % 3
# 		ring_location = 0
# 		for i in range(1, 6):
# 			if (board.player and board.state[(6, (to_play*6)+i)] == 'WR') or (not board.player and board.state[(6, (to_play*6)+i)] == 'BR'):
# 				ring_location = i
# 				break

# 		to_flip = []
# 		if ring_location is 5:
# 			algo = Algo()
# 			return algo.min_max(board)

# 		for i in range(1, 6-ring_location):
# 			if board.state[(6, (to_play*6)+i)] == 'E':
# 				new_board = Board(board.player, 6, 5)
# 				new_board.state = board.state.copy()
# 				if to_flip:
# 					for marker in to_flip:
# 						if board.player:
# 							new_board.state[marker] = 'BM'
# 						if not board.player:
# 							new_board.state[marker] = 'WM'
# 				if board.player:
# 					new_board.state[(6, (to_play*6)+ring_location)] = 'BM'
# 					new_board.state[(6, (to_play*6)+i)] = 'BR'
# 				else:
# 					new_board.state[(6, (to_play*6)+ring_location)] = 'WM'
# 					new_board.state[(6, (to_play*6)+i)] = 'WR'

# 				new_board.reach_neighbs_moves += new_board.get_move_string("S", (6,(to_play*6)+ring_location))
# 				new_board.reach_neighbs_moves += self.get_move_string("M", (6,(to_play*6)+i))

# 				return new_board
# 			if board.state[(6, (to_play*6)+i)] == 'WM' and board.player:
# 				to_flip.append((6, (to_play*6)+i))
# 			if board.state[(6, (to_play*6)+i)] == 'BM' and not board.player:
# 				to_flip.append((6, (to_play*6)+i))
		
# 		algo = Algo()
# 		return algo.min_max(board)
# 		