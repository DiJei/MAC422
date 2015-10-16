#--------------------------------------------#
#            substituipaginas.py             #
#--------------------------------------------#
#   Algoritmos de substituição de página     #
#--------------------------------------------#


"""
Faz a substituição de uma página por outra, atualizando tanto a tabela de
páginas quanto a lista de páginas na memória física. Precisa saber o número das
páginas nova e antiga e do quadro de página em que vai acontecer a substituição
e o pedaço de memória no qual está esse quadro.
"""
def substitui_pagina(quadro_pagina, tabela_paginas, processo, num_pagina_antiga, num_pagina_nova, num_quadro_pagina, lista_paginas):
    quadro_pagina.proc_nome = processo.nome
    quadro_pagina.proc_id = processo.pid

    tabela_paginas.tabela[num_pagina_antiga] = None
    tabela_paginas.tabela[num_pagina_nova] = num_quadro_pagina

    print("vou remover", num_pagina_antiga)
    lista_paginas.remove(num_pagina_antiga)
    lista_paginas.append(num_pagina_nova)
    print("adicionei", num_pagina_nova)


"""
Algoritmo que divide as páginas na memória física em duas classes (0 e 1)
determinadas pelo estado do bit R da página. Substitui preferencialmente uma
página da classe 0, mas, se não houver nenhuma, uma da classe 1.
"""
def not_recently_used_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica):
    classe0 = []
    classe1 = []

    for pagina in lista_paginas:
        if tabela_paginas.acessos[pagina] == 0:
            classe0.append(pagina)
        else:
            classe1.append(pagina)

    if classe0:
        num_pagina_antiga = classe0[0]
        print("vou tirar", classe0[0], "da classe 0")
    else:
        num_pagina_antiga = classe1[0]
        print("vou tirar", classe1[0], "da classe 1")

    num_pagina_nova = int(posicao_virtual / 16)
    num_quadro_pagina = tabela_paginas.tabela[num_pagina_antiga]
    quadro_pagina = mem_fisica.pedaco_na_pagina(num_quadro_pagina)

    substitui_pagina(quadro_pagina, tabela_paginas, processo, num_pagina_antiga, num_pagina_nova, num_quadro_pagina, lista_paginas)
    print("adicionei", num_pagina_nova)


"""
Algoritmo que escolhe para ser substituída a página que está há mais tempo na
memória física (a primeira da lista de páginas na memória física, que é
ordenada por tempo de chegada.
"""
def first_in_first_out(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica):
    num_quadro_pagina = tabela_paginas.tabela[lista_paginas[0]]
    num_pagina_antiga = lista_paginas[0]
    num_pagina_nova = int(posicao_virtual / 16)

    quadro_pagina = mem_fisica.pedaco_na_pagina(num_quadro_pagina)
    substitui_pagina(quadro_pagina, tabela_paginas, processo, num_pagina_antiga, num_pagina_nova, num_quadro_pagina, lista_paginas)


"""
Algoritmo que olha para a página que está há mais tempo na memória física e, se
o bit R dela for 0, a substitui como no FIFO, mas, se ele for 1, muda o bit
para 0, põe a página no final da lista de páginas na memória física e repete o
procedimento para a próxima página no começo da lista.
"""
def second_chance_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica):
    while tabela_paginas.acessos[lista_paginas[0]] != 0:
        print("dando segunda chance pra", lista_paginas[0], "")
        tabela_paginas.acessos[lista_paginas[0]] = 0
        comeco_lista = lista_paginas[0]
        lista_paginas.remove(comeco_lista)
        lista_paginas.append(comeco_lista)

    first_in_first_out(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)


"""
Algoritmo que usa um contador associado a cada página, que é incrementado de um
em um segundo com o valor do bit R daquela página. O algoritmo escolhe para ser
substituída a página com o menor valor no contador.
"""
def least_recently_used_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica):
    menor = [-1, -1]    # valor do contador e página, respectivamente
    for pagina in lista_paginas:
        if tabela_paginas.contador[pagina] < menor[0] or menor[0] == -1:
            menor[0] = tabela_paginas.contador[pagina]
            menor[1] = pagina

    num_quadro_pagina = tabela_paginas.tabela[menor[1]]
    num_pagina_antiga = menor[1]
    num_pagina_nova = int(posicao_virtual / 16)
    quadro_pagina = mem_fisica.pedaco_na_pagina(num_quadro_pagina)
    # print('contadores:')
    # for pagina in lista_paginas:
    #     print(pagina, tabela_paginas.contador[pagina])
    substitui_pagina(quadro_pagina, tabela_paginas, processo, num_pagina_antiga, num_pagina_nova, num_quadro_pagina, lista_paginas)
