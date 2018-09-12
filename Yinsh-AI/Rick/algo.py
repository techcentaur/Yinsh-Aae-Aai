import sys
	
class Algo:
	def __init__(self):
		pass

	def min_max(board):
		alpha_init = sys.float_info.min
		beta_init = sys.float_info.max
		value = max_value(board, alpha_init, beta_init)
		for state in board.get_neighbours():
			if utility_function(state) == value:
				return state

		return {'Error': 'Hypothetical State'}

	def max_value(board, alpha, beta):
		if terminal_test(board):
			return utility_function(board)
		
		for state in board.get_neighbours():
			child_value = self.min_value(board, alpha, beta)
			alpha = min(alpha, child_value)
			if alpha>=beta:
				return child_value

		return alpha

	def min_value(board, alpha, beta):
		if terminal_test(board):
			return utility_function(board)

		for state in board.get_neighbours():
			child_value = self.max_value(board, alpha, beta)
			beta = min(beta, child_value)
			if alpha>=beta:
				return child_value

		return beta
