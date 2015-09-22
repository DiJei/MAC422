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

    def __init__(self, livre, proc_id, inicio_mem, tamanho_mem):
        self.livre = livre
        self.proc_id = proc_id
        self.inicio_mem = inicio_mem
        self.tamanho_mem = tamanho_mem

    def __str__(self):
        descricao = "Espaço "
        if self.livre:
            descricao += "livre"
        else:
            descricao += ("ocupado pelo processo " + str(self.proc_id) +
                          " a partir da posição " + str(self.inicio_mem) +
                          " até a " + str(self.inicio_mem + self.tamanho_mem))

        return descricao


class Lista:
    """
    Representa uma lista ligada para gerenciar memória livre. Cada item da lista
    é uma instância da classe Item. As instâncias da lista contêm uma referência
    para o primeiro item da lista e uma para o último.
    """

    inicio = None
    final = None

    def __init__(self, inicio):
        self.inicio = inicio
        self.final = inicio
        inicio.prox = None

    def adiciona_depois_de(self, item, novo_item):
        novo_item.prox = item.prox
        item.prox = novo_item

    def remove_depois_de(self, item):
        item.prox = item.prox.prox
