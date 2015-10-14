#-------------------------------------#
#               ep2.py                #
#-------------------------------------#
#    Programa com loop principal      #
#-------------------------------------#
from util import *
from time import *
from estruturas import *

#Coloca valores inicias
line = " "
comandos = ()
espID = 1
subsID = 1
trace = None
total = 0
virtual = 0
memoria_virtual = None
memoria_fisica = None
tabela_paginas = None
listaProcessos = []
lista_paginas = []
tempo_inicio = 0
tamanhos = {} #Dicionario que guarda quantas vezes cada tamanho ocorreu no arquivo
#----Loop Principal----#
while (1):
    #---Ler entrada---#
    line = input("[ep2]: ")
    comandos = line.split(" ")

    #---Verifica comandos--#

    #Sai do programa
    if (comandos[0] == "sai"):
        break

    #Carrega o arquivo trace
    if (comandos[0] == "carrega"):
        trace = openFile(comandos[1])
        if (trace != 0):
            temp = (trace.readline()).split(" ")
            total = int(temp[0])
            virtual = int(temp[1])
            listaProcessos = listaProcessosBuild(trace,tamanhos)
            tamanhos_repetidos = sorted(tamanhos.items(), key = itemgetter(1)) #Lista com tuplas de pares tamanho em b e quantidade de vezes que se repete
            trace.close()
            memoria_virtual = Lista(Item(True, "", 0, virtual))
            memoria_fisica = Lista(Item(True, "", 0, total))
            tabela_paginas = TabelaPagina(virtual)
            print("memoria_virtual:\n", memoria_virtual)
            print("memoria_fisica:\n", memoria_fisica)

    #Seleciona qual algoritmo de esapaco usar
    if (comandos[0] == "espaco"):
        espID = int(comandos[1])

    #Seleciona qual algoritmo de substituicao usar
    if (comandos[0] == "substitui"):
        subsID = int(comandos[1])

    #Comeca simulacao
    if (comandos[0] == "executa"):
        if ((espID < 1 or espID > 3) or (subsID < 1 or subsID > 4)):
            print("Valores para algoritmos errados")
        else:
            tempo_inicio = time()
            # depois mexer aqui pra usar o simulationStart mesmo
            i = 0
            ultima_pos = memoria_virtual.inicio.inicio_mem
            dic_tamanhos_fixos = {16: [], 32: [], 128: [], 512: [], 1024: [], 2048: []}
            while not processos_terminaram(listaProcessos):
                if i % 5 == 0:
                    tabela_paginas.reseta_acessos()

                if espID == 1:
                    gerencia_memoria(tempo_inicio, listaProcessos, memoria_virtual)

                if espID == 2:
                    ultima_pos = gerencia_memoria(tempo_inicio, listaProcessos, memoria_virtual, ultima_pos)

                if espID == 3:
                    gerencia_memoria(tempo_inicio, listaProcessos, memoria_virtual, None, dic_tamanhos_fixos)

                print("ultima_pos =", ultima_pos, "mem_vir pos aloc:\n", memoria_virtual)

                if espID != 3:
                    simula_processos(tempo_inicio, lista_paginas, listaProcessos, tabela_paginas, memoria_virtual, memoria_fisica)
                else:
                    simula_processos(tempo_inicio, lista_paginas, listaProcessos, tabela_paginas, memoria_virtual, memoria_fisica, dic_tamanhos_fixos)

                print(i, "s")
                print("mem_vir:\n", memoria_virtual)
                print("mem_fis:\n", memoria_fisica)
                sleep(1)
                i += 1
#----FIM do programa----#
