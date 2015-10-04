""" ARQUIVO TEMPORARIO DE PARA TESTES """
from estruturas import *

i1 = Item(True, '', 0, 100)
i2 = Item(False, 'p1', 100, 100)
i3 = Item(False, 'p2', 200, 100)
i4 = Item(True, '', 300, 100)
i5 = Item(False, 'p3', 400, 100)

a1 = Acesso(0, 7)
a2 = Acesso(7, 10)
a3 = Acesso(10, 15)
a4 = Acesso(100, 20)
a5 = Acesso(200, 30)
a6 = Acesso(202, 60)
a7 = Acesso(333, 120)

acessos1 = [a1, a2, a3, a4]
acessos2 = [a5, a6, a7]

proc1 = Processo(0, "Proc1", 100, 1024, acessos1)
proc2 = Processo(120, "Proc2", 500, 16384, acessos2)

lista = Lista(i1)
lista.adiciona_depois_de(lista.inicio, i2)
lista.adiciona_depois_de(lista.inicio.prox, i3)
lista.adiciona_depois_de(lista.inicio.prox.prox, i4)
lista.adiciona_depois_de(lista.inicio.prox.prox.prox, i5)

print("lista:", lista, sep="\n")
print("processo 1:", proc1, sep="\n")
print("processo 2:", proc2, sep="\n")
lista.remove("p3")
print("lista:", lista, sep="\n")
lista.remove("p2")
print("lista:", lista, sep="\n")
lista.remove("p1")
print("lista:", lista, sep="\n")
