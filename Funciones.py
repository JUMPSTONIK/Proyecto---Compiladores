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
    tamaño = len(expresion) * 2
    for y in range(0, tamaño):
        try:
            if((expresion[y] in alfabeto or expresion[y] == "+" or expresion[y] == "*" or expresion[y] == "?" or expresion[y] == ")") and (expresion[y+1] in alfabeto or expresion[y+1] == "(")):
                parte1 = expresion[:y+1]
                parte2 = expresion[y+1:]
                expresion = parte1 + "." +parte2
                demo = parte1 + "." +parte2
                print(demo)
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

def Thompson(expresionPosfix, alfabeto, operadores):
    estadoInicial = "q0"
    estadoFinal = ""
    estados = ["q0"]
    transiciones = {}
    transicionesPila = []
    estadosPila = []
    inicialesPila = []
    finalesPila = []
    cont = 1
    cont2 = 0
    for i in expresionPosfix:
        #print(i)
        if (i in alfabeto):
            #print(i)
            transicionesPila.append(i)
            #pila.append()
            print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
        else:
            if(i == "*"):
                if(estadoFinal == ""):
                    for x in range(cont, cont+3):
                        estadosPila.append("q" + str(cont))
                        cont+= 1
                    transiciones[estadoInicial] = {"ε1":estadosPila[0], "ε2":estadosPila[-1]}
                    transiciones[estadosPila[0]] = {transicionesPila.pop():estadosPila[1]}
                    transiciones[estadosPila[1]] = {"ε1":estadosPila[2],"ε2":estadosPila[0]}
                    estados.append(estadosPila)
                    estadoFinal = estadosPila[-1]
                    inicialesPila.append(estadoInicial)
                    finalesPila.append(estadosPila[-1])
                    estadosPila.clear()
                    transicionesPila.clear()
                    #print(transiciones)
                else:
                    for x in range(cont, cont+2):
                        estadosPila.append("q" + str(cont))
                        cont+= 1
                    transiciones[estadosPila[0]] = {"ε1":inicialesPila[-1], "ε2": estadosPila[-1]}
                    transiciones[finalesPila[-1]] = {"ε1":inicialesPila[-1],"ε2":estadosPila[-1]}
                    estados.append(estadosPila)
                    estadoFinal = estadosPila[-1]
                    if(inicialesPila != True and finalesPila != True):
                        inicialesPila[-1] = estadosPila[0]
                        finalesPila[-1] = estadosPila[-1]
                    else:
                        inicialesPila.append(estadosPila[0])
                        finalesPila.append(estadosPila[-1])
                    
                    estadosPila.clear()
                    #transicionesPila.clear()
                print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                print(transiciones)
                    
            elif(i == "."):
                if(len(transicionesPila) ==1 and len(inicialesPila) > 0 and len(finalesPila) == 1):
                    
                    #print(expresionPosfix[cont2-1])
                    if(expresionPosfix[cont2-1] in operadores):
                        transiciones["q" + str((len(transiciones)+ 1))] = {transicionesPila[-1], inicialesPila[-1]}
                    elif("q0" in transiciones):
                        #transiciones[finalesPila.pop()] = {transicionesPila.pop(): inicialesPila.pop()}
                        transiciones[finalesPila[-1]] = {transicionesPila.pop(): "q" + str((len(transiciones)+ 1))}
                        finalesPila.pop()
                        finalesPila.append("q" + str((len(transiciones))))
                    cont += 1
                    #print(transiciones)
                elif(len(inicialesPila) > 1 and len(finalesPila) > 1 and len(transicionesPila)==0):
                    print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                    transiciones[finalesPila[-2]] = {"ε1": inicialesPila[-1]}
                    #transiciones[finalesPila.pop(-2)] = {"ε1": inicialesPila.pop()}
                    print(transiciones)
                
                elif(estadoFinal == "" and len(transicionesPila) >= 2):
                    transiciones[estadoInicial] = {transicionesPila.pop(0): "q1"}
                    transiciones["q1"] ={ transicionesPila.pop(): "q2"}
                    #print(transiciones)
                    estadoFinal = "q2"
                    cont += 2
                    estados.append("q1")
                    estados.append("q2")
                    
                    inicialesPila.append(estadoInicial)
                    finalesPila.append(estadoFinal)
                    #print(cont)
                    #print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                    #len(inicialesPila) == 1 and len(finalesPila) == 1) or estadoFinal == "" and
                print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                print(transiciones) 
            elif(i == "|"):
                if(len(transicionesPila) >= 2):
                    if("q0" in transiciones):
                        for x in range(cont, cont+6):
                            estadosPila.append("q" + str(cont))
                            #print("q" + str(cont))
                            cont+= 1
                        #print(estadosPila)
                        #print(transiciones)
                    else:
                        estadosPila.append("q0")
                        
                        for x in range(cont, cont+5):
                            estadosPila.append("q" + str(cont))
                            #print("q" + str(cont))
                            cont+= 1
                    #print(estadosPila)
                    #print(transiciones)
                    #inicialesPila.append(finalesPila[-1])
                    transiciones[estadosPila[0]] = {"ε1":estadosPila[1], "ε2":estadosPila[2]}
                    transiciones[estadosPila[1]] = {transicionesPila.pop() : estadosPila[3]}
                    transiciones[estadosPila[2]] = {transicionesPila.pop() : estadosPila[4]}
                    transiciones[estadosPila[3]] = {"ε1":estadosPila[5]}
                    transiciones[estadosPila[4]] = {"ε1":estadosPila[5]}
                    #print(transiciones)
                    
                    #if("q0" in transiciones and cont<6):
                    #    transiciones.pop(estadoInicial)
            
                    #estados.pop()
                    estados.append(estadosPila)
                    if(estadoInicial != "q0"):
                        estadoInicial = estadosPila[0]
                    estadoFinal = estadosPila[-1]
                    #if(inicialesPila and finalesPila ):
                    #    inicialesPila[0] = estadoInicial
                    #    finalesPila[0] = estadoFinal
                    #else:
                    inicialesPila.append(estadosPila[0])
                    finalesPila.append(estadoFinal)
                    estadosPila.clear()
                    #print(transiciones)
                    #print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila) + "   soy del or   y estado final es " + str(estadoFinal))
                    #print("op1")
                elif(len(inicialesPila) == 1 and len(finalesPila) == 1 and len(transicionesPila) == 1):
                    #print("si entre")
                    #print(finalesPila)
                    for x in range(cont, cont+4):
                        estadosPila.append("q" + str(cont))
                        cont+= 1
                    #print(finalesPila)
                    transiciones[estadosPila[0]] = {"ε1" : estadosPila[1], "ε2" : inicialesPila[0]}
                    transiciones[estadosPila[1]] = {transicionesPila.pop() : estadosPila[2]}
                    transiciones[estadosPila[2]] = {"ε1" : estadosPila[3]}
                    #print(finalesPila)
                    transiciones[finalesPila.pop()] = {"ε2" : estadosPila[3]}
                    estados.pop()
                    estados.append(estadosPila)
                    estadoInicial = estadosPila[0]
                    estadoFinal = estadosPila[-1]
                    #print(transiciones)
                    #print("op2")
                elif(len(inicialesPila) == 2 and len(finalesPila) == 2):
                    for x in range(cont, cont+2):
                        estadosPila.append("q" + str(cont))
                        #print("q" + str(cont))
                        cont+= 1
                    transiciones[estadosPila[0]] = {"ε1" : inicialesPila[0], "ε2" : inicialesPila[1]}
                    transiciones[finalesPila[0]] = {"ε1" : estadosPila[1]}
                    transiciones[finalesPila[1]] = {"ε1" : estadosPila[1]}
                    estados.pop()
                    estados.append(estadosPila)
                    estadoInicial = estadosPila[0]
                    estadoFinal = estadosPila[-1]
                    inicialesPila.clear()
                    finalesPila.clear()
                    finalesPila.append(estadosPila.pop())
                    inicialesPila.append(estadosPila.pop())
                print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                print(transiciones)
                    #print(finalesPila + inicialesPila)
                    #print("op3")
            elif(i == "?"):
                if(estadoFinal == ""):
                    for x in range(cont, cont+3):
                        estadosPila.append("q" + str(cont))
                        cont+= 1
                    transiciones[estadoInicial] = {"ε1":estadosPila[0], "ε2":estadosPila[-1]}
                    transiciones[estadosPila[0]] = {transicionesPila.pop():estadosPila[1]}
                    transiciones[estadosPila[1]] = {"ε1":estadosPila[-1]}
                    estados.append(estadosPila)
                    estadoFinal = estadosPila[-1]
                    estadosPila.clear()
                    #transicionesPila.clear()
                    #print(transiciones)
                else:
                    for x in range(cont, cont+2):
                        estadosPila.append("q" + str(cont))
                        cont+= 1
                    transiciones[estadosPila[0]] = {"ε1":inicialesPila[0], "ε2": estadosPila[-1]}
                    transiciones[finalesPila.pop()] = {"ε1":estadosPila[-1]}
                    estados.append(estadosPila)
                    estadoFinal = estadosPila[-1]
                    estadosPila.clear()
                    #transicionesPila.clear()
                print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                print(transiciones)
            elif(i == "+"):
                if(estadoFinal == ""):
                    for x in range(cont, cont+4):
                        estadosPila.append("q" + str(cont))
                        cont+= 1
                    transiciones[estadoInicial] = {transicionesPila[0] : estadosPila[0]}
                    transiciones[estadosPila[0]] = {"ε1":estadosPila[1], "ε2":estadosPila[-1]}
                    transiciones[estadosPila[1]] = {transicionesPila.pop():estadosPila[2], "ε1":estadosPila[-1]}
                    transiciones[estadosPila[2]] = {"ε1":estadosPila[-1]}
                    estados.append(estadosPila)
                    estadoFinal = estadosPila[-1]
                    inicialesPila.append(estadoInicial)
                    finalesPila.append(estadosPila[-1])
                    estadosPila.clear()
                    #transicionesPila.clear()
                    #print(transiciones)
                elif(inicialesPila != "" and finalesPila != ""):
                    for x in range(cont, cont+4):
                        estadosPila.append("q" + str(cont))
                        print("q" + str(cont))
                        cont+= 1
                    transiciones[finalesPila[-1]] = {transicionesPila[-1]:estadosPila[0]}
                    transiciones[estadosPila[0]] = {"ε1":estadosPila[1], "ε2":estadosPila[-1]}
                    transiciones[estadosPila[1]] = {transicionesPila.pop():estadosPila[2], "ε1":estadosPila[-1]}
                    transiciones[estadosPila[2]] = {"ε1":estadosPila[-1]}
                    estados.append(estadosPila)
                    estadoFinal = estadosPila[-1]
                    if(inicialesPila != True and finalesPila != True):
                        inicialesPila[-1] = estadosPila[0]
                        finalesPila[-1] = estadosPila[-1]
                    else:
                        inicialesPila.append(estadosPila[0])
                        finalesPila.append(estadosPila[-1])
                    
                    estadosPila.clear()
                    #transicionesPila.clear()
                print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                print(transiciones)
        cont2 += 1
    estadoInicial = "q0"
    #inicialesPila.pop()
    #estadoFinal = finalesPila.pop()
    if(len(transicionesPila) == 1):
        transiciones[estadoInicial] = {transicionesPila.pop(): "q1"}
        #print(transiciones)
    return transiciones