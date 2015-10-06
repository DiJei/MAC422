#-------------------------------------#
#               util.py               #
#-------------------------------------#
#    Arqivo com funcoes auxiliares    #
#-------------------------------------#
from estruturas import *
from espacolivre import *
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
    i = 0
    while linha:
        linha_trace = linha.split(" ")
        if linha_trace[-1] == "\n" or linha_trace[-1] == '':
            linha_trace.pop()
        acessos = []
        for x in range(4, len(linha_trace), 2):
            acesso = Acesso(int(linha_trace[x]), int(linha_trace[x + 1]))
            acessos.append(acesso)
        processo = Processo(int(linha_trace[0]), linha_trace[1], i, int(linha_trace[2]), int(linha_trace[3]), acessos)
        if int(linha_trace[3]) not in tamanhos.keys():
            tamanhos[int(linha_trace[3])] = 1
        else:
            tamanhos[int(linha_trace[3])] = tamanhos[int(linha_trace[3])] + 1
        lista.append(processo)
        linha = trace.readline()
        i += 1
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


def simula_processos(tempo_inicio, lista_processos, mem_virtual):
    for processo in lista_processos:
        tempo_atual = time() - tempo_inicio
        if tempo_atual >= processo.tf and processo.rodando:
            print("ta =", tempo_atual, "tf =", processo.tf)
            mem_virtual.remove(processo.nome)
            processo.rodando = False
            processo.terminou = True
    escreve_na_memoria(mem_virtual, False)


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
