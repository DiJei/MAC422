#-------------------------------------#
#               ep2.py                #
#-------------------------------------#
#    Programa com loop principal      #
#-------------------------------------#
from util import *
from time import *
from estruturas import *

# Coloca valores inicias
espID = 0
subsID = 0
total = 0
virtual = 0
tempo_reseta_r = 3          # de quanto em quanto tempo reseta bit R
memoria_virtual = None
memoria_fisica = None
tabela_paginas = None
lista_processos = []
lista_paginas = []
tempo_inicio = 0

# Loop Principal
while (1):

    # Lê entrada
    line = input("[ep2]: ")
    comandos = line.split(" ")

    # Verifica comandos

    # Sai do programa
    if (comandos[0] == "sai"):
        break

    # Carrega o arquivo trace
    if (comandos[0] == "carrega"):
        trace = abre_arquivo(comandos[1])
        if (trace != 0):
            temp = (trace.readline()).split(" ")
            total = int(temp[0])
            virtual = int(temp[1])
            lista_processos = monta_lista_processos(trace)
            trace.close()
            memoria_virtual = Lista(Item(True, "", 0, virtual))
            memoria_fisica = Lista(Item(True, "", 0, total))
            tabela_paginas = TabelaPagina(virtual)

    # Seleciona qual algoritmo de espaço usar
    if (comandos[0] == "espaco"):
        try:
            espID = int(comandos[1])
        except IndexError:
            print("Especifique o número correspondente ao algoritmo de gerência de espaço livre desejado")
            continue

    # Seleciona qual algoritmo de substituição usar
    if (comandos[0] == "substitui"):
        try:
            subsID = int(comandos[1])
        except IndexError:
            print("Especifique o número correspondente ao algoritmo de substituição de página desejado")
            continue

    # Começa simulação
    if (comandos[0] == "executa"):
        if len(comandos) == 1:
            print("Especifique de quantos em quantos segundos o estado das memórias deve ser exibido")
            continue

        if ((espID < 1 or espID > 3) or (subsID < 1 or subsID > 4)):
            print("Valores para algoritmos errados")

        else:
            tempo_inicio = time()
            i = 0

            if espID == 2:
                ultima_pos = memoria_virtual.inicio.inicio_mem

            if espID == 3:
                dic_tamanhos_fixos = {}
                for x in range(16, 1601, 16):
                    dic_tamanhos_fixos[x] = []

            while not processos_terminaram(lista_processos):
                if i % tempo_reseta_r == 0:
                    tabela_paginas.reseta_acessos()

                if espID == 1:
                    gerencia_memoria(tempo_inicio, lista_processos, memoria_virtual)

                if espID == 2:
                    ultima_pos = gerencia_memoria(tempo_inicio, lista_processos, memoria_virtual, ultima_pos)

                if espID == 3:
                    gerencia_memoria(tempo_inicio, lista_processos, memoria_virtual, None, dic_tamanhos_fixos)

                if espID != 3:
                    simula_processos(tempo_inicio, lista_paginas, lista_processos, tabela_paginas, memoria_virtual, memoria_fisica, subsID)
                else:
                    simula_processos(tempo_inicio, lista_paginas, lista_processos, tabela_paginas, memoria_virtual, memoria_fisica, subsID, dic_tamanhos_fixos)

                if i % int(comandos[1]) == 0:
                    print("Memória Física:")
                    livre_fisica = memoria_fisica.quantidade_livre()
                    ocupada_fisica = total - livre_fisica
                    print("Livre: " + str(livre_fisica) + "/" + str(total))
                    print("Memória Virtual:")
                    livre_virtual = memoria_virtual.quantidade_livre()
                    ocupada_virtual = virtual - livre_virtual
                    print("Livre: " + str(livre_virtual) + "/" + str(virtual) + "\n")
                    print(memoria_virtual)

                sleep(1)
                i += 1
