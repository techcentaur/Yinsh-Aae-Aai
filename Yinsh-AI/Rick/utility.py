## Utility Function - Learning and Evaluation
## Make a function
## Change coefficient and evaluate board

def func(board):
	# constant equations of the board
	equations = board.get_equations()

	for eq in equations:
		good_markers, bad_markers = board.get_markers_in_equation(eq)

		# If our player markers >= 5; and last game
		if good_markers >= 5 and bad_markers >= 5 and board.removed_rings == 2:
			# last move
			value += 20
			flag = True
			break
		if good_markers >= 5 and bad_markers >= 5 and board.removed_rings < 2:
			# good move and bad move
			value += 6
		if good_markers >= 5 and bad_markers < 5:
			# very good move
			value += 10
		if bad_markers >=5 and good_markers < 5:
			# very bad move
			value += -10
		if bad_markers < 5 and good_markers < 5:
			value += (bad_markers * -1) + (good_markers * 1)

	if flag:
		return value

	return value