#-------------------------------------#
#               util.py               #
#-------------------------------------#
#    Arqivo com funcoes auxiliares    #
#-------------------------------------#

#Abre o arquivo com nome dentro da string filename
def openFile(filename):
   try:
     trace = open(filename, "r")
     return trace
   except IOError:
     print ("Erro na abertura do arquivo")
     return 0
#Funcao para montar a lista de processos, com as informcoes do arquivo trace
def listaProcessosBuild(trace):
   from estruturas import Processo
   lista = []
   line = trace.readline()
   while line:
     temp = line.split(" ")
     acesso = []
     for x in range(4, len(temp),2):
       acess = (temp[x],temp[x + 1])
       acesso.append(acess)
     processo = Processo(temp[1],temp[0],temp[2],temp[3],acesso)
     lista.append(processo)
     line = trace.readline()
   return lista
#Funcao que comeca simulacao ja com parametros certos
def  simulationStart(delay,espID,subsID):
   #Calma jose, tamo fazendo
   return 0