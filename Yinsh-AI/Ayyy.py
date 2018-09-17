from game import Game
import random
import sys
import time
from Rick import algo, board

class RandomPlayer:

	def __init__(self):
		data = sys.stdin.readline().strip().split() # Initialize Environment
		self.player = int(data[0]) - 1 # player can have values 0 and 1
		self.n = int(data[1]) # n can have values 5, 6, or 7
		self.time_left = int(data[2])
		self.game = Game(self.n)
		self.RingPos = {}
		self.board = board.Board(player=self.player+1)
		self.algo = algo.Algo()
		self.play()

	def placeRing(self):
		movetype = 'P'
		hexagon = random.randint(0,self.n)
		position = random.randint(0,max(0,6*hexagon-1))
		if hexagon==self.n and position%self.n==0:
			position+=1
		return '{type} {hex} {pos}'.format(type=movetype, hex=hexagon, pos=position), len(self.RingPos), hexagon, position

	def selectRing(self):
		movetype = 'S'
		ring_num = random.randint(0,self.n-1)
		while ring_num not in self.RingPos:
			ring_num = random.randint(0,self.n-1)
		ring = self.RingPos[ring_num]
		return '{type} {hex} {pos}'.format(type=movetype, hex=ring[0], pos=ring[1]), ring_num

	def moveRing(self):
		movetype = 'M'
		hexagon = random.randint(0,self.n)
		position = random.randint(0,max(0,6*hexagon-1))
		if hexagon==self.n and position%self.n==0:
			position+=1
		return '{type} {hex} {pos}'.format(type=movetype, hex=hexagon, pos=position), hexagon, position

	def removeRowStart(self):
		movetype = 'RS'
		hexagon = random.randint(0,self.n)
		position = random.randint(0,max(0,6*hexagon-1))
		if hexagon==self.n and position%self.n==0:
			position+=1
		return '{type} {hex} {pos}'.format(type=movetype, hex=hexagon, pos=position)

	def removeRowEnd(self):
		movetype = 'RE'
		hexagon = random.randint(0,self.n)
		position = random.randint(0,max(0,6*hexagon-1))
		if hexagon==self.n and position%self.n==0:
			position+=1
		return '{type} {hex} {pos}'.format(type=movetype, hex=hexagon, pos=position)

	def removeRing(self):
		movetype = 'X'
		ring_num = random.randint(0,self.n-1)
		while ring_num not in self.RingPos:
			ring_num = random.randint(0,self.n-1)
		ring = self.RingPos[ring_num]
		return '{type} {hex} {pos}'.format(type=movetype, hex=ring[0], pos=ring[1]), ring_num

	def play_move_seq(self, move_seq):
		moves = ' '.join(move_seq) + '\n'
		sys.stdout.write(moves)
		sys.stdout.flush()

	def play(self):
		if self.player == 1:
			move = sys.stdin.readline().strip()
			self.game.execute_move(move)
			move_split = move.split()
			if move_split[0] == 'P':
				if self.player:
					self.board.state[(int(move_split[1]),int(move_split[2]))] = 'BR'
				else:
					self.board.state[(int(move_split[1]),int(move_split[2]))] = 'WR'
				self.board.rings[self.player].append((int(move_split[1]),int(move_split[2])))

		while True: # Keep playing moves till game is over
			move_seq = []

			while True: # Loop till valid move sequence is found
				state = self.game.check_player_state()
				if state == 0: ## Place Rings
					moveP, i, hex, pos = self.placeRing()
					success = self.game.execute_move(moveP)
					if success != 0:
						self.RingPos[i] = (hex, pos)
						self.board.rings[self.player].append((hex, pos))
						if self.player == 1:
							self.board.state[(hex, pos)] = 'BR'
						else:
							self.board.state[(hex, pos)] = 'WR'
						move_seq.append(moveP)
						break
				elif state == 1: ## Select a Ring and the Move to Valid Postion
					brd = self.algo.min_max(self.board)

					# moveS, i = self.selectRing()
					# moveM, hex, pos = self.moveRing()
					move_s = board.parse_move_reverse(brd.moves, True)
					self.board = brd
					self.game.execute_move(move_s[0])
					state = self.game.check_player_state()
					success = self.game.execute_move(move_s[1])
					if success != 0:
						for key, val in self.RingPos.items():
							if val == brd.moves[0]:
								val = brd.moves[1]

						state = self.game.check_player_state()
						move_seq.append(move_s[0]); move_seq.append(move_s[1])
						if state != 3:
							break

				elif state == 2:
					raise AssertionError("The player state cannot be 2 after a sequence of valid moves")
				elif state == 3 or state == 6: ## Select Row to Remove (State 6 if other players your row)
					# move_start = self.removeRowStart()
					if state == 6:
						move_s = board.parse_move_reverse(self.board.moves, True)

					for rows_to_remove in range(0, len(move_s)-4, 3):
						success = self.game.execute_move(move_s[2+rows_to_remove])
						if success != 0:
							while True:
								# move_end = self.removeRowEnd()
								success = self.game.execute_move(move_s[3+rows_to_remove])
								if success != 0:
									break
							state = self.game.check_player_state()
							move_seq.append(move_start); move_seq.append(move_end);
							if state == 4 or state == 7:
								move = move_s[4+rows_to_remove]

								for k, v in self.RingPos.items():
									if v == brd.moves[3][rows_to_remove]:
										del self.RingPos[k]

										break

								self.game.execute_move(move)
								move_seq.append(move)

								state = self.game.check_player_state()
						break  #removed all rows and now, chance for next player
				
				# elif state == 4 or state == 7: ## Select Ring to Remove (State 7 if other players your row)
				# 	# move, i = self.removeRing()
				# 	move = move_s[4+rows_to_remove]
				# 	# del self.RingPos[i]
				# 	for k, v in self.RingPos.items():
				# 		if v == brd.moves[3][rows_to_remove]:
				# 			del self.RingPos[k]
				# 			break

				# 	self.game.execute_move(move)
				# 	move_seq.append(move)
				# 	if state == 7:
				# 		continue
				# 	state = self.game.check_player_state()
				# 	# if state != 3:
				# 	# 	break

			self.play_move_seq(move_seq)
			
			## Execute Other Player Move Sequence
			move = sys.stdin.readline().strip()
			self.game.execute_move(move)
			move_split = move.split()
			if move_split[0] == 'P':
				if self.player:
					self.board.state[(int(move_split[1]),int(move_split[2]))] = 'BR'
				else:
					self.board.state[(int(move_split[1]),int(move_split[2]))] = 'WR'
				self.board.rings[self.player].append((int(move_split[1]),int(move_split[2])))
			else:
				move_parsed = board.parse_move(move)
				self.board.execute_move(move_parsed)

random_player = RandomPlayer()
