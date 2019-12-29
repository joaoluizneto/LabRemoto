import tkinter as tk
from tkinter import ttk #ttk da um estilo pros widgets
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np

def faz_lista_de_linhas(yks,xs):
	lista_de_linhas=[]
	for i in range(len(xs)):
		x=xs[i]
		y=yks[i]
		linha=[x,y]
		lista_de_linhas.append(linha)
	return lista_de_linhas

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


style.use('fivethirtyeight')

arquivo_dados = 'file2.txt'

fig = plt.figure()
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))


def animate(i):
	graph_data = open('file2.txt', 'r').read()
	lines = graph_data.split('\n')
	xs = []
	y1s = []
	y2s = []
	y3s = []
	for line in lines:
		if len(line)>2:
			x,y_all = line.split(',')
			xs.append(float(x))
			y1,y2,y3 = y_all.split('&')
			y1s.append(float(y1))
			y2s.append(float(y2))
			y3s.append(float(y3))

			#area da curva_1
			lista_de_linhas1 = faz_lista_de_linhas(y1s,xs)
			area1 = area_curva(lista_de_linhas1)

			#area da curva_2
			lista_de_linhas2 = faz_lista_de_linhas(y2s,xs)
			area2 = area_curva(lista_de_linhas2)

			#area da curva_3
			lista_de_linhas3 = faz_lista_de_linhas(y3s,xs)
			area3 = area_curva(lista_de_linhas3)
			
			#Volume de agua nos reservatórios
			vol1 = area1 - area2
			vol2 = area2 - area3


	#print("area1: ",area1,"\narea2: ",area2, "\narea3: ",area3)
	
	reservatorios = ['Reservatório 1', 'Reservatório 2']
	volume_reserv = [vol1, vol2]

	ax1.clear()
	ax2.clear()
	
	ax1.plot(xs, y1s)
	ax1.plot(xs, y2s)
	ax1.plot(xs, y3s)
	
	ax2.axhline(y=1000, color='r', linewidth=10, label='Limite de Emergência')
	ax2.bar(reservatorios, volume_reserv)

	ax2.set_ylim([0,1000])	
	ax2.set_ylabel('Litros')
	ax2.legend(['Limite de Emergência'], loc=1)

	#Estilo do gráfico:
	fig.subplots_adjust(left=0.15, bottom=0.1, right=None, top=None, wspace=None, hspace=0.5)
	ax1.legend(['Sensor 1','Sensor 2','Sensor 3'], loc=1)
	ax1.set_xlim([0, 1020])
	ax1.set_ylim([0, 8])
	ax1.set_xlabel('Tempo')
	ax1.set_ylabel('Vazão')
	ax1.set_title('Curva de Vazão - LaDISan')

class app(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		#Coloca o Icone do app
		#logo = tk.PhotoImage(file='pet.png')
		#self.call('wm', 'iconphoto', self._w, logo)

		#Coloca o Título do app
		tk.Tk.wm_title(self, "Aplicativo Generico")


		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#Dicionário de páginas
		self.frames = {}

		#Adiciona as paginas no dicionário para serem usadas pelo show_frame
		for F in (StartPage, PageOne, PageTwo, PageThree):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	#Traz a pagina que foi adicionada no dicionário ao topo
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):					#Essa parte inicia a pagina como um Frame
	def __init__(self, parent, controller):	#
		tk.Frame.__init__(self, parent)		#

		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = tk.Label(self, text="Start Page", font=("Verdana","12"))
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Visit Page 1", command=lambda: controller.show_frame(PageOne))
		button1.pack()

		button2 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(PageTwo))
		button2.pack()

		button3 = ttk.Button(self, text="Visit Page 3", command=lambda: controller.show_frame(PageThree))
		button3.pack()

class PageOne(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Page One", font=("Verdana","12"))
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(PageTwo))
		button2.pack()

		button3 = ttk.Button(self, text="Visit Page 3", command=lambda: controller.show_frame(PageThree))
		button3.pack()

class PageTwo(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Page Two", font=("Verdana","12"))
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = ttk.Button(self, text="Visit Page 1", command=lambda: controller.show_frame(PageOne))
		button2.pack()

		button3 = ttk.Button(self, text="Visit Page 3", command=lambda: controller.show_frame(PageThree))
		button3.pack()

class PageThree(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Page Three", font=("Verdana","12"))
		label.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartPage))
		button1.pack()


		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		
		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		

app = app()
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()

