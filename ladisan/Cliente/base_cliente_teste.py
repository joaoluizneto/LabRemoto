from socket import *
import json

def cria_cliente(ip, porta):
	"""
	Criamos o socket e o conectamos ao servidor
	"""
	ip = str(ip)
	global sockobj
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.connect((ip, porta))

try:
	cria_cliente('127.0.0.1', 50007)
	print(" Conexão socket com o RaspberryPi estabelecida! ")
	while True:

		#requisita = ''.encode()
		#sockobj.send(requisita)

		#Depois de mandar uma mensagem esperamos uma resposta do servidor
		data = sockobj.recv(1000000)
		json_da_lista = data.decode("utf-8")
		lista_de_linhas = json.loads(json_da_lista)
		linhas = '\n'.join(lista_de_linhas)
		arquivo = open('file2.txt', 'w')
		arquivo.writelines(linhas)
		arquivo.close()
except:
	print("Um erro de conexão ocorreu! \n -Servidor desligado \n ou -Endereço IP e porta incorretos ")
