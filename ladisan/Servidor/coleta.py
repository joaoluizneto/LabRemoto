import serial


serial_port = '/dev/ttyACM0'
baud_rate = 9600; #In arduino, Serial.begin(baud_rate)
write_to_file_path = "file1.txt"

ser = serial.Serial(serial_port, baud_rate)

while True:
	line = ser.readline()
	line = line.decode("utf-8")
	if line == '\n':
		line = '0'
	if line == ',':
		line = '0'

	if float(line[0])<=1:
	
		while True:
		
			line = ser.readline()
			line = line.decode("utf-8") #ser.readline returns a binary, convert to str   
			print(line)
			
			arquivo = open(write_to_file_path, 'r') # Abra o arquivo (leitura)
			conteudo = arquivo.readlines()
			conteudo.append(line)   # insira seu conteúdo
		
			arquivo = open(write_to_file_path, 'w') # Abre novamente o arquivo (escrita)
			arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente 	nele.

			arquivo.close()





