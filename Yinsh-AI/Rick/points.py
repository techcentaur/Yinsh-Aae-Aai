from math import cos, sin, pi

K = 1

state = {}

for n in range(6):
	if n==0:
		state[(0, 0)] = (0, 0)
	else:
		for m in range(6):
			y = round(n*K*(cos(m*(pi/3))), 4)
			x = round(n*K*(sin(m*(pi/3))), 4)

			state[(n, m*n)] = (x, y)


for key in [2, 3, 4, 5]:
	for i in range(6):
		(x1, y1) = state[(key, i*key)]
		(x2, y2) = state[(key, (((i+1)*key) % (key*6)))]
		# print(key, " ", i*key)
		# print(key, " ", (((i+1)*key) % (key*6)))

		for t in range(1, key):
			x = round((x1*(key - t) + x2*t) / key, 4)
			y = round((y1*(key - t) + y2*t) / key, 4)

			state[(key, key*i + t)] = (x, y)
			# print(key, " ", key*i + t)

print(state)

for i in [(5,0), (5,5), (5,10), (5,15), (5,20), (5,25)]:
	state.pop(i)

import numpy as np
import matplotlib.pyplot as plt

xli = []
yli = []

for k in state:
	xli.append(state[k][0])
	yli.append(state[k][1])

x = np.array(xli)
y = np.array(yli)

plt.scatter(x, y)
plt.show()