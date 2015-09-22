from struct import *

tamanho = int(input("qual é o tamanho?\n"))

# converte array de -1s de tamanho tamanho em string binaria (em hexadecimal)
# correspondente (1 byte por numero) e depois escreve isso no arquivo
str = pack('b' * tamanho, *([-1] * tamanho))
with open('arq', 'wb') as arq:
    arq.write(str)
    arq.close()
