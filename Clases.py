class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val
    
    def insertLeft(self,n):
        self.l = n

    def insertRight(self,n):
        self.r = n

class AFN:

    def __init__(self, estIn, estFin, states, alfabeth, transitions):
        self.estadoInicial = estIn
        self.estadoFinal = estFin
        self.estados = states
        self.alfabeto = alfabeth
        self.transiciones = transitions

    

