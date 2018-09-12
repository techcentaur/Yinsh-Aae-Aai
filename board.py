class Point:
	def __init__(self, index):
		self.edges = []
		self.index = index



class Board:
	def __init__(self, size=5):
		self.size = size
		self.nodes = dict()

		for i in range(self.size):
			if not i:
				self.nodes[(0, 0)] = Point((0, 0))
			else:
				for j in range(i*6):
					self.nodes[(i, j)] = Point((i, j))
		for i in range(self.size):
			self.nodes.pop((self.size-1, (self.size-1)*i))


board = Board(6)
