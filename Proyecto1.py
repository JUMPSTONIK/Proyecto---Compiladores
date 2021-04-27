from abc import get_cache_token
from re import sub
import Funciones1 
import Clases

estadoDelWhile = True
print("Bienvenido al proyecto 1 de compiladores\n")
while estadoDelWhile:
    #recordar que se removio "\" por el momento
    metaCaracteres = ["*","+","(",")","|","?","."]
    operadores = ["*","+","|","?","."]
    alfabeto = []
    alfabetoNoe = []
    expresion = input("ingrese la expresion regular que usara: ")
    print("procederemos a comprobar si la sintaxis de la expresion regular es correcta")
    #Funciones.validadExpresion(expresion)
    if True:
        #print("¡Si! ¡la expresion esta correctamente escrita! Podemos proseguir")
        #print("vamos a obtener todos los caracteres unicos de la expresion")
        alfabeto, expresion = Funciones1.procesandoAlfabeto(expresion,alfabeto, metaCaracteres)
        #print("su alfabeto es el siguiente: " + str(alfabeto))
        #print("sus MetaCaracteres(operadores) son: " + str(operadores))
        #print("vamos a añadir el operador de concatenacion")
        print("la expresion regular con su operador de concatenacion queda asi: " + expresion)
        #print("realizaremos un proceso extra para trabajar el operador +, en caso se encuentre dentro de la expresion")
        if expresion.find("+") != -1:
            expresion = Funciones1.Transformplus(expresion,alfabeto)
            print("si la expresion tenia algun +, pues ahora ha sido tranformado de esta forma " + expresion) 
            print("La expresion regular se veria de esta forma")
            Funciones1.printlist(expresion.split("."))
            
        expresionPosfix = Funciones1.infijoAPosfix(expresion,alfabeto)
        print ("Notacion posfija: " + str(expresionPosfix))
        #print("Ahora vamos a contruir el arbol binario")   
        #Funciones.printTree(Funciones.crearArbol(expresionPosfix, alfabeto, operadores))
        print("ahora formaremos el automata")
        transiciones, estadoFinal, estadoInicial = Funciones1.Thompson(expresionPosfix, alfabeto)
        
        estados = Funciones1.getEstados(transiciones, estadoInicial)
        estados.append(estadoFinal)
        print("los estados son: " + str(estados))
        print("estado inicial es " + str(estadoInicial))
        print("estado Final es " + str(estadoFinal))
        print(str(transiciones))
        AFN = Clases.Automata(estadoInicial, estadoFinal, estados, alfabeto, transiciones)
        #print("ya que tenemos el automata a traves de thompson, vamos a graficarlo")
        Grafo = Funciones1.crearGrafoDelAutomata(AFN.transiciones, "AFN", estadoFinal)
        #print("El grafo generado del AFN fue hecho en base a esta estructura: \n" + str(Grafo))
        """
        subconjuntos = Funciones.clausuraE1(estados,AFN.transiciones)
        subconjuntos = Funciones.sortSubSets(subconjuntos)
        print(subconjuntos)
        #Funciones.printSubSets(subconjuntos, estados)
        
        subSets, allSubSets, alfabetoNoe = Funciones.clausuraE2(subconjuntos, alfabeto, estadoFinal, transiciones)
        #a imprimir la tabla de Subconjuntos
        Funciones.printTableOfSubSets(subSets,allSubSets, alfabetoNoe)
        
        newStates = Funciones.newStates(subSets)
        newEstadoInicial = "0"
        newEstadosFinales = Funciones.newFinalStates(subSets, newStates, estadoFinal)
        newTransitions = Funciones.createFDA(subSets, alfabetoNoe, allSubSets)

        AFD = Clases.Automata(newEstadoInicial, newEstadosFinales, newStates, alfabetoNoe, newTransitions)
        
        Grafo2 = Funciones.crearGrafoDelAutomata(AFD.transiciones, "AFD", newEstadosFinales)
        print("El grafo generado del AFD fue hecho en base a esta estructura: \n" + str(Grafo2))
        
        print("Ahora que ya tenemos el automata, podemos probar si funciona alguna cadena que ingresemos")
        cadena = input("ingrese su cadena a procesar: ")
        print(Funciones.Simulation(newEstadoInicial, newTransitions, cadena, newEstadosFinales))
        """
        estadoDelWhile = False
        
    else:
        print("¡Error! Ingrese una expresion regular valida.")
        estadoDelWhile = False

    #"ε"
    '''
    (b|b)*abb(a|b)*
    (ab)*|(c*)b
    (a|b)*abb(a|b)*
    (a*|b*)*
    ((ϵ|a)b*)*
    '''