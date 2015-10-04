#-------------------------------------#
#               util.py               #
#-------------------------------------#
#    Arqivo com funcoes auxiliares    #
#-------------------------------------#
from estruturas import *


#Abre o arquivo com nome dentro da string filename
def openFile(filename):
    try:
        trace = open(filename, "r")
        return trace
    except IOError:
        print ("Erro na abertura do arquivo")
        return 0


#Funcao para montar a lista de processos, com as informcoes do arquivo trace
def listaProcessosBuild(trace):
    lista = []
    linha = trace.readline()
    while linha:
        linha_trace = linha.split(" ")
        if linha_trace[-1] == "\n" or linha_trace[-1] == '':
            linha_trace.pop()
        acessos = []
        for x in range(4, len(linha_trace), 2):
            acesso = Acesso(int(linha_trace[x]), int(linha_trace[x + 1]))
            acessos.append(acesso)
        processo = Processo(int(linha_trace[0]), linha_trace[1], int(linha_trace[2]), int(linha_trace[3]), acessos)
        lista.append(processo)
        linha = trace.readline()
    return lista


#Funcao que comeca simulacao ja com parametros certos
def simulationStart(delay, espID, subsID):
    #Calma jose, tamo fazendo
    return 0
