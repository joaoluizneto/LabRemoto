#Server TCP/IP

from socket import *
import time
import json


def cria_servidor(ip, porta, num_clientes):

	""" 
	Use porta = 50007
	Use ip = localhost

	Cria um objeto socket. As duas constantes referem-se a:
	família do endereço (padrão é socket.AF_INET)
	Se é stream(socket.SOCK_STREAM, o padrão) ou datagram(socket.SOCK_DATAGRAM)
	E o protocolo (padrão é 0)
	Significado:
	AF_INET == Protocolo de endereço IP
	SOCK_STREAM == Protocolo de transferência TCP
	Combinação = Server TCP/IP
	"""
	ip = str(ip)
	global sockobj
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.bind((ip, porta))
	#O socket começa a esperar por clientes limitando a 5 conexões por vez
	sockobj.listen(num_clientes)
	print("Servidor iniciado em ",ip, " na porta ",porta, ", esperando por no máximo ", num_clientes, " clientes")

def recebe_cliente():

	"""
	Aceita uma conexão quando encontrada e devolve a um novo socket conexão e o endereço do cliente conectado
	"""
	global conexão, endereço
	conexão, endereço = sockobj.accept()
	print('Server conectado por ', endereço)

def pega_dados(arquivo):
	arquivo = str(arquivo)
	data = open(arquivo, 'r')
	texto = data.read()
	lista_de_linhas = texto.split('\n')
	tamanho = len(lista_de_linhas)
	for linha in lista_de_linhas:
		if tamanho >= 2:
			if linha != '':
				ultima_linha = str(linha) 
		else:
			ultima_linha = "NONE"

	data.close()
	return tamanho, lista_de_linhas, ultima_linha

def delta_tempo():
	global tempo_inicial
	return time.time() - tempo_inicial


	
tempo_inicial = time.time()
cria_servidor('localhost', 50007, 5)
tamanho1, lista_de_linhas1, ultima_linha1 = pega_dados('file1.txt')

while True:
	# Aceita uma conexão quando encontrada e devolve a um novo socket conexão e o endereço do cliente conectado
	
	recebe_cliente() #fica esperando o cliente aparecer

	# Recebe dados enviados pelo cliente
	#data = conexão.recv(1024)
	#perfil_de_curva = data.decode("utf-8")
	
	#if perfil_de_curva == '1':
	#	print('perfil 1 selecionado!')
	#if perfil_de_curva == '2':
	#	print('perfil 2 selecionado!')
	#if perfil_de_curva == '3':
	#	print('perfil 3 selecionado!')
		
	# Se não receber mada paramos o loop
	#if not data: break
	
	#if tamanho1 >=3:

	while True:
	
	
		if delta_tempo() > 1.0 :
			tamanho2, lista_de_linhas2, ultima_linha2 = pega_dados('file1.txt')
		
			if tamanho2 != tamanho1:
				print("tamanho alterado!")
				print("novo tamanho = ", tamanho2)
				print("linha inserida: ", ultima_linha2)
				json_da_lista = json.dumps(lista_de_linhas2)
				conexão.send(json_da_lista.encode())
				tamanho1 = tamanho2
				lista_de_linhas1 = lista_de_linhas2
				ultima_linha1 = ultima_linha2

				tempo_inicial = time.time()
		

	#Fecha a conexão criada depois de responder o cliente
	conexão.close()


