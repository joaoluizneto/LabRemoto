#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk, messagebox #ttk da um estilo pros widgets
import matplotlib, time, subprocess
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('dark_background')



tempo_de_coleta = 0.1
arquivo_dados = 'file2.txt'
caminho_arquivo_login = "login.txt"
caminho_arquivo_log = "log.txt"

#######Parte de dicada para a configuração do gráfico de animação#######
def faz_matriz(yks,xs):
	"""
	Transforma a a lista de coordenadas xs = [1,2,3,4] e y1s = [vazão1, vazão2, ...] em uma matris -> [[x[0],y1[0], x[1],y1[1], ...]
	"""
	matriz=[]
	for i in range(len(xs)):
		x=xs[i]
		y=yks[i]
		coordenadas=[x,y]
		matriz.append(coordenadas)
	return matriz

def area_curva(matriz):
	"""
	Utiliza as coordenadas dispostas em formato de matriz para calcular a área de baixo da curva relacionada à essa matriz
	"""
	area=0
	for i in range(len(matriz)):
		x0=matriz[i][0]
		y0=matriz[i][1]
		if i!=len(matriz)-1:
			x=matriz[i+1][0]
			y=matriz[i+1][1]
			area+=(x-x0)*(y-y0)/2+(x-x0)*y
	return area


fig = plt.figure()
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))

def animate(i):
	"""
	Itera sobre o arquivo de recebimento "file2.txt" para formar os frames da animação
	"""
	volume_reserv=[0,0] #volume inicial dos reservatórios
	with open('file2.txt', 'r') as graph_data:
		graph_data = graph_data.read()

	lines = graph_data.split('\n')

	firstsec = 0
	lastsec = 800

	if len(lines) > 800:
		while len(lines) > 800:
			lines.pop(0)

		firstline = lines[0].split(',')
		firstsec = int(firstline[0])

		lastline = lines[len(lines)-2].split(',')
		lastsec = int(lastline[0])


	xs = []
	y1s = []
	y2s = []
	y3s = []
	for line in lines:
		try:
			x,y_all = line.split(',')
			y1, y2, y3 = y_all.split('&')
		except:
			break
		xs.append(float(x))
		y1s.append(float(y1))
		y2s.append(float(y2))
		y3s.append(float(y3))

		# area da curva_1
		matriz1 = faz_matriz(y1s, xs)
		area1 = area_curva(matriz1)

		# area da curva_2
		matriz2 = faz_matriz(y2s, xs)
		area2 = area_curva(matriz2)

		# area da curva_3
		matriz3 = faz_matriz(y3s, xs)
		area3 = area_curva(matriz3)

		# Volume de agua nos reservatórios
		vol1 = area1 - area2
		vol2 = area2 - area3
		volume_reserv = [vol1, vol2]

	# print("area1: ",area1,"\narea2: ",area2, "\narea3: ",area3)

	reservatorios = ['Reservatório 1', 'Reservatório 2']

	ax1.clear()
	ax2.clear()

	ax1.plot(xs, y1s,color="#65FF2B",lw=1)
	ax1.plot(xs, y2s,color="#FFBC2B",lw=1)
	ax1.plot(xs, y3s,color="#2B85FF",lw=1)

	ax2.axhline(y=20, color='r', linewidth=10, label='Limite de Emergência')
	ax2.bar(reservatorios, volume_reserv)

	ax2.set_ylim([0, 20])
	ax2.set_ylabel('Litros por reservatório(L)')
	ax2.legend(['Limite de Emergência'], loc=1)

	# Estilo do gráfico:
	fig.subplots_adjust(left=0.15, bottom=0.1, right=None, top=None, wspace=None, hspace=0.5)
	ax1.legend(['Entrada', 'Intermediário', 'Saída'], framealpha=0.1, loc=1)
	ax1.set_xlim([firstsec, lastsec])
	ax1.set_ylim([0, 0.134])
	ax1.set_xlabel('Tempo(s)')
	ax1.set_ylabel('Vazão(L/s)')
	ax1.set_title('Curva de Vazão - LaDISan')

############### Parte onde começa a interface gráfica ##################

