#Controle de servo no Raspberry Pi
#Autor: João Luiz
from pynput.keyboard import Listener
import python, pyHook
import RPi.GPIO as GPIO
import time

servo_pin = 7
angulo = 0 #angulo inicial para incremento

#Tamanho dos pulsos em milisegundos para cada grau 
deg_0_pulse   = 0.5 # 0º
deg_180_pulse = 2.5 # 180º
f = 50.0


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

def pressiona(Key):
	global angulo
	tecla = str(Key)
	if tecla == 'Key.right':
		angulo = angulo + 1
		print(angulo, tecla)
	if tecla == 'Key.left':
		angulo = angulo - 1	
		print(angulo, tecla)
		if angulo < 0:
   			print("cleaning up")
    		GPIO.cleanup()			
			sys.exit(0)

	set_angle(angulo)

##################################################################

set_pwm()


with Listener(on_press=pressiona) as l:
	try: 
		l.join()

	finally:
    	print("cleaning up")
    	GPIO.cleanup()
