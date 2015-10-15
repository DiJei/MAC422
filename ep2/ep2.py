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
espID = 0
subsID = 0
trace = None
total = 0
virtual = 0
memoria_virtual = None
memoria_fisica = None
tabela_paginas = None
listaProcessos = []
lista_paginas = []
matriz_acessos = None
tempo_inicio = 0

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
            listaProcessos = listaProcessosBuild(trace)
            trace.close()
            memoria_virtual = Lista(Item(True, "", 0, virtual))
            memoria_fisica = Lista(Item(True, "", 0, total))
            tabela_paginas = TabelaPagina(virtual)
            print("memoria_virtual:\n", memoria_virtual)
            print("memoria_fisica:\n", memoria_fisica)

    #Seleciona qual algoritmo de esapaco usar
    if (comandos[0] == "espaco"):
        try:
            espID = int(comandos[1])
        except IndexError:
            print("Especifique o número correspondente ao algoritmo de gerência de espaço livre desejado")
            continue

    #Seleciona qual algoritmo de substituicao usar
    if (comandos[0] == "substitui"):
        try:
            subsID = int(comandos[1])
        except IndexError:
            print("Especifique o número correspondente ao algoritmo de substituição de página desejado")
            continue

    #Comeca simulacao
    if (comandos[0] == "executa"):
        if len(comandos) == 1:
            print("Especifique de quantos em quantos segundos o estado das memórias deve ser exibido")
            continue
        if ((espID < 1 or espID > 3) or (subsID < 1 or subsID > 4)):
            print("Valores para algoritmos errados")
        else:
            tempo_inicio = time()
            # depois mexer aqui pra usar o simulationStart mesmo
            i = 0
            ultima_pos = memoria_virtual.inicio.inicio_mem
            dic_tamanhos_fixos = {16: [], 32: [], 128: [], 512: [], 1024: [], 2048: []}
            if subsID == 4:
                matriz_acessos = MatrizAcessos(int(total / 16))

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
                    simula_processos(tempo_inicio, lista_paginas, listaProcessos, tabela_paginas, memoria_virtual, memoria_fisica, subsID, matriz_acessos)
                else:
                    simula_processos(tempo_inicio, lista_paginas, listaProcessos, tabela_paginas, memoria_virtual, memoria_fisica, subsID, matriz_acessos, dic_tamanhos_fixos)

                print(i, "s")
                print("mem_vir:\n", memoria_virtual)
                print("mem_fis:\n", memoria_fisica)
                if subsID == 4:
                    print(matriz_acessos.matriz)
                sleep(1)
                i += 1
#----FIM do programa----#
