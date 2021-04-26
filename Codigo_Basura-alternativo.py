
def Transformplus2():
    while expresion.find("+") != -1:
            '''son las variables que serviran para tener las posiciones de corte de la expresion'''
            conte1 = 0
            corte2 = 0
            '''aqui empezamos a analizar del final al principio toda la expresion o desde al posicion que tenga que
            analisar segun la posicion por la variable control'''
            for pos in range (len(expresion)-1,0,-1):
                
                if str(expresion[pos]) == "+":
                    print('entre')
                    corte1 = pos + 1
                    stack = []
                    #print(expresion[pos -1])
                    for x in range(pos-1,-1,-1):
                        #print('entre x2')

                        if expresion[x] == "*" or expresion[x] == "+" or expresion[x] == "?" or expresion[x] == ")" or expresion[x] in alfabeto:
                            print('entre x2')
                            stack.append(expresion[x])
                            print(str(stack))
                        elif expresion[x] == "(" and "(" in stack:
                            stack.remove(")") 
                            print(str(stack))
                        elif expresion[x] == "|" or expresion[x] == ".":
                            if ")" not in stack:
                                corte2 = x
                                transform = expresion[corte2 +1: corte1 - 1]
                                expresion = expresion[:corte2 + 1] + "(" + transform + "." + transform + "*)" + expresion[corte1:]
                                print(str(expresion))
                                stack = []
                                break
                            else:
                                stack.insert(0,expresion[x])
                    if len(stack) != 0:
                        print(str(stack))
                        print(str(expresion) + "dddd")
                        if(expresion[0] != "("):
                            transform = expresion[:corte1 -1]
                            expresion = "(" +transform + "." + transform + "*)" + expresion[corte1:]
                        else:
                            transform = expresion[1:corte1-1]
                            expresion = "((" +transform + "." + transform + "*)" + expresion[corte1:]
#proceso del operador + de thompson
"""
elif(i == "+"):
                if(estadoFinal == ""):
                    for x in range(cont, cont+4):
                        estadosPila.append("q" + str(cont))
                        cont+= 1
                    transiciones[estadoInicial] = {transicionesPila[0] : estadosPila[0]}
                    transiciones[estadosPila[0]] = {"ε1" : estadosPila[1], "ε2":estadosPila[-1]}
                    transiciones[estadosPila[1]] = {transicionesPila.pop() : estadosPila[2], "ε1" : estadosPila[-1]}
                    transiciones[estadosPila[2]] = {"ε1" : estadosPila[-1]}
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
                        #print("q" + str(cont))
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
                #print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                #print(transiciones)
"""
#un intento de resolver algo en thompson
'''elif len(transicionesPila) != 0 and len(finalesPila) >0:
                    newfinal = "q" + str(len(estados)+1)
                    transiciones[finalesPila.pop()] = {transicionesPila.pop(): newfinal}
                    finalesPila = []
                    inicialesPila = []
                    finalesPila.append(newfinal)
                '''