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
            aloca(lista, item.inicio_mem, processo)
            break


"""
Algoritmo que aloca o processo no primeiro pedaço de memória livre que achar
partindo da ultima busca feita anteriomente
"""
def nextFit(lista, processo, ultima_pos):
    pedaco_ultima_pos = lista.pedaco_na_pagina(int(ultima_pos / 16))
    while pedaco_ultima_pos:

        if pedaco_ultima_pos.inicio_mem != ultima_pos:
            tamanho_resto = pedaco_ultima_pos.tamanho_mem - (ultima_pos - pedaco_ultima_pos.inicio_mem)
            if tamanho_resto >= processo.b:
                pedaco_ultima_pos.fragmenta(ultima_pos)
                aloca(lista, ultima_pos, processo)
                return ultima_pos + processo.b
            pedaco_ultima_pos = pedaco_ultima_pos.prox
            ultima_pos = pedaco_ultima_pos.inicio_mem
            continue

        if pedaco_ultima_pos.tamanho_mem >= processo.b:
            aloca(lista, ultima_pos, processo)
            return ultima_pos + processo.b

        pedaco_ultima_pos = pedaco_ultima_pos.prox
        ultima_pos = pedaco_ultima_pos.inicio_mem


def aloca(lista, posicao, processo):
    num_pags = int(processo.b / 16)
    if processo.b % 16 != 0:
        num_pags += 1

    pedaco = lista.pedaco_na_pagina(int(posicao / 16))
    if pedaco.tamanho_mem > processo.b:
        posicao_fim_processo = pedaco.inicio_mem + (num_pags * 16) - 1
        tamanho_mem_resto = pedaco.tamanho_mem - num_pags * 16
        resto = Item(True, "", posicao_fim_processo + 1, tamanho_mem_resto)
        lista.adiciona_depois_de(pedaco, resto)

    pedaco.livre = False
    pedaco.proc_nome = processo.nome
    pedaco.proc_id = processo.pid
    pedaco.tamanho_mem = num_pags * 16

    processo.rodando = True
