class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val
    
    def insertLeft(self,n):
        self.l = n

    def insertRight(self,n):
        self.r = n

#No recomiendo esto, pero en el Automata uno puede poner cualquier tipo de valor, pero casi todos
#suelen ser del mismo tipo, sin importar si es AFN o AFD, pero estadosFinales es un string para AFN
#y para AFD llega a ser una lista. Por ello hay 2 funciones que crean para crear los estados finales
#del AFD, porque se le pasa una lista pare crearlo o una string.
class Automata:
    def __init__(self, estIn, estFin, states, alfabeth, transitions, name = ""):
        self.estadoInicial = estIn
        self.estadosFinales = estFin
        self.estados = states
        self.alfabeto = alfabeth
        self.transiciones = transitions
        self.nombre = name

    

