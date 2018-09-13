import sys
from utility import func

class Algo:
	def __init__(self):
		pass

	def min_max(self, board):
		alpha_init = sys.float_info.min
		beta_init = sys.float_info.max
		
		self.depth = 0

		child_board = self.max_value(board, alpha_init, beta_init)
		
		return child_board

	def terminal_test(self):
		return self.depth >= 6

	def max_value(self, board, alpha, beta):
		if self.terminal_test():
			return utility.func(board)
		
		self.depth += 1
		for b in board.get_neighbours():
			child_value = self.min_value(b, alpha, beta)
			alpha = min(alpha, child_value)

			if alpha>=beta:
				return child_value

		# alpha is wrong -- will return some child
		return alpha--

	def min_value(self, board, alpha, beta):
		if self.terminal_test():
			return utility.func(board)

		self.depth += 1
		for b in board.get_neighbours():
			child_value = self.max_value(b, alpha, beta)
			beta = min(beta, child_value)

			if alpha>=beta:
				return child_value

		# beta is wrong -- will return some child
		return beta
