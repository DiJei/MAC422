#-------------------------------------#
#               ep2.py                #
#-------------------------------------#
#    Programa com loop principal      #
#-------------------------------------#
from util import openFile, simulationStart, listaProcessosBuild
from estruturas import *
from espacolivre import *

#Coloca valores inicias
line = " "
comands = ()
espID = -1
subsID = -1
trace = None
total = 0
virtual = 0
memoria = None
listaProcessos = []

#----Loop Principal----#
while (1):
    #---Ler entrada---#
    line = input("[ep2]: ")
    comands = line.split(" ")

    #---Verifica comandos--#

    #Sai do programa
    if (comands[0] == "sai"):
        break

    #Carrega o arquivo trace
    if (comands[0] == "carrega"):
        trace = openFile(comands[1])
        if (trace != 0):
            temp = (trace.readline()).split(" ")
            total = int(temp[0])
            virtual = int(temp[1])
            listaProcessos = listaProcessosBuild(trace)
            trace.close()
            memoria = Lista(Item(True, "", 0, virtual))
            print("memoria:\n", memoria)

    #Seleciona qual algoritmo de esapaco usar
    if (comands[0] == "espaco"):
        espID = int(comands[1])

    #Seleciona qual algoritmo de substituicao usar
    if (comands[0] == "substitui"):
        subsID = int(comands[1])

    #Comeca simulacao
    if (comands[0] == "executa"):
        if ((espID < 1 or espID > 3) or (subsID < 1 or subsID > 4)):
            print("Valores para algoritmos errados")
        else:
            simulationStart(float(comands[1]), espID, subsID)
            # depois mexer aqui pra usar o simulationStart mesmo
            # e nao to considerando o tempo nem nada por enquanto
            for processo in listaProcessos:
                firstFit(memoria, processo)
                print(memoria)

#----FIM do programa----#