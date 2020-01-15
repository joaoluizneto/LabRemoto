from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import matplotlib.pyplot as plt
import time

write_to_file_path = 'file1.txt'
tempo_de_coleta = 0.1

absissa = [x/60 for x in range(16*100)]

def curva_1(x,a):
	if x>=a:
		return 5*exp(-(1/3)*(x-a)**2/(2*(2.60)**2))+2
	else:
		return 5*exp(-3*(x-a)**2/(2*(2.60)**2))+2

def curva_2(x,a):
		return 5*exp(-(x-a)**2/(2*(2.60)**2))+2


def curva_3(x,a):
	if x<=a:
		return 5*exp(-(1/3)*(x-a)**2/(2*(2.60)**2))+2
	else:
		return 5*exp(-3*(x-a)**2/(2*(2.60)**2))+2


#print("Simulando coleta...")
for segundo in range(1460):
	time.sleep(tempo_de_coleta)
	line = str(segundo) + "," + str(round(curva_1(segundo/60,3)/60,5)) + "&" +str(round(curva_2(segundo/60,8)/60,5)) + "&" + str(round(curva_3(segundo/60,13)/60,5)) + "\n"
	#print(line)
	with open(write_to_file_path, "a") as myfile:
	    myfile.write(line)


#plt.plot(absissa, f(absissa), 'b')
