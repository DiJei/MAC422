
class Item:
    """
    Representa um item de uma lista ligada para gerenciar memória livre.
    Guarda informações dizendo se o pedaço de memória representado pelo item
    está livre ou sendo usado por um processo, qual o processo que está usando
    ele (se algum estiver), e onde começa e qual o tamanho do pedaço de memória.
    Além disso, guarda uma referência para o próximo item da lista (ou None se
    esse item é o último).
    """

    prox = None
    ant = None
    proc_id = -1

    def __init__(self, livre, proc_nome, inicio_mem, tamanho_mem):
        self.livre = livre
        self.proc_nome = proc_nome
        self.inicio_mem = inicio_mem
        self.tamanho_mem = tamanho_mem

    def __str__(self):
        descricao = ""
        nome = self.proc_nome
        len_nome_proc = len(self.proc_nome) + 2
        len_inicio_mem = (len(str(self.inicio_mem)) + 2)
        len_tamanho_mem = (len(str(self.tamanho_mem)) + 2)

        if self.livre:
            len_nome_proc = 7
            nome = "Livre"

        descricao += " " + len_nome_proc * "_"
        descricao += " " + len_inicio_mem * "_"
        descricao += " " + len_tamanho_mem * "_" + " _\n"
        descricao += "|" + len_nome_proc * " "
        descricao += "|" + len_inicio_mem * " "
        descricao += "|" + len_tamanho_mem * " " + "| |\n"
        descricao += "| " + nome + " "
        descricao += "| " + str(self.inicio_mem) + " "
        descricao += "| " + str(self.tamanho_mem)
        descricao += " |--->\n"
        descricao += "|" + len_nome_proc * "_"
        descricao += "|" + len_inicio_mem * "_"
        descricao += "|" + len_tamanho_mem * "_" + "|_|\n"

        return descricao


class Lista:
    """
    Representa uma lista ligada para gerenciar memória livre. Cada item da lista
    é uma instância da classe Item. As instâncias da lista contêm uma referência
    para o primeiro item da lista.
    """

    inicio = None

    def __init__(self, inicio):
        self.inicio = inicio
        inicio.prox = None
        inicio.ant = None
        self.__iter_atual = inicio

    def __iter__(self):
        return self.gen()

    def gen(self):
        atual = self.inicio
        while atual:
            yield atual
            atual = atual.prox

    def __str__(self):
        descricao = ""
        for item in self:
            descricao += str(item)
        return descricao + "\nFim da lista\n"

    def fragmenta(self, posicao):
        # assume que a posição recebida como argumento vai ser sempre uma
        # posição no meio de um pedaço de memória na lista e cria um novo
        # pedaço começando nessa posição
        pedaco = self.pedaco_na_posicao(posicao)
        tamanho_novo = pedaco.tamanho_mem + pedaco.inicio_mem - posicao
        novo_pedaco = Item(pedaco.livre, pedaco.proc_nome, posicao, tamanho_novo)
        pedaco.tamanho_mem = posicao - pedaco.inicio_mem
        self.adiciona_depois_de(pedaco, novo_pedaco)

    def localiza(self, nome):
        for item in self:
            if item.proc_nome == nome:
                return item
        return None

    def pedaco_na_posicao(self, posicao):
        for item in self:
            if item.inicio_mem <= posicao < item.inicio_mem + item.tamanho_mem:
                return item
        return None

    def pedaco_na_pagina(self, pagina):
        for item in self:
            if int(item.inicio_mem / 16) == pagina:
                return item
        return None

    def adiciona_depois_de(self, item, novo_item):
        novo_item.prox = item.prox
        novo_item.ant = item
        item.prox = novo_item

    def remove_depois_de(self, item):
        if item.prox:
            if item.prox.prox:
                item.prox.prox.ant = item
            item.prox = item.prox.prox

    """
    Remove o processo com nome nome e já atualiza a lista juntando espaços
    em branco (se for o caso).
    """
    def remove(self, nome):
        for item in self:
            if item.proc_nome == nome:

                if self.inicio is item:
                    if item.prox and item.prox.livre:
                        self.inicio = item.prox
                        self.inicio.ant = None

                if item.prox and item.ant:
                    #Caso que a celula está no meio de duas células livres
                    if (item.ant.livre and item.prox.livre):
                        item.ant.tamanho_mem = item.ant.tamanho_mem + item.tamanho_mem + item.prox.tamanho_mem
                        if item.prox.prox:
                            item.prox.prox.ant = item.ant
                            item.ant.prox = item.prox.prox
                        else:
                            item.ant.prox = None
                        continue
                if item.ant:
                    #Caso que a anterior é livre
                    if item.ant.livre:
                        item.ant.tamanho_mem = item.ant.tamanho_mem + item.tamanho_mem
                        item.ant.prox = item.prox
                        if item.prox:
                            item.prox.ant = item.ant
                        continue
                if item.prox:
                    #Caso que a proxima é livre
                    if item.prox.livre:
                        item.prox.tamanho_mem = item.tamanho_mem + item.prox.tamanho_mem
                        item.prox.inicio_mem = item.inicio_mem
                        if item.ant:
                            item.ant.prox = item.prox
                            item.prox.ant = item.ant
                        continue

                item.livre = True
                item.proc_nome = ""
                item.proc_id = -1


