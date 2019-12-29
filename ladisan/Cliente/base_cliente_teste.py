from socket import *
import json
import time

#ip_raspberry = "200.156.93.194"
#ip_raspberry = "192.168.0.148"
#ip_raspberry = "192.168.0.175"
ip_raspberry = "127.0.0.1"

porta = 50007
#porta = 12000

caminho_arquivo_login="login.txt"
caminho_arquivo_log = "log.txt"
caminho_arquivo_file2 = "file2.txt"

def cria_cliente(ip, porta):
	"""
	Criamos o socket e o conectamos ao servidor
	"""
	ip = str(ip)
	global sockobj
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.connect((ip, porta))


def escreve_log(coisa):
	coisa=str(coisa)
	global caminho_arquivo_log
	with open(caminho_arquivo_log, 'a+') as arquivo_log:
		arquivo_log.write(coisa+'\n')

def apaga_tudo(arquivo):
	with open(arquivo, 'w') as arquivo:
		arquivo.close()

def envia_login():
	global caminho_arquivo_login
	with open(caminho_arquivo_login, "r") as arquivo:
		login = arquivo.read()
		login = login.strip('\n')
		login = login.split(',')

	#print("Arquivo: ", login)

	json_da_lista = json.dumps(login)
	#print("Json: ", json_da_lista)

	sockobj.send(json_da_lista.encode())


apaga_tudo(caminho_arquivo_file2)
apaga_tudo(caminho_arquivo_log)

try:

	cria_cliente(ip_raspberry, porta)
	escreve_log("Conexão socket com o RaspberryPi estabelecida!")
	#print("Conexão socket com o RaspberryPi estabelecida!")

	resposta=False
	while resposta!=True:
		envia_login()
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
		time.sleep(0.5)
		data = sockobj.recv(1000000)
		json_da_lista = data.decode("utf-8")
		lista_de_linhas = json.loads(json_da_lista)
		linhas = '\n'.join(lista_de_linhas)

		with open(caminho_arquivo_file2, 'w') as arquivo:
			arquivo.writelines(linhas)

except:
	escreve_log("Um erro de conexão ocorreu! / -Servidor desligado ou -Endereço IP e porta incorretos")
	#print("Um erro de conexão ocorreu! \n -Servidor desligado \n ou -Endereço IP e porta incorretos ")


	escreve_log("Fechando cliente...")
