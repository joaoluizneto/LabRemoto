import numpy as np
import matplotlib.pyplot as plt

def area_curva(lista_de_linhas):
	area=0
	for i in range(len(lista_de_linhas)):
		x0=lista_de_linhas[i][0]			
		y0=lista_de_linhas[i][1]
		if i!=len(lista_de_linhas)-1:
			x=lista_de_linhas[i+1][0]
			y=lista_de_linhas[i+1][1]
			area+=(x-x0)*(y-y0)/2+(x-x0)*y
	return area


absissa = [x/60 for x in range(16*60)]

def curva_1(x,a):
	if x>=a:
		return 5*np.exp(-(1/3)*(x-a)**2/(2*(2.60)**2))+2
	else:
		return 5*np.exp(-3*(x-a)**2/(2*(2.60)**2))+2

def curva_2(x,a): 
		return 5*np.exp(-(x-a)**2/(2*(2.60)**2))+2


def curva_3(x,a):
	if x<=a:
		return 5*np.exp(-(1/3)*(x-a)**2/(2*(2.60)**2))+2
	else:
		return 5*np.exp(-3*(x-a)**2/(2*(2.60)**2))+2

lista_de_linhas=[]
for i in range(len(absissa)):
	x=absissa[i]
	y=curva_2(x,6)
	linha=[x,y]
	print(linha)
	lista_de_linhas.append(linha)


area=area_curva(lista_de_linhas)

print("area: ", area)


fig = plt.figure()
ax1 = fig.add_subplot(111)


ax1.plot(absissa, [curva_1(x,3) for x in absissa], 'g')
ax1.plot(absissa, [curva_2(x,8) for x in absissa], 'b')
ax1.plot(absissa, [curva_3(x,13) for x in absissa], 'r')

plt.show()



