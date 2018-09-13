import gc
import sys
from utility import func

class Algo:
	def __init__(self):
		pass

	def min_max(self, board):
		self.depth = 0
		alpha_init = sys.float_info.min
		beta_init = sys.float_info.max
	
		child_val = self.max_value(board, alpha_init, beta_init)
		gc.collect() # collect garbage here

		try:
			for b in board.get_neighbours():
				if utility.func(b) == child_val:
					return b
		
		except Exception as e:
			print("[*] Value not found in neighbours!")
			raise ValueError


	def terminal_test(self):
		return self.depth >= 6

	def max_value(self, board, alpha, beta):
		if self.terminal_test():
			return utility.func(board)
		
		self.depth += 1

		neighbs = board.get_neighbours()
		for b in neighbs:
			child_value = self.min_value(b, alpha, beta)
			alpha = min(alpha, child_value)

			if alpha>=beta:
				return child_value

		max_util =  max([utility.func(x) for x in neighbs])

		return max_util

	def min_value(self, board, alpha, beta):
		if self.terminal_test():
			return utility.func(board)

		self.depth += 1

		neighbs = board.get_neighbours()
		for b in neighbs:
			child_value = self.max_value(b, alpha, beta)
			beta = min(beta, child_value)

			if alpha>=beta:
				return child_value

		min_util =  min([utility.func(x) for x in neighbs])

		return min_util
