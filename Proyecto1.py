from abc import get_cache_token
from re import sub
import Funciones1 
import Clases

estadoDelWhile = True
print("Bienvenido al proyecto 1 de compiladores\n")
while estadoDelWhile:
    #recordar que se removio "\" por el momento
    metaCaracteres = ["*","(",")","|","?","ʚ"]
    operadores = ["*","|","?","ʚ"]
    alfabeto = []
    alfabetoNoe = []
    
    print("1. Usar Thompson y Subconjuntos para formar el AFN y AFD \n2. Usar el Metodo directo con Minimizacion para crear el AFD \n3. Salir del programa")
    opcion = input("elija una opcion: ")
    print("procederemos a comprobar si la sintaxis de la expresion regular es correcta")
    #Funciones.validadExpresion(expresion)
    if opcion == "3":

        estadoDelWhile = False

    else:

        expresion = input("ingrese la expresion regular que usara: ")
        if opcion == "2":
            expresion += "#"
        #print("¡Si! ¡la expresion esta correctamente escrita! Podemos proseguir")
        #print("vamos a obtener todos los caracteres unicos de la expresion")
        alfabeto, expresion = Funciones1.procesandoAlfabeto(expresion,alfabeto, metaCaracteres)
        #print("sus MetaCaracteres(operadores) son: " + str(operadores))
        #print("vamos a añadir el operador de concatenacion")
        print("la expresion regular con su operador de concatenacion queda asi: " + expresion)
        #print("realizaremos un proceso extra para trabajar el operador +, en caso se encuentre dentro de la expresion")
        expresionPosfix = Funciones1.infijoAPosfix(expresion,alfabeto)
        print ("Notacion posfija: " + str(expresionPosfix))
        print("su alfabeto es el siguiente: " + str(alfabeto))
        '''
        if expresion.find("+") != -1:
            expresion = Funciones1.Transformplus(expresion,alfabeto)
            print("si la expresion tenia algun +, pues ahora ha sido tranformado de esta forma " + expresion) 
            print("La expresion regular se veria de esta forma")
            Funciones1.printlist(expresion.split("<"))
        '''

        if opcion == "2":
        
            listOfVals = Funciones1.valsOfSimbols(expresionPosfix, alfabeto)
            print("la lista de Valores es: " + str(listOfVals))
            print("Ahora vamos a contruir el arbol binario")
            Tree, ConCatList =  Funciones1.crearArbol(expresionPosfix, alfabeto, operadores, listOfVals) 
            Funciones1.printTree(Tree)

            listOfsimbols = list(filter(lambda x: x not in operadores and x != "ε", expresionPosfix))
            #print(list(listOfsimbols))
            #print(str(len(ConCatList)) + "cantidad de nodos")
            FollowPosList = Funciones1.getFollowposList(ConCatList)
            listOfVals = Funciones1.valsOfSimbols(expresionPosfix, alfabeto)
            Funciones1.printDirectTable(listOfsimbols, listOfVals, FollowPosList)
            #Funciones1.printVerticallyList(FollowPosList)
            #print("\n" + str(FollowPosList))

            Transiciones = {}
            Transiciones = Funciones1.createDirectAFD(ConCatList, listOfVals, listOfsimbols, FollowPosList)
            #print(str(Transiciones))
            #print(str(list(Transiciones.keys())))
            DFA = Clases.Automata(ConCatList[-1].firstPos(),list(Transiciones.keys())[-1] ,list(Transiciones.keys()),list(filter(lambda x: x != "ε" and x != "#", alfabeto)), Transiciones)
            #print(str(DFA.alfabeto))
            traductor = {}
            cont = 0
            #print(str(DFA.estados))
            for estado in list(Transiciones.keys()):
                #print(estado)
                traductor[estado] = cont
                cont += 1

            #print(traductor)

            Grafo2 = Funciones1.crearGrafoDFA(DFA.transiciones, "AFD", DFA.estadosFinales, traductor)
            print("El grafo generado del AFD fue hecho en base a esta estructura: \n" + str(Grafo2))

            print("Ahora que ya tenemos el automata, podemos probar si funciona alguna cadena que ingresemos")
            cadena = input("ingrese su cadena a procesar: ")
            print(Funciones1.Simulation(DFA.estadoInicial, DFA.transiciones, cadena, DFA.estadosFinales))
        # estadoDelWhile = False

        #print("ahora formaremos el automata")
        
        elif(opcion == "1"):
        
        
            transiciones, estadoFinal, estadoInicial = Funciones1.Thompson(expresionPosfix, alfabeto)
            
            estados = Funciones1.getEstados(transiciones, estadoInicial)
            estados.append(estadoFinal)
            #print("los estados son: " + str(estados))
            #print("estado inicial es " + str(estadoInicial))
            #print("estado Final es " + str(estadoFinal))
            #print(str(transiciones))
            AFN = Clases.Automata(estadoInicial, estadoFinal, estados, alfabeto, transiciones)
            #print("ya que tenemos el automata a traves de thompson, vamos a graficarlo")
            Grafo = Funciones1.crearGrafoDelAutomata(AFN.transiciones, "AFN", estadoFinal)
            #print("El grafo generado del AFN fue hecho en base a esta estructura: \n" + str(Grafo))
            
            subconjuntos = Funciones1.clausuraE1(estados,AFN.transiciones)
            subconjuntos = Funciones1.sortSubSets(subconjuntos)
            #print("estos son lo subconjuntos despues de ClausuraE1: " + str(subconjuntos))
            #Funciones.printSubSets(subconjuntos, estados)
            
            subSets, allSubSets, alfabetoNoe = Funciones1.clausuraE2(subconjuntos, alfabeto,estadoInicial, transiciones)
            #a imprimir la tabla de Subconjuntos
            
            #print("estos son los subconjuntos unicos, luego de ClausuraE2" + str(subSets))
            #print("estos son todos los subconjuntos para la tabla" + str(allSubSets))

            
            Funciones1.printTableOfSubSets(subSets,allSubSets, alfabetoNoe)
            
            newStates = Funciones1.newStates(subSets)
            newEstadoInicial = "0"
            newEstadosFinales = Funciones1.newFinalStates1(subSets, newStates, estadoFinal)
            newTransitions = Funciones1.createFDA(subSets, alfabetoNoe, allSubSets, newStates)
            print(str(newEstadoInicial))
            print(str(newStates))
            print(str(newEstadosFinales))
            AFD = Clases.Automata(newEstadoInicial, newEstadosFinales, newStates, alfabetoNoe, newTransitions)
            
            Grafo2 = Funciones1.crearGrafoDelAutomata(AFD.transiciones, "AFD", newEstadosFinales)
            #print("El grafo generado del AFD fue hecho en base a esta estructura: \n" + str(Grafo2))
        
            print("Ahora que ya tenemos el automata, podemos probar si funciona alguna cadena que ingresemos")
            cadena = input("ingrese su cadena a procesar: ")
            print(Funciones1.Simulation(newEstadoInicial, newTransitions, cadena, newEstadosFinales))
            
            #estadoDelWhile = False
        
        else:
            print("Ingreso una opcion incorrecta, vuelva a intentarlo")
            # estadoDelWhile = False

'''
    #"ε"
    #dot -Tpng AFD.dot -o AFD.png 
    #dot -Tpng AFN.dot -o AFN.png
    
    (ε|b|c|d)*abb(a|b|c|d)* 
    (a|b|c|d)*abb(a|b|c|d)*
    ba(a|b)*ab
    (a|b)*abb 
    (ab)*|(c*)b
    (a|b)*abb(a|b)*
    (a*|b*)*
    ((ε|a)b*)*
    '''