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

        print("Ahora vamos a contruir el arbol binario")

        #leaf = Clases.Node()
        pila = []
        for i in expresionPosfix:
            print(i)
            if (i in alfabeto):
                leaf = Clases.Node(i)
                #print(i)
                pila.append(leaf)
            elif (i in operadores and i != "*" and i != "+"):
                leaf = Clases.Node(i)
                L1 = pila.pop()
                #print(L1.v)
                L2 = pila.pop()
                #print(L2.v)
                leaf.insertLeft(L1)
                leaf.insertRight(L2)
                pila.append(leaf)
            elif( i != "*" or i != "+"):
                leaf = Clases.Node(i)
                L1 = pila.pop()
                #print(L1.v)
                leaf.insertLeft(L1)
                pila.append(leaf)
            

        Clases.printTree(pila.pop())


        estadoDelWhile = False
    else:
        print("¡Error! Ingrese una expresion regular valida.")
        estadoDelWhile = False

    #(b|b)*abb(a|b)*
