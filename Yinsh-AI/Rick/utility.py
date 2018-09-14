## Utility Function: How to change - Learning and Evaluation
## Make a function
## Change coefficient and evaluate board

# Utility func - How it should be? 
# Change in number of markers in general
# Change in number of markers in a particular line 
# Cluttering? -- No

# Relative: difference between configs of board and its parent
# Not relative: values based on the config of the board

def function(board, parent_board=None, relative=False):
	if not relative:
		