def apaga_tudo(arquivo):
	"""
	Função para apagar tudo de um arquivo de texto
	"""
	with open(arquivo, 'w') as arquivo:
		arquivo.close()

def escreve_login(login, passwd):
	"""
	Escreve o login no arquivo de login para que este fique disponível para o script base_cliente_teste.py
	"""
	global caminho_arquivo_login
	print(login+','+passwd)
	with open(caminho_arquivo_login, 'w') as arquivo:
		arquivo.write(login+','+passwd)

def ler_log():
	"""
	Lê a ultima linha do arquivo log
	"""
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
	"""
	1- Manda o sistema operacional começar o script base_cliente_teste.py em segundo plano e assim iniciando o processo de login
	2- Alterna para a PageOne que mostra o resultado do login a partir do arquivo de log
	"""
	global login
	global passwd
	global ed1
	global ed2
	global base_cliente
	#Recebe os parametros de login da pagina anterior
	login = ed1.get()
	passwd = ed2.get()
	escreve_login(login, passwd)
	base_cliente = subprocess.Popen(["python3", "base_cliente_teste.py"])
	controller.show_frame(PageOne)

def escreve_log(inform):
	inform=str(inform)
	with open(caminho_arquivo_log, 'a+') as arquivo_log:
		arquivo_log.write(inform+'\n')

def altera_label_log():
	texto_log = ler_log()
	label_log.config(text=texto_log)
	label_log.after(200, altera_label_log)
	return texto_log

def sair():
	escreve_log("Saindo da aplicação...")
	try:
		base_cliente.terminate()
	except NameError:
		pass
	app.destroy()
	exit()

def fecha_base_cliente():
	try:
		base_cliente.terminate()
	except NameError:
		pass

class app(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		ttk.Style().configure("TButton", padding=6, relief="flat", background="#000")

		#self.geometry("300x300")
		apaga_tudo(caminho_arquivo_log)
		escreve_log("Faça o login")

		#Adiciona menubar na aplicação
		menubar = tk.Menu(self, font=("Arial", "9"), background="#4682B4",fg='white', activebackground='#011C56', activeforeground='white', tearoff=1)
		menubar.add_command(label="Login", command=lambda: self.show_frame(StartPage))
		menubar.add_command(label="Status", command=lambda: self.show_frame(PageOne))
		menubar.add_command(label="Gráfico", command=lambda: self.show_frame(PageTwo))
		menubar.add_command(label="Parar Coleta", command=lambda: fecha_base_cliente())
		menubar.add_command(label="Sair", activebackground='red', command=sair)
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
		for F, geometry in zip((PageTwo,PageOne,StartPage),('720x1080','270x150','270x150')):
#								((PageTwo,PageOne,StartPage),('720x1080','220x150','220x150'))
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

		label1 = ttk.Label(self, text="       Login:")
		label1.grid(row=1, column=0, sticky="w")

		global ed1
		ed1 = tk.Entry(self)
		ed1.grid(row=1, column=1, sticky="w")

		label2 = tk.Label(self, text="Password:")
		label2.grid(row=2, column=0, sticky="w")

		global ed2
		ed2 = tk.Entry(self, show="*")
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

		#button1 = tk.Button(self, text="Voltar para o login", height='0.5' ,width='20', highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: controller.show_frame(StartPage))
		#button1.pack()

		#button2 = tk.Button(self, text="Começar curva", width='20', highlightbackground='#3E4149', bg='#00FF7F', relief='raised', fg='black', activebackground='#32CD32',activeforeground='white', command=inicia_curva)
		#button2.pack()

		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		#canvas.get_tk_widget().grid(row=1, columnspan=2)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		#canvas._tkcanvas.grid(row=2, columnspan=2)

def on_closing():
	if messagebox.askokcancel("Sair", "Você deseja sair?"):
		escreve_log("Saindo da aplicação...")
		try:
			base_cliente.terminate()
		except NameError:
			pass
		app.destroy()
		exit()

app = app()

app.protocol("WM_DELETE_WINDOW", on_closing)

texto_log = altera_label_log()

ani = animation.FuncAnimation(fig, animate, interval=tempo_de_coleta*1000, repeat=True)

#Centraliza app na tela
app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))

app.mainloop()
