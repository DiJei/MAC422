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

    def __init__(self, inicio):
        self.inicio = inicio
        inicio.prox = None
        inicio.ant = None

    def __str__(self):
        descricao = ""
        if self.inicio:
            descricao += str(self.inicio)
        item = self.inicio.prox
        while item:
            descricao += str(item)
            item = item.prox
        descricao += "\nFim da lista\n"
        return descricao

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
        temp = self.inicio
        while temp:
            if temp.proc_nome == nome:
                if temp.prox:
                    #Caso que a celula está no meio de duas células livres
                    if (temp.ant.livre and temp.prox.livre):
                        temp.ant.tamanho_mem = temp.ant.tamanho_mem + temp.tamanho_mem + temp.prox.tamanho_mem
                        if temp.prox.prox:
                            temp.prox.prox.ant = temp.ant
                            temp.ant.prox = temp.prox.prox
                        else:
                            temp.ant.prox = None
                        break
                    #Caso que a anterior é livre
                    if temp.ant.livre:
                        temp.ant.tamanho_mem = temp.ant.tamanho_mem + temp.tamanho_mem
                    #Caso que a proxima é livre
                    elif temp.prox.livre:
                        temp.prox.tamanho_mem = temp.tamanho_mem + temp.prox.tamanho_mem
                        temp.prox.inicio_mem = temp.inicio_mem
                    temp.ant.prox = temp.prox
                    temp.prox.ant = temp.ant
                else:
                    if temp.ant.livre:
                        temp.ant.tamanho_mem = temp.ant.tamanho_mem + temp.tamanho_mem
                    temp.ant.prox = None
                break
            temp = temp.prox


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
