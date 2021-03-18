class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val
    
    def insertLeft(self,n):
        self.l = n

    def insertRight(self,n):
        self.r = n

def printTree(node, level=0):
    if node != None:
        printTree(node.l, level + 1)
        print(' ' * 4 * level + '->', node.v)
        printTree(node.r, level + 1)
    
