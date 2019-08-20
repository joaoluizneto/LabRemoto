def apaga_tudo(arquivo):
	with open(arquivo, 'w') as arquivo:
		arquivo.close()

apaga_tudo("file2.txt")
