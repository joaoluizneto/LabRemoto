import tkinter as tk
from tkinter import ttk #ttk da um estilo pros widgets
import os
import time


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
	texto = ler_log()
	#print(texto)
	label_log.config(text=texto)
	label_log.after(200, altera_label_log)

caminho_arquivo_login = "login.txt"
caminho_arquivo_log = "log.txt"


class app(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		#self.geometry("300x300")

		#Adiciona menubar na aplicação 
		#menubar = tk.Menu(self)
		#menubar.add_command(label="Ajuda", command=ajuda)
		#menubar.add_command(label="Sair", command=sair)
		#self.config(menu=menubar)
		

		#Coloca o Icone do app
		logo = tk.PhotoImage(file='pet.png')
		self.call('wm', 'iconphoto', self._w, logo)

		#Coloca o Título do app
		tk.Tk.wm_title(self, "Aplicativo Generico")
		
		#Cria o conteiner onde as paginas criadas serão encaixadas
		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#Dicionário de páginas
		self.frames = {}

		#Adiciona as paginas no dicionário para serem usadas pelo show_frame e o tamanho de cada
		for F, geometry in zip((StartPage, PageOne, PageTwo), ('220x150', '220x150', '220x150')):

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
		ed1 = ttk.Entry(self)
		ed1.grid(row=1, column=1, sticky="w")

		label2 = ttk.Label(self, text="Password:")
		label2.grid(row=2, column=0, sticky="w")

		global ed2
		ed2 = ttk.Entry(self)
		ed2.grid(row=2, column=1, sticky="w")

		button1 = ttk.Button(self, text="OK", command=lambda: faz_login(PageOne, controller))
		button1.grid(row=3, columnspan=2, pady=10)


class PageOne(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		global label_log

		texto = ler_log()

		label_log = tk.Label(self, text=texto, font=("Verdana", "10"))
		label_log.pack(pady=10, padx=10)

		button1 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
		button2.pack()

class PageTwo(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)


		button1 = ttk.Button(self, text="Back Home", command=lambda: controller.show_frame(StartPage))
		button1.pack()



app = app()

#Centraliza app na tela
app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))

altera_label_log()

app.mainloop()

