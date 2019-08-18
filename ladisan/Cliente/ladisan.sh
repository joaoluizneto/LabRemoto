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
		echo 'Iniciando cliente socket e gráfico de vazão...'
		echo -e '\n\n'
		python3 base_cliente_teste.py &
		python3 live_graph.py &
		numero=`wc -l log.txt`

		until ps $erro -eq 1
		do
			if test ! $numero -eq `wc -l log.txt`
			then
			echo `tail -1 log.txt`
			fi

			if test -e `tail -1 log.txt` | grep erro
			then
				erro=1
				break
			fi
		done
		echo 'saindo do programa...'

fi