class Processo:
    """
    Representa um processo que vai rodar no sistema. Inclui o nome do processo,
    o instante de tempo em que chegou (t0), o instante de tempo em que termina
    (tf), quanto usa de memória em bytes (b), uma flag representando se o
    processo está rodando ou não, outra flag representando se ele já terminou
    ou não e uma lista de instâncias da classe Acesso contendo informações
    sobre acesso à memória (onde, quando, já acessou)
    """

    rodando = False
    terminou = False

    def __init__(self, t0, nome, pid, tf, b, acessos):
        self.t0 = t0
        self.nome = nome
        self.pid = pid
        self.tf = tf
        self.b = b
        self.acessos = acessos

    def __str__(self):
        descricao = self.nome + " chega no instante " + str(self.t0) + "s e "
        descricao += "acaba no instante " + str(self.tf) + ", ocupa "
        descricao += str(self.b) + " bytes; acessos à memória:\n"

        for acesso in self.acessos:
            descricao += str(acesso) + "\n"
        return descricao


class Acesso:
    """
    Representa um acesso a uma posição de memória, contendo informações sobre
    qual a posição de memória acessada, o instante de tempo em que esse acesso
    ocorre e se ele já ocorreu ou ainda não
    """

    ocorreu = False

    def __init__(self, posicao, instante):
        self.posicao = posicao
        self.instante = instante

    def __str__(self):
        descricao = "Acesso à memória na posição " + str(self.posicao)
        descricao += " aos " + str(self.instante) + "s"
        return descricao


class TabelaPagina:
    """
    Tabela de paginas, basicamente um dicionário cuja as chaves são
    as paginas e quadros de paginas são valores.
    """
    paginas = 0
    tabela = []     # o índice é a página, o valor é o quadro
    acessos = []    # cada posição representa o bit R da respectiva página

    def __init__(self, virtual):
        self.paginas = int(virtual / 16)   # Quantidade de paginas
        for x in range(self.paginas):
            self.tabela.append(None)
            self.acessos.append(0)

    def map(self, endereco_virtual):
        pagina = int(endereco_virtual / 16)
        quadro = self.tabela[pagina]

        return quadro

    def reseta_acessos(self):
        self.acessos = [0 for pagina in self.acessos]

"""
 Matriz para implementacao do algoritmo de substituicao de pagina LRU
"""
import numpy as np
class MatrizAcessos:
    matriz = None
    size = 0
    def __init__(self,num_qaudros):
       self.matriz = np.zeros((num_qaudros * num_qaudros), dtype = np.uint8)
       self.matriz = np.reshape(self.matriz,(num_qaudros,num_qaudros))
       self.size = self.matriz.shape[0]
    """
    recebe o numero de quadro e coloca 1 na linha k
    e zera coluna k 
    """
    def acesso_quadro(self,k):  #observacao o a contagem da pagina dos quadros comeca do 1
       k = k -1
       self.matriz[k] =  1
       self.matriz[0:self.size, k:k+1:1] =   self.matriz[0:self.size, k:k+1:1] * 0
       #print( self.size)
    """
    devolve a linha que possui o menor numero binário
    """
    def menor_quadro(self):
        temp = 0
        menor_bin = 0 
        aux = 1
        linha = 0
        #alguma coisa
        for x in range(0,self.size):
           menor_bin += aux * self.matriz[0][self.size - 1 - x]
           aux *= 10  
        for x in range(1,self.size):
           aux = 1
           temp = 0
           for y in range(0,self.size):
              temp += aux * self.matriz[x][self.size - 1 - y]
              aux *= 10
           if menor_bin > temp:
              menor_bin = temp
              linha = x 
        return linha + 1