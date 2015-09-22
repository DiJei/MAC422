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
     print "Erro na abertura do arquivo"
     return 0
#Funcao que comeca simulacao ja com parametros certos
def  simulationStart(delay,espID,subsID):
    #Calma jose, tamo fazendo
	return 0