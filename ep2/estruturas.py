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
        len_final_mem = (len(str(self.inicio_mem + self.tamanho_mem - 1)) + 2)

        if self.livre:
            len_nome_proc = 7
            nome = "Livre"

        descricao += " " + len_nome_proc * "_"
        descricao += " " + len_inicio_mem * "_"
        descricao += " " + len_final_mem * "_" + " _\n"
        descricao += "|" + len_nome_proc * " "
        descricao += "|" + len_inicio_mem * " "
        descricao += "|" + len_final_mem * " " + "| |\n"
        descricao += "| " + nome + " "
        descricao += "| " + str(self.inicio_mem) + " "
        descricao += "| " + str(self.inicio_mem + self.tamanho_mem - 1)
        descricao += " |--->\n"
        descricao += "|" + len_nome_proc * "_"
        descricao += "|" + len_inicio_mem * "_"
        descricao += "|" + len_final_mem * "_" + "|_|\n"

        return descricao


class Lista:
    """
    Representa uma lista ligada para gerenciar memória livre. Cada item da lista
    é uma instância da classe Item. As instâncias da lista contêm uma referência
    para o primeiro item da lista.
    """

    inicio = None
    __iter_atual = None

    def __init__(self, inicio):
        self.inicio = inicio
        inicio.prox = None
        inicio.ant = None
        self.__iter_atual = inicio

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__iter_atual:
            raise StopIteration
        atual = self.__iter_atual
        self.__iter_atual = self.__iter_atual.prox
        return atual

    def __str__(self):
        descricao = ""
        for item in self:
            descricao += str(item)
        return descricao + "\nFim da lista\n"

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
                if item.prox:
                    #Caso que a celula está no meio de duas células livres
                    if (item.ant.livre and item.prox.livre):
                        item.ant.tamanho_mem = item.ant.tamanho_mem + item.tamanho_mem + item.prox.tamanho_mem
                        if item.prox.prox:
                            item.prox.prox.ant = item.ant
                            item.ant.prox = item.prox.prox
                        else:
                            item.ant.prox = None
                        break
                    #Caso que a anterior é livre
                    if item.ant.livre:
                        item.ant.tamanho_mem = item.ant.tamanho_mem + item.tamanho_mem
                    #Caso que a proxima é livre
                    elif item.prox.livre:
                        item.prox.tamanho_mem = item.tamanho_mem + item.prox.tamanho_mem
                        item.prox.inicio_mem = item.inicio_mem
                    item.ant.prox = item.prox
                    item.prox.ant = item.ant
                else:
                    if item.ant.livre:
                        item.ant.tamanho_mem = item.ant.tamanho_mem + item.tamanho_mem
                    item.ant.prox = None
                break


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

    def __init__(self, nome, t0, tf, b, acessos):
        self.nome = nome
        self.t0 = t0
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
