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
    pedaco_ultima_pos = lista.pedaco_na_posicao(ultima_pos)
    while pedaco_ultima_pos:

        if pedaco_ultima_pos.inicio_mem != ultima_pos:
            tamanho_resto = pedaco_ultima_pos.tamanho_mem - (ultima_pos - pedaco_ultima_pos.inicio_mem)
            if tamanho_resto >= processo.b:
                lista.fragmenta(ultima_pos)
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


def quick_fit(lista_memoria, processo, dic_tamanhos_fixos):
    try:
        posicao = dic_tamanhos_fixos[processo.b][0]
        aloca(lista_memoria, posicao, processo)
        return
    except (KeyError, IndexError):
        for tamanho in sorted(dic_tamanhos_fixos.keys()):
            if tamanho > processo.b and dic_tamanhos_fixos[tamanho]:
                posicao = dic_tamanhos_fixos[tamanho][0]
                dic_tamanhos_fixos[tamanho].remove(posicao)
                aloca(lista_memoria, posicao, processo)
                return

        # não achou nenhuma posição nas listas de tamanhos fixos, usa First Fit
        print("caí no first fit...")
        firstFit(lista_memoria, processo)


def atualiza_dic_tamanhos_fixos(lista_memoria, dic_tamanhos_fixos):
    for item in lista_memoria:
        if item.tamanho_mem in dic_tamanhos_fixos.keys() and item.livre:
            dic_tamanhos_fixos[item.tamanho_mem].append(item.inicio_mem)

    for tamanho in dic_tamanhos_fixos.keys():
        for posicao in dic_tamanhos_fixos[tamanho]:
            pedaco_da_posicao = lista_memoria.pedaco_na_posicao(posicao)
            if pedaco_da_posicao.tamanho_mem != tamanho or not pedaco_da_posicao.livre:
                dic_tamanhos_fixos[tamanho].remove(posicao)


def aloca(lista, posicao, processo):
    num_pags = int(processo.b / 16)
    if processo.b % 16 != 0:
        num_pags += 1

    pedaco = lista.pedaco_na_pagina(int(posicao / 16))
    if pedaco.tamanho_mem > (num_pags * 16):
        posicao_fim_processo = pedaco.inicio_mem + (num_pags * 16) - 1
        tamanho_mem_resto = pedaco.tamanho_mem - num_pags * 16
        resto = Item(True, "", posicao_fim_processo + 1, tamanho_mem_resto)
        lista.adiciona_depois_de(pedaco, resto)

    pedaco.livre = False
    pedaco.proc_nome = processo.nome
    pedaco.proc_id = processo.pid
    pedaco.tamanho_mem = num_pags * 16

    processo.rodando = True
