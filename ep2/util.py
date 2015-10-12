#-------------------------------------#
#               util.py               #
#-------------------------------------#
#    Arqivo com funcoes auxiliares    #
#-------------------------------------#
from estruturas import *
from espacolivre import *
from substituipaginas import *
from struct import *
from time import *
from operator import itemgetter

#Abre o arquivo com nome dentro da string filename
def openFile(filename):
    try:
        trace = open(filename, "r")
        return trace
    except IOError:
        print ("Erro na abertura do arquivo")
        return 0


#Funcao para montar a lista de processos, com as informcoes do arquivo trace
def listaProcessosBuild(trace, tamanhos):
    lista = []
    linha = trace.readline()
    pid = 0
    while linha:
        linha_trace = linha.split(" ")
        if linha_trace[-1] == "\n" or linha_trace[-1] == '':
            linha_trace.pop()
        acessos = []
        for x in range(4, len(linha_trace), 2):
            acesso = Acesso(int(linha_trace[x]), int(linha_trace[x + 1]))
            acessos.append(acesso)
        processo = Processo(int(linha_trace[0]), linha_trace[1], pid, int(linha_trace[2]), int(linha_trace[3]), acessos)
        if int(linha_trace[3]) not in tamanhos.keys():
            tamanhos[int(linha_trace[3])] = 1
        else:
            tamanhos[int(linha_trace[3])] = tamanhos[int(linha_trace[3])] + 1
        lista.append(processo)
        linha = trace.readline()
        pid += 1
    return lista

def processos_terminaram(lista_processos):
    for processo in lista_processos:
        if not processo.terminou:
            return False
    return True


def gerencia_memoria(tempo_inicio, lista_processos, mem_virtual):
    for processo in lista_processos:
        tempo_atual = time() - tempo_inicio
        if tempo_atual >= processo.t0 and not processo.rodando and not processo.terminou:
            firstFit(mem_virtual, processo)
    escreve_na_memoria(mem_virtual, False)

"""
Temporario
"""
def gerencia_memoria2(tempo_inicio, lista_processos, mem_virtual, ultimo):
    for processo in lista_processos:
        tempo_atual = time() - tempo_inicio
        if tempo_atual >= processo.t0 and not processo.rodando and not processo.terminou:
           ultimo =  nextFit(mem_virtual, processo, ultimo)
    escreve_na_memoria(mem_virtual, False)

def simula_processos(tempo_inicio, lista_paginas, lista_processos, tabela_paginas, mem_virtual, mem_fisica):
    for processo in lista_processos:
        tempo_atual = time() - tempo_inicio

        for acesso in processo.acessos:
            if tempo_atual >= acesso.instante and not acesso.ocorreu:
                processo_mem_virt = mem_virtual.localiza(processo.nome)
                if processo_mem_virt:
                    posicao_virtual = processo_mem_virt.inicio_mem + acesso.posicao
                posicao_fisica = tabela_paginas.map(posicao_virtual)
                if posicao_fisica is not None:
                    print("Posicao", posicao_virtual, "está no quadro", posicao_fisica)
                else:
                    print("Page Fault!!!", (posicao_virtual))
                    gerencia_paginas(lista_paginas, tabela_paginas, posicao_virtual, processo, mem_fisica)
                acesso.ocorreu = True
                # atualiza bit R
                tabela_paginas.acessos[int(posicao_virtual / 16)] = 1


        if tempo_atual >= processo.tf and processo.rodando:
            print("ta =", tempo_atual, "tf =", processo.tf)
            libera_paginas(tabela_paginas, lista_paginas, mem_virtual, processo)
            mem_virtual.remove(processo.nome)
            mem_fisica.remove(processo.nome)
            processo.rodando = False
            processo.terminou = True

    escreve_na_memoria(mem_virtual, False)
    escreve_na_memoria(mem_fisica, True)


def libera_paginas(tabela_paginas, lista_paginas, mem_virtual, processo):
    end_virt = mem_virtual.localiza(processo.nome)
    for pagina in range(end_virt.inicio_mem, end_virt.inicio_mem + end_virt.tamanho_mem, 16):
        tabela_paginas.tabela[int(pagina / 16)] = None
        print("vou remover", int(pagina/16))
        if int(pagina / 16) in lista_paginas:
            lista_paginas.remove(int(pagina / 16))


def gerencia_paginas(lista_paginas, tabela_paginas, posicao_virtual, processo, mem_fisica):
    print("lista:", lista_paginas)
    for pedaco in mem_fisica:
        if pedaco.livre and pedaco.tamanho_mem >= 16:
            tabela_paginas.tabela[int(posicao_virtual / 16)] = int(pedaco.inicio_mem / 16)
            pagina = Processo(processo.t0, processo.nome, processo.pid, processo.tf, 16, processo.acessos)
            aloca(mem_fisica, pedaco, pagina)
            lista_paginas.append(int(posicao_virtual / 16))
            print("adicionei", int(posicao_virtual / 16))
            return

    # nenhum espaço livre na memória física
    # chama algoritmo de substituição de página escolhido
    first_in_first_out(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)
    #second_chance_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)
    #not_recently_used_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)


# funcao que converte array de -1s de tamanho tamanho em string binaria
# (em hexadecimal) correspondente (1 byte por numero) e depois escreve
# isso no arquivo
def escreve_na_memoria(lista, principal):
    mem = b""
    for item in lista:
        tamanho = item.tamanho_mem
        if item.livre:
            mem += pack('b' * tamanho, *([-1] * tamanho))
        else:
            mem += pack('b' * tamanho, *([item.proc_id] * tamanho))
    if principal:
        arq = "/tmp/ep2.mem"
    else:
        arq = "/tmp/ep2.vir"
    with open(arq, 'wb') as memoria:
        memoria.write(mem)
        memoria.close()


#Funcao que comeca simulacao ja com parametros certos
def simulationStart(delay, espID, subsID, total, virtual):
    #Calma jose, tamo fazendo
    return 0
