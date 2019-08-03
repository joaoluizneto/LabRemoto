#!/bin/bash

saida=`(saida=`python3 base_cliente_teste.py`;echo $saida)`

var=`echo $saida | grep erro`

if test ! erro:
	then
	echo 'nenhum erro detectado!'
else
echo 'um erro ocorreu'

fi
