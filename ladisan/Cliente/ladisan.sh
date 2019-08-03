#!/bin/bash

clear
echo ''
echo ''
echo '###  INTERFACE DE AUTOMAÇÂO DO CLIENTE  ###'
echo '###########################################'
echo '   _          ____ ___ ____                '
echo '  | |    __ _|  _ \_ _/ ___|  __ _ _ __    '
echo '  | |   / _` | | | | |\___ \ / _` | ´_ \   '
echo '  | |__| (_| | |_| | | ___) | (_| | | | |  '
echo '  |_____\__,_|____/___|____/ \__,_|_| |_|  '
echo '                                           '
echo '###########################################'

echo -e 'Laboratório de Drenagem, Irrigação e Saneamento Ambiental \n'
echo ''
echo ''
echo ''
echo ''
echo ''
echo 'INFO:'
echo 'Esse é um software feito pelo PET-Tele da UFF, com o objetivo de automatizar um procedimento experimental. '
echo ''

#Verifica se o usuário quer iniciar o programa
echo 'Você deseja continuar? [Y/N]'

read decide

if test $decide = 'Y' -o $decide = 'y'
	then
		prosseguir=1
else
	echo 'Tchau :)'
	exit
fi

echo -e '\n\n\n\n'

if test $prosseguir -eq 1
	then
		echo 'Iniciando cliente socket...'
		echo -e '\n\n'
		erro_python=`python3 base_cliente_teste.py` &
		erro=`echo $erro_python | grep erro`
		if test ! $erro
			then
			echo 'O cliente socket foi iniciado com sucesso!'
			echo -e '\n\n\n'
			echo 'Iniciando gráfico de vazão...'
rro ocorreu'

fi
			echo -e '\n\n\n'
			python3 live_graph.py
		else
			echo 'Um problema de conexão foi encontrado!'
		fi
fi

