
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib import style

style.use('fivethirtyeight')

arquivo_dados = 'file2.txt'

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
	graph_data = open('file2.txt', 'r').read()
	lines = graph_data.split('\n')
	xs = []
	ys = []
	for line in lines:
		if len(line)>2:
			x,y = line.split(',')
			xs.append(float(x))
			ys.append(float(y))

	ax1.clear()
	ax1.plot(xs, ys)

	plt.xlim(0, 960)
	plt.ylim(0, 8)
	plt.xlabel('Tempo')
	plt.ylabel('Vazão')
	plt.title('Curva de Vazão - LaDISan')

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
