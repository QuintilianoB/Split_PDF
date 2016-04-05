#!/usr/bin/python2.7

from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import time

arquivo = "teste2.pdf"
tamanho_max_permitido = 990000
pasta_destino = "teste_script"
prefixo = "teste_"

inputpdf = PdfFileReader(open(arquivo, "rb"))

num_pag_total = inputpdf.numPages
cache_pag_total = num_pag_total
tamanho_total = os.stat(arquivo).st_size
tamanho_pagina = tamanho_total/num_pag_total
max_pag_arquivo = 10
cache_max_pag = max_pag_arquivo

ultima_pagina = 0
pagina_atual = 0

print num_pag_total

while(num_pag_total > 0):
	
	output = PdfFileWriter()

	nome_arquivo = pasta_destino + "/" + prefixo + str(pagina_atual) + ".pdf"
	
	for i in range(max_pag_arquivo):
		print "Pagina atual ---", pagina_atual
		if pagina_atual == cache_pag_total:
			break		
		output.addPage(inputpdf.getPage(pagina_atual))
		pagina_atual = pagina_atual + 1
		contador = i
		
	print "Gravando arquivo ---", nome_arquivo
	outputStream = file(nome_arquivo, "wb")
	output.write(outputStream)

	tamanho_arquivo_atual = os.stat(nome_arquivo).st_size
	
	if tamanho_arquivo_atual >= tamanho_max_permitido:
		print "Arquivo muito grande, reduzindo quantidade de paginas."
		ultima_pagina = pagina_atual - max_pag_arquivo
		pagina_atual = ultima_pagina		

		if max_pag_arquivo > 0:
			max_pag_arquivo = max_pag_arquivo - 1
		else:
			raise Exception("Pagina maior que tamanho maximo", pagina_atual)
	else:
		max_pag_arquivo = cache_max_pag
		ultima_pagina = pagina_atual - 1
		pagina_atual = ultima_pagina + 1 
		num_pag_total = num_pag_total - (contador + 1)
	
	print "Ultima pagina --", ultima_pagina
	print "Restante --", num_pag_total
	print "####"
			
	
	
