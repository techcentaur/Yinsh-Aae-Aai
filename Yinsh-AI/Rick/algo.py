import gc
import sys
from board import Board

class Algo:
	def __init__(self):
		self.depth = 2

	def print_alp_bet(self, alp, bet):
		print("alpha: ", alp, ":: beta: ", bet)
		return True

	def min_max(self, board):
		depth = 0
		alpha_init = sys.float_info.min
		beta_init = sys.float_info.max
		# self.print_alp_bet(alpha_init, beta_init)

		child_val = self.max_value(board, alpha_init, beta_init, depth)
		# print("child val: ", child_val)

		return True
		gc.collect() # collect garbage here

		try:
			for b in board.get_neighbours():
				if b.utility == child_val:
					return b
		
		except Exception as e:
			print("[*] Value not found in neighbours!")
			raise ValueError

	def is_terminal(self, depth):
		return depth >= self.depth

	def max_value(self, board, alpha, beta, depth):
		if self.is_terminal(depth):
			return board.utility
		
		neighbs = board.get_neighbours()
		for (i, b) in enumerate(neighbs):
			print("--------------------------", i, "-------------------------------")
			# print("[*] ", depth)
			child_value = self.min_value(b, alpha, beta, depth+1)
			# self.print_alp_bet(alpha, beta)
			# print("child val", child_value)

			alpha = max(alpha, child_value)
			# print("alpha-dash", alpha)
			if alpha>=beta:
				return child_value

		max_util =  max([x.utility for x in neighbs])

		# print("max-util", max_util)
		return max_util


	def min_value(self, board, alpha, beta, depth):
		if self.is_terminal(depth):
			return board.utility

		neighbs = board.get_neighbours()
		for (i, b) in enumerate(neighbs):
			print(i)
			# print("[*] ", depth)
			child_value = self.max_value(b, alpha, beta, depth+1)
			# self.print_alp_bet(alpha, beta)
			# print("child val", child_value)
			beta = min(beta, child_value)
			# print("beta-dash", beta)
			if alpha>=beta:
				return child_value

		min_util =  min([x.utility for x in neighbs])

		# print("min-util", min_util)
		return min_util

if __name__ == '__main__':
	b = Board()
	b.normie_f()

	a = Algo().min_max(b)
