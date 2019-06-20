from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import matplotlib.pyplot as plt
import time

write_to_file_path = 'file1.txt'

x = ar([x*2 for x in range(8)]) # 0,2,4,...,14
y = ar([2,4,6,7,6,4,1,2])

n = len(x)                          #the number of data
mean = sum(x*y)/n                   #note this correction
sigma = sum(y*(x-mean)**2)/n        #note this correction

def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))+2

popt,pcov = curve_fit(gaus,x,y,p0=[0,mean,sigma])

absissa = [x/60 for x in range(16*60)]

def f(x): 
    global popt 
    return gaus(x,*popt)

arquivo = open(write_to_file_path, 'w')
arquivo.close()

print("Simulando coleta...")
for segundo in range(14*60):
	time.sleep(1)
	line = str(segundo) + "," + str(f(segundo/60)) + "\n"
	print(line)

	arquivo = open(write_to_file_path, 'r') # Abra o arquivo (leitura)
	conteudo = arquivo.readlines()
	conteudo.append(line)   # insira seu conteúdo
	arquivo = open(write_to_file_path, 'w') # Abre novamente o arquivo (escrita)
	arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente 	nele.
	arquivo.close()


	
#plt.plot(absissa, f(absissa), 'b')


