import re


class Node:
    def __init__(self, sim, val = None):
        self.parent = None
        self.leftNode = None
        self.rightNode = None
        self.leftList = []
        self.rigthList = []
        self.s = sim
        self.v = val

    def insertParent(self, p):
        self.parent = p
    
    def insertLeft(self,n):
        self.leftNode = n

    def insertRight(self,n):
        self.rightNode = n

    def insertVal(self, val):
        self.v = val

    def getLeftNode(self):
        return self.leftNode

    def getRightNode(self):
        return self.rightNode

    def getSimbol(self):
        return self.s
    
    def getVal(self):
        return self.v

    def nullable(self):
        if self.s == "ε" or self.s == "*" or self.s == "?":
            return True
        else:
            return False


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

    

