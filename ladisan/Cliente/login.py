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
import os
import time

#######Parte de dicada para a configuração do gráfico de animação#######
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



arquivo_dados = 'file2.txt'

fig = plt.figure()
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))


def animate(i):
	volume_reserv=[0,0]
	graph_data = open('file2.txt', 'r').read()
	lines = graph_data.split('\n')
	xs = []
	y1s = []
	y2s = []
	y3s = []
	for line in lines:
		if line.count('&')==2:
			x, y_all = line.split(',')
			xs.append(float(x))
			y1, y2, y3 = y_all.split('&')
			y1s.append(float(y1))
			y2s.append(float(y2))
			y3s.append(float(y3))

			# area da curva_1
			lista_de_linhas1 = faz_lista_de_linhas(y1s, xs)
			area1 = area_curva(lista_de_linhas1)

			# area da curva_2
			lista_de_linhas2 = faz_lista_de_linhas(y2s, xs)
			area2 = area_curva(lista_de_linhas2)

			# area da curva_3
			lista_de_linhas3 = faz_lista_de_linhas(y3s, xs)
			area3 = area_curva(lista_de_linhas3)

			# Volume de agua nos reservatórios
			vol1 = area1 - area2
			vol2 = area2 - area3
			volume_reserv = [vol1, vol2]

	# print("area1: ",area1,"\narea2: ",area2, "\narea3: ",area3)

	reservatorios = ['Reservatório 1', 'Reservatório 2']

	ax1.clear()
	ax2.clear()

	ax1.plot(xs, y1s)
	ax1.plot(xs, y2s)
	ax1.plot(xs, y3s)

	ax2.axhline(y=20, color='r', linewidth=10, label='Limite de Emergência')
	ax2.bar(reservatorios, volume_reserv)

	ax2.set_ylim([0, 20])
	ax2.set_ylabel('Litros por reservatório(L)')
	ax2.legend(['Limite de Emergência'], loc=1)

	# Estilo do gráfico:
	fig.subplots_adjust(left=0.15, bottom=0.1, right=None, top=None, wspace=None, hspace=0.5)
	ax1.legend(['Entrada', 'Intermediário', 'Saída'], loc=1)
	ax1.set_xlim([0, 1020])
	ax1.set_ylim([0, 0.134])
	ax1.set_xlabel('Tempo(s)')
	ax1.set_ylabel('Vazão(L/s)')
	ax1.set_title('Curva de Vazão - LaDISan')

############### Parte onde começa a interface gráfica ##################

def apaga_tudo(arquivo):
	with open(arquivo, 'w') as arquivo:
		arquivo.close()

def escreve_login(login, passwd):
	global caminho_arquivo_login
	print(login+','+passwd)
	with open(caminho_arquivo_login, 'w') as arquivo:
		arquivo.write(login+','+passwd)

def ler_log():
	global caminho_arquivo_log
	with open(caminho_arquivo_log, 'r') as arquivo:
		string_log=arquivo.read()
		lista_log=string_log.split('\n')
	for i in range(len(lista_log)):
		if i == len(lista_log)-2:
			if len(lista_log[i]) > 20:
				frase=""
				c=0
				for x in lista_log[i]:
					frase=frase+x
					c+=1
					if c>20:
						frase+='\n'
						c=0
			else: 
				frase=lista_log[i]

			#print("Ultima linha do log: \n", frase)
			return frase	
	

def faz_login(PageOne, controller):
	global login
	global passwd
	global ed1
	global ed2
	login = ed1.get()
	passwd = ed2.get()
	escreve_login(login, passwd)
	os.system("python3 base_cliente_teste.py &")
	controller.show_frame(PageOne)


def altera_label_log():
	texto_log = ler_log()
	label_log.config(text=texto_log)
	label_log.after(200, altera_label_log)
	return texto_log

def inicia_curva():
	pass

def sair():
	exit()

def ajuda():
	pass

caminho_arquivo_login = "login.txt"
caminho_arquivo_log = "log.txt"


class app(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		ttk.Style().configure("TButton", padding=6, relief="flat", background="#000")

		#self.geometry("300x300")

		#Adiciona menubar na aplicação
		menubar = tk.Menu(self, activebackground='#FA8072')
		menubar.add_command(label="Ajuda", command=ajuda)
		menubar.add_command(label="Sair", command=sair)
		self.config(menu=menubar)
		

		#Coloca o Icone do app
		#logo = tk.PhotoImage(file='pet.png')
		#self.call('wm', 'iconphoto', self._w, logo)

		#Coloca o Título do app
		tk.Tk.wm_title(self, "GUI LaDISan")
		
		#Cria o conteiner onde as paginas criadas serão encaixadas
		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#Dicionário de páginas
		self.frames = {}

		#Adiciona as paginas no dicionário para serem usadas pelo show_frame e o tamanho de cada
		for F, geometry in zip((StartPage, PageOne, PageTwo), ('220x150', '220x150', '720x1080')):

			frame = F(container, self)

			self.frames[F] = (frame, geometry)

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	#Traz a pagina que foi adicionada no dicionário ao topo
	def show_frame(self, page_name):
		frame, geometry = self.frames[page_name]
		self.update_idletasks()
		self.geometry(geometry)
		frame.tkraise()

class StartPage(tk.Frame):					#Essa parte inicia a pagina como um Frame
	def __init__(self, parent, controller):	#
		tk.Frame.__init__(self, parent)		#

		apaga_tudo(caminho_arquivo_login)

		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = ttk.Label(self, text="Pagina de Login", font=("Arial", "12"))
		label.grid(row=0, columnspan=2, pady=10)

		label1 = ttk.Label(self, text="Login:")
		label1.grid(row=1, column=0, sticky="w")

		global ed1
		ed1 = tk.Entry(self)
		ed1.grid(row=1, column=1, sticky="w")

		label2 = tk.Label(self, text="Password:")
		label2.grid(row=2, column=0, sticky="w")

		global ed2
		ed2 = tk.Entry(self)
		ed2.grid(row=2, column=1, sticky="w")

		button1 = tk.Button(self, text="OK", highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: faz_login(PageOne, controller))
		button1.grid(row=3, columnspan=2, pady=10)


class PageOne(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		global label_log

		texto = ler_log()

		label_log = tk.Label(self, text=texto, font=("Verdana", "10"))
		label_log.pack(pady=10, padx=10)

		button1 = tk.Button(self, text="Ir para Login", width='20',highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white' ,command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = tk.Button(self, text="Ver gráfico", width='20', highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: controller.show_frame(PageTwo))
		button2.pack()

class PageTwo(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		button1 = tk.Button(self, text="Voltar pro login", width='20', highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = tk.Button(self, text="Começar curva", width='20', highlightbackground='#3E4149', bg='#00FF7F', relief='raised', fg='black', activebackground='#32CD32',activeforeground='white', command=inicia_curva)
		button2.pack()



		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		#canvas.get_tk_widget().grid(row=1, columnspan=2)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		#canvas._tkcanvas.grid(row=2, columnspan=2)

app = app()

texto_log = altera_label_log()

ani = animation.FuncAnimation(fig, animate, interval=1000)

#Centraliza app na tela
app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))

app.mainloop()
