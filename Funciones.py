import re
import Clases
def validadExpresion(expresion):
    try:
        re.compile(expresion)
        esValido = True
    except re.error:
        esValido = False
    return esValido

def procesandoAlfabeto(expresion,alfabeto, metaCaracteres):
    alfabeto = list(set(expresion))
    print("su alfabeto con todos los simbolos unicos de la expresion son los siguiente: " + str(alfabeto))
    #con la siguiente linea eliminamso todos los metaCaracteres y dejamos solo los simbolos de la expresion regular
    alfabeto = [e for e in alfabeto if e not in metaCaracteres]
    if ("ε" in alfabeto):
        pass
    else:
        alfabeto.insert(0,"ε")
    #vamos a añadir el operador de concatenacion
    for y in range(0,len(expresion)):
        try:
            if((expresion[y] in alfabeto or expresion[y] == "+" or expresion[y] == "*" or expresion[y] == "?" or expresion[y] == ")") and (expresion[y+1] in alfabeto or expresion[y+1] == "(")):
                parte1 = expresion[:y+1]
                parte2 = expresion[y+1:]
                expresion = parte1 + "." +parte2
                #demo = parte1 + "." +parte2
                #print(demo)
        except:
            pass
    return alfabeto, expresion

#Código para expresiones regulare de Infija a Postfija
def infijoAPosfix(expresion,alfabeto):
    expresionPosfix = []
    pila = ['n']
    for i in expresion:
        if (i in alfabeto):
            expresionPosfix.append(i) 
        else:
            if (pila == [] or pila[-1] == "(" or i == "("):
                pila.append(i) 
            elif (i == "+" or i == "*" or i == "?"):
                if (pila[-1] == "+" or pila[-1] == "*" or pila[-1] == "?"):
                    expresionPosfix.append(i)
                    #pila.append(i)
                else:
                    pila.append(i)
            elif i == ".":
            #print "len(pila)"
            #print len(pila)
                while (pila[-1] == "+" or pila[-1] == "*" or pila[-1] == "?") :
                    expresionPosfix.append(pila.pop())
                    #print len(pila)
                if (pila[-1] == "."):
                    expresionPosfix.append(i)
                else:
                    pila.append(i)
            elif(i == "|"):
                #print "len(pila)"
                #print len(pila)
                while (pila[-1] == "+" or pila[-1] == "*" or pila[-1] == "?" or pila[-1] == "."):
                    expresionPosfix.append(pila.pop())
                    #print len(pila)
                if (pila[-1] == "|"):
                    expresionPosfix.append(i)
                else:
                    pila.append(i)
            elif(i == ")"):
                while pila[-1] != "(":
                    expresionPosfix.append(pila.pop())
                pila.pop()
        #print(str(pila) + "   " + str(expresionPosfix))
    while len(pila) > 1:
        expresionPosfix.append(pila.pop())
    return expresionPosfix

def crearArbol(expresionPosfix, alfabeto, operadores):
    pila = []
    for i in expresionPosfix:
        #print(i)
        if (i in alfabeto):
            leaf = Clases.Node(i)
            #print(i)
            pila.append(leaf)
        elif (i in operadores and i != "*" and i != "+" and i != "?"):
            leaf = Clases.Node(i)
            L1 = pila.pop()
            #print(L1.v)
            L2 = pila.pop()
            #print(L2.v)
            leaf.insertLeft(L1)
            leaf.insertRight(L2)
            pila.append(leaf)
        elif( i == "*" or i == "+" or i == "?"):
            leaf = Clases.Node(i)
            L1 = pila.pop()
            #print(L1.v)
            leaf.insertLeft(L1)
            pila.append(leaf)
    return pila.pop()

def printTree(node, level=0):
    if node != None:
        printTree(node.l, level + 1)
        print(' ' * 4 * level + '->', node.v)
        printTree(node.r, level + 1)