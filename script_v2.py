#!/usr/bin/python2.7

from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import time
import argparse
from datetime import datetime


def converter(arquivo_original, max_pag_arquivo, tamanho_max, pasta_destino,
              prefixo):

    inputpdf = PdfFileReader(open(arquivo_original, "rb"))
    num_pag_total = inputpdf.numPages
    cache_pag_total = num_pag_total
    cache_max_pag = max_pag_arquivo
    ultima_pagina = 0
    pagina_atual = 0

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

        if tamanho_arquivo_atual >= tamanho_max:
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


def main():

    def msg(name=None):
        return '''script_v2.py

            Example: python2.7 script_v2.py --arquivo teste.pdf --max_pag 10 --max_size 400 --pasta teste --prefixo teste
            '''

    parser = argparse.ArgumentParser(description="Separador de arquivos PDF.",
                                     usage=msg())
    parser.add_argument('--arquivo', help="Arquivo a ser dividido.")
    parser.add_argument('--max_pag', help="Numero maximo de paginas por arquivo criado.", type=int)
    parser.add_argument('--max_size', help="Tamanho maximo de cada arquivo criado em Kbytes. Ex: 990")
    parser.add_argument('--pasta', help="Pasta de destino para armazenar os arquivos criados.")
    parser.add_argument('--prefixo', help="Prefixo para os arquivos criados.")

    # Receives the arguments sent by the user.
    args = parser.parse_args()
    arquivo_original = args.arquivo
    max_pag_arquivo = args.max_pag
    tamanho_max = args.max_size
    pasta_destino = args.pasta
    prefixo = args.prefixo

    # If target file is not set, prints the help menu from argparse and exits.
    if arquivo_original is None or tamanho_max is None or pasta_destino is None:
        print parser.print_help()
        exit(0)

    if max_pag_arquivo is None:
        max_pag_arquivo = 10

    if prefixo is None:
        prefixo = datetime.now().strftime('%Y%m%d_')

    converter(arquivo_original, max_pag_arquivo, tamanho_max, pasta_destino, prefixo)


if __name__ == '__main__':
    main()
