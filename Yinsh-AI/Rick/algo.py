import sys
from utility import func

class Algo:
	def __init__(self):
		pass

	def min_max(self, board):
		alpha_init = sys.float_info.min
		beta_init = sys.float_info.max
		
		value = self.max_value(board, alpha_init, beta_init)
		
		# return the action ofwhose state value has been selected
		for state in board.get_neighbours():
			if utility.func(state) == value:
				return state

		return False

	def max_value(self, board, alpha, beta):
		if terminal_test(board):
			return utility.func(board)
		
		for state in board.get_neighbours():
			child_value = self.min_value(board, alpha, beta)
			alpha = min(alpha, child_value)
			if alpha>=beta:
				return child_value

		return alpha

	def min_value(self, board, alpha, beta):
		if terminal_test(board):
			return utility.func(board)

		for state in board.get_neighbours():
			child_value = self.max_value(board, alpha, beta)
			beta = min(beta, child_value)
			if alpha>=beta:
				return child_value

		return beta
