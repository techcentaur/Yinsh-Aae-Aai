from game import Game
import random
import sys
import time
from Rick import algo, board

import signal


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
                    self.board.state[(int(move_split[1]),int(move_split[2]))] = 'WR'
                else:
                    self.board.state[(int(move_split[1]),int(move_split[2]))] = 'BR'
                self.board.rings[int(not bool(self.player))].append((int(move_split[1]),int(move_split[2])))

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
                    brd.player = self.board.player
                    self.board = brd
                    
                    reach_here_string = self.board.reach_neighbs_moves
                    reach_here_list = self.board.get_move_list(reach_here_string)

                    self.game.execute_move(reach_here_list[0])
                    state = self.game.check_player_state()
                    success = self.game.execute_move(reach_here_list[1])

                    state = self.game.check_player_state()
                    move_seq.append(reach_here_list[0]); move_seq.append(reach_here_list[1])

                    if state != 3:
                        break

                elif state == 2:
                    raise AssertionError("The player state cannot be 2 after a sequence of valid moves")

                elif state == 3: ## Select Row to Remove (State 6 if other players your row)
                    reach_here_string = self.board.reach_neighbs_moves
                    reach_here_list = self.board.get_move_list(reach_here_string)

                    first_counter = 0
                    success = self.game.execute_move(reach_here_list[2+first_counter])                  
                    success = self.game.execute_move(reach_here_list[3+first_counter])
                    state = self.game.check_player_state()
                    move_seq.append(reach_here_list[2+first_counter]); move_seq.append(reach_here_list[3+first_counter]);

                elif state == 4:
                    self.game.execute_move(reach_here_list[4+first_counter])
                    move_seq.append(reach_here_list[4+first_counter])

                    state = self.game.check_player_state()
                    if state != 3:
                        first_counter = 0
                        break
                    if state == 3:
                        first_counter += 3
   
                elif state == 6: ## Select Row to Remove (State 6 if other players your row)
                    execute_move_list = self.board.get_move_list(self.board.state_six())

                    second_counter = 0
                    success = self.game.execute_move(execute_move_list[second_counter])                  
                    success = self.game.execute_move(execute_move_list[1+second_counter])

                    state = self.game.check_player_state()
                    move_seq.append(execute_move_list[second_counter]); move_seq.append(execute_move_list[1+second_counter]);
                elif state == 7:
                    move = execute_move_list[2+second_counter]
                    self.game.execute_move(move)
                    move_seq.append(execute_move_list[2+second_counter])
                    state = self.game.check_player_state()
                    
                    if state == 6:
                        second_counter += 3
                    else:
                        second_counter = 0

            self.play_move_seq(move_seq)
            
            ## Execute Other Player Move Sequence
            move = sys.stdin.readline().strip()
            self.game.execute_move(move)
            state = self.game.check_player_state()
    
            move_split = move.split()
            if move_split[0] == 'P':
                if self.player:
                    self.board.state[(int(move_split[1]),int(move_split[2]))] = 'WR'
                else:
                    self.board.state[(int(move_split[1]),int(move_split[2]))] = 'BR'
                self.board.rings[int(not bool(self.player))].append((int(move_split[1]),int(move_split[2])))
            else:
                self.board.execute_move(move)

random_player = RandomPlayer()
