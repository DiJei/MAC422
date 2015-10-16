#-------------------------------------#
#               util.py               #
#-------------------------------------#
#    Arqivo com funções auxiliares    #
#-------------------------------------#
from estruturas import *
from espacolivre import *
from substituipaginas import *
from struct import *
from time import *

# Função que abre o arquivo com nome dentro da string nome
def abre_arquivo(nome):
    try:
        trace = open(nome, "r")
        return trace
    except IOError:
        print ("Erro na abertura do arquivo")
        return 0


# Função para montar a lista de processos, com as informações do arquivo trace
def monta_lista_processos(trace):
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
        lista.append(processo)

        linha = trace.readline()
        pid += 1

    return lista


# Função que verifica se todos os processos terminaram (True) ou não (False)
def processos_terminaram(lista_processos):
    for processo in lista_processos:
        if not processo.terminou:
            return False
    return True


"""
Função que gerencia a memória, alocando processos em espaços livres quando eles
chegam de acordo com o algoritmo escolhido pelo usuário. A alocação é na memória
física e o arquivo que representa a memória é atualizado no final da função.
"""
def gerencia_memoria(tempo_inicio, lista_processos, mem_virtual, ultima_pos=None, dic_tamanhos_fixos=None):
    for processo in lista_processos:
        tempo_atual = time() - tempo_inicio

        if tempo_atual >= processo.t0 and not processo.rodando and not processo.terminou:
            # argumentos sinalizam qual o algoritmo sendo usado

            if ultima_pos is None and dic_tamanhos_fixos is None:
                first_fit(mem_virtual, processo)

            elif dic_tamanhos_fixos is None:
                ultima_pos = next_fit(mem_virtual, processo, ultima_pos)

            elif ultima_pos is None:
                quick_fit(mem_virtual, processo, dic_tamanhos_fixos)
                atualiza_dic_tamanhos_fixos(mem_virtual, dic_tamanhos_fixos)

    escreve_na_memoria(mem_virtual, False)
    if ultima_pos is not None and dic_tamanhos_fixos is None:   # Next Fit precisa devolver posição
        return ultima_pos



"""
Função que simula os processos em execução, fazendo com que os acessos à
memória física que eles fazem ocorram quando for o tempo certo e chamando, se
necessário (quando ocorre page fault) a função que gerencia as páginas (usa os
algoritmos de substituição de páginas). Também remove os processos das memórias
se chega o tempo em que eles terminam e atualiza constantemente os arquivos que
representam as memórias.
"""
def simula_processos(tempo_inicio, lista_paginas, lista_processos, tabela_paginas, mem_virtual, mem_fisica, subs, dic_tamanhos_fixos=None):
    if subs == 4:
        # atualiza contador para o LRU
        for pagina in lista_paginas:
            tabela_paginas.contador[pagina] += tabela_paginas.acessos[pagina]

    for processo in lista_processos:
        tempo_atual = time() - tempo_inicio

        for acesso in processo.acessos:
            if tempo_atual >= acesso.instante and not acesso.ocorreu:
                processo_mem_virt = mem_virtual.localiza(processo.nome)
                if processo_mem_virt:
                    posicao_virtual = processo_mem_virt.inicio_mem + acesso.posicao

                posicao_fisica = tabela_paginas.tabela[int(posicao_virtual / 16)]
                if posicao_fisica is None:
                    # Page Fault
                    gerencia_paginas(lista_paginas, tabela_paginas, posicao_virtual, processo, mem_fisica, subs)
                acesso.ocorreu = True

                # atualiza bit R
                tabela_paginas.acessos[int(posicao_virtual / 16)] = 1

                escreve_na_memoria(mem_fisica, True)

        if tempo_atual >= processo.tf and processo.rodando:
            libera_paginas(tabela_paginas, lista_paginas, mem_virtual, processo)
            mem_virtual.remove(processo.nome)
            mem_fisica.remove(processo.nome)
            processo.rodando = False
            processo.terminou = True

            # se está usando o Quick Fit, atualiza dicionário
            if dic_tamanhos_fixos is not None:
                atualiza_dic_tamanhos_fixos(mem_virtual, dic_tamanhos_fixos)

            escreve_na_memoria(mem_fisica, True)

    escreve_na_memoria(mem_virtual, False)


"""
Função que remove da lista de páginas na memória física e da tabela de páginas
as páginas de um processo que terminou.
"""
def libera_paginas(tabela_paginas, lista_paginas, mem_virtual, processo):
    end_virt = mem_virtual.localiza(processo.nome)
    for pagina in range(end_virt.inicio_mem, end_virt.inicio_mem + end_virt.tamanho_mem, 16):
        tabela_paginas.tabela[int(pagina / 16)] = None
        if int(pagina / 16) in lista_paginas:
            lista_paginas.remove(int(pagina / 16))


"""
Função que gerencia páginas, alocando uma página na memória física se houver
espaço livre e chamando o algoritmo de substituição de páginas especificado
se não houver.
"""
def gerencia_paginas(lista_paginas, tabela_paginas, posicao_virtual, processo, mem_fisica, subs):
    for pedaco in mem_fisica:
        if pedaco.livre and pedaco.tamanho_mem >= 16:
            tabela_paginas.tabela[int(posicao_virtual / 16)] = int(pedaco.inicio_mem / 16)
            pagina = Processo(processo.t0, processo.nome, processo.pid, processo.tf, 16, processo.acessos)
            aloca(mem_fisica, pedaco.inicio_mem, pagina)
            lista_paginas.append(int(posicao_virtual / 16))
            return

    # nenhum espaço livre na memória física
    # chama algoritmo de substituição de página escolhido
    if subs == 1:
        not_recently_used_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)
    if subs == 2:
        first_in_first_out(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)
    if subs == 3:
        second_chance_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)
    if subs == 4:
        least_recently_used_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)


"""
Função que recebe uma lista representando o estado atual da memória (física ou
virtual) e escreve, de forma binária, em /tmp/ep2.mem (física) ou /tmp/ep2.vir
(virtual) esse estado, representando bytes ocupados por processos com o número
(PID) do processo e bytes livres com o número 255
"""
def escreve_na_memoria(lista, principal):
    mem = b""
    for item in lista:
        tamanho = item.tamanho_mem
        if item.livre:
            mem += pack('B' * tamanho, *([255] * tamanho))
        else:
            mem += pack('B' * tamanho, *([item.proc_id] * tamanho))
    if principal:
        arq = "/tmp/ep2.mem"
    else:
        arq = "/tmp/ep2.vir"
    with open(arq, 'wb') as memoria:
        memoria.write(mem)
        memoria.close()
