import gc
import sys
from board import Board

class Algo:
	def __init__(self):
		pass

	def print_alp_bet(self, alp, bet):
		print("alpha: ", alp, ":: beta: ", beta)
		return True

	def min_max(self, board):
		self.depth = 0
		alpha_init = sys.float_info.min
		beta_init = sys.float_info.max
		self.print_alp_bet(alpha_init, beta_init)

		child_val = self.max_value(board, alpha_init, beta_init)
		gc.collect() # collect garbage here

		try:
			for b in board.get_neighbours():
				if b.utility == child_val:
					return b
		
		except Exception as e:
			print("[*] Value not found in neighbours!")
			raise ValueError

	@property
	def is_terminal(self):
		return self.depth >= 4


	def max_value(self, board, alpha, beta):
		if self.terminal_test:
			return board.utility
		
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

if __name__ == '__main__':
	b = Board()
	b.normie_f()

	a = Algo().min_max(b)
