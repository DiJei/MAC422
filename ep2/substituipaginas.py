def substitui_pagina(quadro_pagina, tabela_paginas, processo, num_pagina_antiga, num_pagina_nova, num_quadro_pagina, lista_paginas):
    quadro_pagina.proc_nome = processo.nome
    quadro_pagina.proc_id = processo.pid

    tabela_paginas.tabela[num_pagina_antiga] = None
    tabela_paginas.tabela[num_pagina_nova] = num_quadro_pagina

    print("vou remover", num_pagina_antiga)
    lista_paginas.remove(num_pagina_antiga)
    lista_paginas.append(num_pagina_nova)
    print("adicionei", num_pagina_nova)


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


def first_in_first_out(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica):
    num_quadro_pagina = tabela_paginas.tabela[lista_paginas[0]]
    num_pagina_antiga = lista_paginas[0]
    num_pagina_nova = int(posicao_virtual / 16)

    quadro_pagina = mem_fisica.pedaco_na_pagina(num_quadro_pagina)
    substitui_pagina(quadro_pagina, tabela_paginas, processo, num_pagina_antiga, num_pagina_nova, num_quadro_pagina, lista_paginas)


def second_chance_page(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica):
    while tabela_paginas.acessos[lista_paginas[0]] != 0:
        print("dando segunda chance pra", lista_paginas[0], "")
        tabela_paginas.acessos[lista_paginas[0]] = 0
        comeco_lista = lista_paginas[0]
        lista_paginas.remove(comeco_lista)
        lista_paginas.append(comeco_lista)

    first_in_first_out(processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica)


def least_recently_used (processo, lista_paginas, posicao_virtual, tabela_paginas, mem_fisica, matriz):
   """
   basicamente apenas escolhe a linha com menor numero binario para ser retirada, isso implica que a medida que
   as paginas forem referenciadas é necessário atualiza a matriz_acesso usando metodo acesso_de_quadro 
   """
   menor = matriz.menor_quadro()
   print(menor," menor")
   num_quadro_pagina =  (menor - 1)
   num_pagina_antiga = lista_paginas[menor - 1]
   num_pagina_nova = int(posicao_virtual / 16)
   quadro_pagina = mem_fisica.pedaco_na_pagina(num_quadro_pagina)
   substitui_pagina(quadro_pagina, tabela_paginas, processo, num_pagina_antiga, num_pagina_nova, num_quadro_pagina, lista_paginas)