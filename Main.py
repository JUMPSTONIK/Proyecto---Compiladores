import Funciones 
import Clases
from os import remove

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
        Transiciones = Funciones.Thompson(expresionPosfix, alfabeto, operadores)
        #print(str(Transiciones) + "  estoy fuera de la funcion")
        print("ya que tenemos el automata a traves de thompson, vamos a graficarlo")

        Grafo = "digraph G{\n"
        for key in Transiciones:
            #print(key)
            #print(Transiciones[key])
            for innerKey in Transiciones[key]:
                graph = str(key) + " -> " + str(Transiciones[key][innerKey] + " [label=" + str(innerKey) + "]\n")
                #print(innerKey)
                #print(Transiciones[key][innerKey])
                Grafo = str(Grafo) + str(graph)
        Grafo = str(Grafo) + "}"
        print(Grafo)
        try:
            remove("demo.dot")
        except:
            f = open('demo.dot','a', encoding='utf-8')
            f.write(str(Grafo))
            f.close()

        estadoDelWhile = False
    else:
        print("¡Error! Ingrese una expresion regular valida.")
        estadoDelWhile = False

    #(b|b)*abb(a|b)*
    #"ε"