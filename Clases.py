import re


class Node:
    def __init__(self, sim, val = None):
        self.leftNode = None
        self.rightNode = None
        self.leftList = []
        self.rightList = []
        self.s = sim
        self.v = val
        #print(str(val) + str(sim))
        self.setLists()

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
    
    def firstPos(self):
        return self.leftList

    def lastPos(self):
        return self.rightList

    def nullable(self, simbol):
        if simbol == "ε" or simbol == "*" or simbol == "?":
            return True
        else:
            return False
    
    def setLists(self):
        if self.getVal() != None:
            self.leftList.append(self.getVal())
            self.rightList.append(self.getVal())

    def setfirstAndlast(self):
        if self.getSimbol() == "|":
            self.leftList = self.rightNode.firstPos() + self.leftNode.firstPos()
            self.rightList = self.leftList
        if self.getSimbol() == "*" or self.getSimbol() == "?":
            self.leftList = self.rightNode.firstPos()
            self.rightList = self.leftList
        if self.getSimbol() == "ʚ":
            if self.nullable(self.leftNode.getSimbol()):
                self.rightList = self.rightNode.lastPos() + self.leftNode.firstPos()
            else:
                self.rightList = self.leftNode.firstPos()

            if self.nullable(self.rightNode.getSimbol()):
                self.leftList = self.rightNode.lastPos() + self.leftNode.lastPos()
            else:
                self.leftList = self.rightNode.firstPos()

        







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

    

