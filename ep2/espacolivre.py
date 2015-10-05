#--------------------------------------------#
#              espacolivre.py                #
#--------------------------------------------#
#   Algoritmos de gerência de espaço livre   #
#--------------------------------------------#
from estruturas import *

"""
Algoritmo que aloca o processo no primeiro pedaço de memória livre que achar
ao procurar na lista que identifica os pedaços livres e os ocupados
"""
def firstFit(lista, processo):
    for item in lista:
        if item.livre and item.tamanho_mem >= processo.b:
            aloca(lista, item, processo)
            break


def aloca(lista, posicao, processo):
    if posicao.tamanho_mem > processo.b:
        posicao_fim_processo = posicao.inicio_mem + processo.b - 1
        tamanho_mem_resto = posicao.tamanho_mem - processo.b
        resto = Item(True, "", posicao_fim_processo + 1, tamanho_mem_resto)
        lista.adiciona_depois_de(posicao, resto)

    posicao.livre = False
    posicao.proc_nome = processo.nome
    posicao.tamanho_mem = processo.b
