import sys
from pynput.keyboard import Listener

angulo = 0

class MyException(Exception): pass
 
def on_press(Key):
	global angulo
	tecla = str(Key)
	if tecla == 'Key.right':
		angulo = angulo + 1
		print(angulo)
	if tecla == 'Key.left':
		angulo = angulo - 1
		print(angulo)	
	if angulo < 0:
		sys.exit(0)
    

with Listener(on_press=on_press) as l:
	l.join()

