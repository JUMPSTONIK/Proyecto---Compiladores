import Funciones 
import Clases
estadoDelWhile = True
print("Bienvenido al proyecto 1 de compiladores\n")
while estadoDelWhile:
    #recordar que se removio "\" por el momento
    metaCaracteres = ["*","+","(",")","|","?","."]
    operadores = ["*","+","|","?","."]
    alfabeto = []
    expresion = input("ingrese la expresion regular que usara: ")
    print("procederemos a comprobar si la sintaxis de la expresion regular es correcta")

    if Funciones.validadExpresion(expresion):
        print("¡Si! ¡la espresion esta correctamente escrita! Podemos proseguir")
        print("vamos a obtener todos los caracteres unicos de la expresion")
        alfabeto, expresion = Funciones.procesandoAlfabeto(expresion,alfabeto, metaCaracteres)
        print("su alfabeto es el siguiente: " + str(alfabeto))
        print("sus MetaCaracteres(operadores) son: " + str(operadores))
        print("vamos a añadir el operador de concatenacion")
        print("la expresion regular con su operador de concatenacion queda asi: " + expresion)
        expresionPosfix = Funciones.infijoAPosfix(expresion,alfabeto)
        print ("Notacion posfija: " + str(expresionPosfix))
        #print("Ahora vamos a contruir el arbol binario")   
        #Funciones.printTree(Funciones.crearArbol(expresionPosfix, alfabeto, operadores))
        print("ahora formaremos el automata")
        
        estadoInicial = "q0"
        estadoFinal = ""
        estados = ["q0"]
        transiciones = {}
        transicionesPila = []
        estadosPila = []
        inicialesPila = []
        finalesPila = []
        cont = 1
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
                        transiciones[estadosPila[0]] = {"ε1":inicialesPila[0], "ε2": estadosPila[-1]}
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
                    if(estadoFinal == "" and len(transicionesPila) >= 2):
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
                    elif(len(inicialesPila) == 1 and len(finalesPila) == 1 and len(transicionesPila) >=1):
                        #print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                        #print("logre entrar")
                        if("q0" in transiciones):
                            estadoFinal = "q" + str(len(transiciones)+1)
                        else:
                            estadoFinal = "q" + str(len(transiciones)+2)
                        
                        print(len(transiciones))
                        estados.append(estadoFinal)
                        if(transicionesPila):
                            transiciones[finalesPila.pop()] = {estadoFinal, transicionesPila.pop()}
                        else:
                            transiciones[finalesPila.pop()] = {estadoFinal, transicionesPila.pop()}
                        finalesPila.append(estadoFinal)
                        cont += 1
                        #print(transiciones)
                    elif(len(inicialesPila) > 1 and len(finalesPila) > 1 and len(transicionesPila)==0):
                        transiciones[finalesPila.pop(-2)] = {"ε1": inicialesPila.pop(-1)}
                        #print(transiciones)
                    print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                    print(transiciones)
                elif(i == "+"):
                    if(estadoFinal == ""):
                        pass
                    else:
                        pass
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
                        print(finalesPila)
                        transiciones[estadosPila[0]] = {"ε1" : estadosPila[1], "ε2" : inicialesPila[0]}
                        transiciones[estadosPila[1]] = {transicionesPila.pop() : estadosPila[2]}
                        transiciones[estadosPila[2]] = {"ε1" : estadosPila[3]}
                        print(finalesPila)
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
                        transicionesPila.clear()
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
                        transicionesPila.clear()
                    print(str(inicialesPila) + "   " + str(finalesPila) + "   " + str(transicionesPila))
                    print(transiciones)
                #pila.append()

        if(len(transicionesPila) == 1):
            transiciones[estadoInicial] = {transicionesPila.pop(): "q1"}
            print(transiciones)
        

        estadoDelWhile = False
    else:
        print("¡Error! Ingrese una expresion regular valida.")
        estadoDelWhile = False

    #(b|b)*abb(a|b)*
    #"ε"