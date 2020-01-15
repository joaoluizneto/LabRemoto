#Acionamento do Servo-motor -- cliente
from socket import *
import time

###################CLIENT###################
ip = "127.0.0.1"

porta = 12000

def cria_cliente(ip, porta):
	"""
	Criamos o socket e o conectamos ao servidor
	"""
	ip = str(ip)
	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.connect((ip, porta))
	return sockobj

###############################################

sockobj = cria_cliente(ip, porta)

while True:
	try:
		data = input("Coloca aí o angulo: ").encode()
		sockobj.send(data)
	except KeyboardInterrupt:
		print("Aplicativo cancelado!!")
		exit()
