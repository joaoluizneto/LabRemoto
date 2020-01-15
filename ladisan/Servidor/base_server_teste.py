#!/usr/bin/python3
#Server TCP/IP
from socket import *
import time, json, threading, subprocess

##############SERVER#############
ip_raspberry = "127.0.0.1"
porta_telemetria = 50007
porta_servo = 50008
caminho_arquivo_login="login.txt"
caminho_arquivo_file1 = "file1.txt"
tempo_de_coleta = 0.1
print(
"""
 ____  _____ _____           _____    _
|  _ \\| ____|_   _|         |_   _|__| | ___
| |_) |  _|   | |    _____    | |/ _ \\ |/ _ \\
|  __/| |___  | |   |_____|   | |  __/ |  __/
|_|   |_____| |_|             |_|\\___|_|\\___|
"""
)

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
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	sockobj.bind((ip, porta))
	#O socket começa a esperar por clientes limitando a 5 conexões por vez
	sockobj.listen(num_clientes)
	print("Servidor iniciado em ",ip, " na porta ",porta, ", esperando por no máximo ", num_clientes, " clientes")
	return sockobj

def recebe_cliente(sockobj):
	"""
	Aceita uma conexão quando encontrada e devolve a um novo socket conexão e o endereço do cliente conectado
	"""
	conexão, endereço = sockobj.accept()
	print('Server conectado por ', endereço)
	return conexão

#############TELEMETRIA############
def confere_login(lista):
	"""
	Confere se o login fornecido pelo usuário é válido
	"""
	login_name= lista[0]
	login_passw= lista[1]
	global caminho_arquivo_login
	with open(caminho_arquivo_login, "r") as arquivo:
		login = arquivo.read()
		login = login.strip('\n')
		login = login.split(',')
	if login_name==login[0] and login_passw==login[1]:
		return True
	else:
		return False

def apaga_tudo(arquivo):
	with open(arquivo, 'w') as arquivo:
		arquivo.close()

def pega_dados(arquivo):
	"""
	Extrai os dados coletados do arquivo "file1.txt"
	"""
	with open(arquivo, 'r') as data:
		texto = data.read()
	lista_de_linhas = texto.split('\n')
	tamanho = len(lista_de_linhas)
	ultima_linha = str(lista_de_linhas[len(lista_de_linhas)-2])
	return (tamanho, lista_de_linhas, ultima_linha)

def telemetria():

	sockobj = cria_servidor(ip_raspberry, porta_telemetria, 5)

	while True:

		apaga_tudo(caminho_arquivo_file1)

		tamanho1, lista_de_linhas1, ultima_linha1 = pega_dados(caminho_arquivo_file1)

			# Aceita uma conexão quando encontrada e devolve a um novo socket conexão e o endereço do cliente conectado
		conexão = recebe_cliente(sockobj) #fica esperando o cliente aparecer

		confere=False
		while confere == False:
			data = conexão.recv(1024)
			json_da_lista = data.decode("utf-8")
			lista = json.loads(json_da_lista)
			confere = confere_login(lista)

			if confere==True:
				print("Login efetuado!")
				json_confere = json.dumps(confere).encode()
				conexão.send(json_confere)
			else:
				print("Login incorreto!")
				json_confere = json.dumps(confere).encode()
				conexão.send(json_confere)

		coleta = subprocess.Popen(["python3", "simula_coleta.py"])

		while True:
			time.sleep(tempo_de_coleta)
			tamanho2, lista_de_linhas2, ultima_linha2 = pega_dados('file1.txt')

			if tamanho2 != tamanho1:
				#print("linha inserida: ", ultima_linha2)
				json_da_lista = json.dumps(lista_de_linhas2)
				try:
					conexão.send(json_da_lista.encode())
				except (BrokenPipeError, ConnectionResetError) as e:
					print("Cliente desligado!!")
					break
				tamanho1 = tamanho2
				lista_de_linhas1 = lista_de_linhas2
				ultima_linha1 = ultima_linha2

		print("Fechando servidor...\n")
		coleta.terminate()
		conexão.close()


##########SERVOPUBLISHER###########
def controla_servo():
	sockobj_servo = cria_servidor(ip_raspberry, porta_servo, 1)

	while True:
		conexão_servo = recebe_cliente(sockobj_servo) #fica esperando o cliente aparecer
		comando = "start"
		while True:
			#try:
			time.sleep(0.5)
			data = conexão_servo.recv(100000)
			if len(data)==0:
				break

			novo_comando = data.decode("utf-8")
			if comando != novo_comando:
				print("comando: ",novo_comando)
				comando = novo_comando
			#except:
			#	print("Um erro de conexão ocorreu! \n -Servidor desligado \n ou -Endereço IP e porta incorretos ")
		conexão_servo.shutdown(0)
		conexão_servo.close()


#########COMEÇA O PROGRAMA#########
Thread1 = threading.Thread(target=telemetria)
Thread2 = threading.Thread(target=controla_servo)

Thread1.daemon = True
Thread2.daemon = True

try:
	Thread1.start()
	Thread2.start()
	Thread1.join()
	Thread2.join()

except KeyboardInterrupt:
	print("\nCtrl-C/ Pesquisa cancelada!")
	exit()
