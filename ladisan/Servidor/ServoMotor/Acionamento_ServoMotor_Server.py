#Acionamento do Servo-motor -- Server
from socket import *
import os, time
#import RPi.GPIO as GPIO

###################SERVER###################
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
	return conexão, endereço

####################SERVO#####################
servo_pin = 7
angulo = 0 #angulo inicial para incremento

#Tamanho dos pulsos em milisegundos para cada grau
deg_0_pulse   = 0.5 # 0º
deg_180_pulse = 2.5 # 180º
f = 50.0 #frequencia

def set_pwm(servo_pin,f):
	#Iniciar o pino gpio
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(servo_pin,GPIO.OUT)
	pwm = GPIO.PWM(servo_pin,f)
	pwm.start(0)

def set_angle(angle):
	period = 1000/f #Período em milisegundos
	deg_0_duty = (deg_0_pulse/period)*100 # Porcentagem para 0º= 2.5%
	duty_range = ((deg_180_pulse - deg_0_pulse)/period)*100 # Proporção de tamanho completo 0.5 à 2.5
	duty = deg_0_duty + (angle/180.0)*duty_range
	pwm.ChangeDutyCycle(duty)

#############################################
sockobj=cria_servidor('localhost', 12000, 1)

conexão, endereço = recebe_cliente(sockobj) #fica esperando o cliente aparecer

while True:
	try:
	    data = conexão.recv(1024)
	    angulo = data.decode("utf-8")
	    print(angulo)
	except:
		print("Aplicaçãp cancelada Crt-C")
		exit()
