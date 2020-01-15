#Cliente TCP/IP

from socket import *
import json, time, threading, signal, sys

##############CLIENTE##############
ip_raspberry = "127.0.0.1"
porta_telemetria = 50007
porta_servo = 50008
caminho_arquivo_login="login.txt"
caminho_arquivo_log = "log.txt"
caminho_arquivo_file2 = "file2.txt"
tempo_de_coleta = 0.1

def cria_cliente(ip, porta):
	"""
	Criamos o socket e o conectamos ao servidor
	"""
	ip = str(ip)
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.connect((ip, porta))
	return sockobj

#############TELEMETRIA############
def escreve_log(inform):
	inform=str(inform)
	with open(caminho_arquivo_log, 'a+') as arquivo_log:
		arquivo_log.write(inform+'\n')


def apaga_tudo(arquivo):
	with open(arquivo, 'w') as arquivo:
		arquivo.close()

def envia_login(sockobj):
	"""
	Coleta os dados do arquivo de login e envia para o servidor para iniciar a coleta dos dados.
	"""
	global caminho_arquivo_login
	with open(caminho_arquivo_login, "r") as arquivo:
		login = arquivo.read()
		login = login.strip('\n')
		login = login.split(',')

	#print("Arquivo: ", login)

	json_da_lista = json.dumps(login)
	#print("Json: ", json_da_lista)

	sockobj.send(json_da_lista.encode())

def telemetria(sockobj):
	"""
	Thread 1 (visualização dos dados)
	"""
#	try:
	resposta=False
	while resposta!=True:
		envia_login(sockobj)
		data = sockobj.recv(1024)
		resposta = data.decode("utf-8")
		resposta = json.loads(resposta)
		if resposta==True:
			#print("Login efetuado!")
			escreve_log("Login efetuado!")
		else:
			#print("Login incorreto!")
			escreve_log("Login incorreto!")

	while True:
		#Depois de mandar uma mensagem esperamos uma resposta do servidor
		try:
			time.sleep(tempo_de_coleta)
			sockobj.settimeout(2)
			data = sockobj.recv(100000)
			sockobj.settimeout(0)
			if len(data) == 0:
				print("O servidor fechou!!")
				exit()

			palavra = data.decode("utf-8")
			contagem = palavra.count("[")

			if contagem > 1:
				lista_palavra = palavra.split("]")
				data = lista_palavra.pop(0)+"]"

			lista_de_linhas = json.loads(data)
			linhas = '\n'.join(lista_de_linhas)

			with open(caminho_arquivo_file2, 'w') as arquivo:
				arquivo.writelines(linhas)

		except:

			sockobj.close()
			escreve_log("Um erro de conexão ocorreu! / -Servidor desligado ou -Endereço IP e porta incorretos")
			print("Um erro de conexão ocorreu! \n -Servidor desligado \n ou -Endereço IP e porta incorretos ")

			escreve_log("Fechando cliente...")
			exit()

##########SERVOMESSANGER###########
def controla_servo(sockobj):
	apaga_tudo("servomessanger.txt")
	while True:
		time.sleep(0.5)
		comando = "start"
		with open("servomessanger.txt", 'r') as arquivo:
			comandos = arquivo.read()
			comandos = comandos.split('\n')
		novo_comando = comandos[len(comandos)-2]
		if novo_comando != comando:
			sockobj.send(novo_comando.encode("utf-8"))
			comando = novo_comando
	sockobj.close()

#####################COMEÇA O PROGRAMA########################
apaga_tudo(caminho_arquivo_file2)
apaga_tudo(caminho_arquivo_log)

try:
	sockobj_telem = cria_cliente(ip_raspberry, porta_telemetria)
	escreve_log("Conexão socket com o RaspberryPi estabelecida!")

	sockobj_servo = cria_cliente(ip_raspberry, porta_servo)
	escreve_log("Conexão socket com o RaspberryPi estabelecida!")

except:
	escreve_log("RaspberryPi offline!!")
	exit()


Thread1 = threading.Thread(target=telemetria, args=(sockobj_telem,))
Thread2 = threading.Thread(target=controla_servo, args=(sockobj_servo,))

Thread1.daemon = True
Thread2.daemon = True

try:
	Thread1.start()
	Thread2.start()
	Thread1.join()
	Thread2.join()

except KeyboardInterrupt:
	print("\nCtrl-C")
	exit()
