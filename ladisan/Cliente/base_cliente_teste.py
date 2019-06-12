

from socket import *


def cria_cliente(ip, porta):
	"""
	Criamos o socket e o conectamos ao servidor 
	"""	
	ip = str(ip)
	global sockobj
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.connect((ip, porta))
	

cria_cliente('127.0.0.1', 50007)

while True:

	#requisita = ''.encode()	
	#sockobj.send(requisita)
	
	#Depois de mandar uma mensagem esperamos uma resposta do servidor 
	data = sockobj.recv(1024)
	texto = data.decode("utf-8")

	print(texto.split('\n'))
	
	arquivo = open('file2.txt', 'w')
	arquivo.write(texto)
	arquivo.close()
