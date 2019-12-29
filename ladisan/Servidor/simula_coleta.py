from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import matplotlib.pyplot as plt
import time

write_to_file_path = 'file1.txt'

absissa = [x/60 for x in range(16*60)]

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
for segundo in range(14*60):
	time.sleep(1)
	line = str(segundo) + "," + str(curva_1(segundo/60,3)/60) + "&" +str(curva_2(segundo/60,8)/60) + "&" + str(curva_3(segundo/60,13)/60) + "\n"
	#print(line)

	arquivo = open(write_to_file_path, 'r') # Abra o arquivo (leitura)
	conteudo = arquivo.readlines()
	conteudo.append(line)   # insira seu conteúdo
	arquivo = open(write_to_file_path, 'w') # Abre novamente o arquivo (escrita)
	arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente 	nele.
	arquivo.close()



#plt.plot(absissa, f(absissa), 'b')


