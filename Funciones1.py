import re
from os import remove
import Clases
import subprocess

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
                #print(demo)
        except:
            pass
    return alfabeto, expresion

def Transformplus(expresion, alfabeto):
    '''Este while existe para que se revise la cantidad de veces que sea necesaria la expresion y se resetee el tamaño
    del primer for'''
    while expresion.find("+") != -1:
        '''son las variables que serviran para tener las posiciones de corte de la expresion'''
        corte1 = 0
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
                    elif expresion[x] == "(":
                        stack.remove(")") 
                        print(str(stack))
                    elif expresion[x] == "|" or expresion[x] == ".":
                        if ")" not in stack:
                            corte2 = x
                            transform = expresion[corte2 +1: corte1 - 1]
                            expresion = expresion[:corte2 + 1] + transform + "." + transform + "*" + expresion[corte1:]
                            print(str(expresion))
                            stack = []
                            break
                        else:
                            stack.insert(0,expresion[x])
                if len(stack) != 0:
                    transform = expresion[:corte1 -1]
                    expresion = transform + "." + transform + "*" + expresion[corte1:]
    return expresion
"""Esta es una funcion que sirve para poder mostrar una lista con todo su contenido concatenado"""
def printlist(expresion):
    regular = ""
    for item in expresion:
        regular += item
    print(regular)

"""Código para expresiones regulare de Infija a Postfija"""
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

def Thompson(expresionPosfix, alfabeto):
    stackTransiciones = []
    stackIniciales = []
    stackFinales = []
    automata = {}
    cont = 0
    stackNewNodos = []
    for caracter in expresionPosfix:
        print(caracter)
        if caracter in alfabeto:
            stackTransiciones.append(caracter)
            print(len(stackTransiciones))
        else:
            if caracter == "|":
                if len(stackTransiciones) >= 2:
                    transicion1 = stackTransiciones.pop()
                    transicion2 = stackTransiciones.pop()

                    for x in range(cont, cont + 6):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1
                    automata[stackNewNodos[0]] = {"ε1": stackNewNodos[1], "ε2" : stackNewNodos[2]}
                    automata[stackNewNodos[1]] = {transicion1 : stackNewNodos[3]}
                    automata[stackNewNodos[2]] = {transicion2 : stackNewNodos[4]}
                    automata[stackNewNodos[3]] = {"ε1":stackNewNodos[5]}
                    automata[stackNewNodos[4]] = {"ε1":stackNewNodos[5]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 1:
                    transicion1 = stackTransiciones.pop()
                    inicial = stackIniciales.pop()
                    final = stackFinales.pop()

                    for x in range(cont, cont + 4):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1
                    
                    automata[stackNewNodos[0]] = {"ε1": inicial, "ε2" : stackNewNodos[1]}
                    automata[stackNewNodos[1]] = {transicion1 : stackNewNodos[2]}
                    automata[stackNewNodos[2]] = {"ε1" : stackNewNodos[3]}
                    automata[final] = {"ε1":stackNewNodos[3]}
                    
                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 0:
                    inicial1 = stackIniciales.pop()
                    inicial2 = stackIniciales.pop()
                    final1 = stackFinales.pop()
                    final2 = stackFinales.pop()

                    for x in range(cont, cont + 2):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1": inicial2, "ε2" : inicial1}
                    automata[final1] = {"ε1":stackNewNodos[1]}
                    automata[final2] = {"ε1":stackNewNodos[1]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

            if caracter == ".":
                if len(stackTransiciones) >= 2:
                    transicion1 = stackTransiciones.pop()
                    transicion2 = stackTransiciones.pop()

                    for x in range(cont, cont + 3):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {transicion1: stackNewNodos[1]}
                    automata[stackNewNodos[1]] = {transicion2: stackNewNodos[2]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 1:
                    transicion1 = stackTransiciones.pop()
                    final = stackFinales.pop()

                    stackNewNodos.append("q" + str(cont))
                    cont += 1

                    automata[final] = {transicion1: stackNewNodos[0]}
                    
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 0:
                    final = stackFinales.pop(-2)
                    inicial = stackIniciales.pop()

                    automata[final] = {"ε1": inicial}

            if caracter == "*":
                if len(stackTransiciones) >= 1:
                    transicion1 = stackTransiciones.pop()

                    for x in range(cont, cont + 4):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1":stackNewNodos[1], "ε2":stackNewNodos[3]}
                    automata[stackNewNodos[1]] = {transicion1 :stackNewNodos[2]}
                    automata[stackNewNodos[2]] = {"ε1":stackNewNodos[3], "ε2":stackNewNodos[1]}
                    
                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 0:
                    inicial = stackIniciales.pop()
                    final = stackFinales.pop()

                    for x in range(cont, cont + 2):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1": inicial, "ε2": stackNewNodos[1]}
                    automata[final] = {"ε1": inicial, "ε2":stackNewNodos[1]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

            if caracter == "?":
                if len(stackTransiciones) >= 1:
                    transicion1 = stackTransiciones.pop()

                    for x in range(cont, cont + 4):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1":stackNewNodos[1], "ε2":stackNewNodos[3]}
                    automata[stackNewNodos[1]] = {transicion1 :stackNewNodos[2]}
                    automata[stackNewNodos[2]] = {"ε1":stackNewNodos[3]}
                    
                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 0:
                    inicial = stackIniciales.pop()
                    final = stackFinales.pop()

                    for x in range(cont, cont + 2):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1": inicial, "ε2":stackNewNodos[1]}
                    automata[final] = {"ε1":stackNewNodos[1]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

    return automata, stackFinales.pop(), stackIniciales.pop()


def crearGrafoDelAutomata(Transiciones, name,estadosFinales):
    Grafo = "digraph G{\n"
    for key in Transiciones:
        #print(key)
        #print(Transiciones[key])
        for innerKey in Transiciones[key]:
            graph = str(key) + " -> " + str(Transiciones[key][innerKey]) + " [label=" + str(innerKey) + "]\n"
            
            if key in estadosFinales and str(name) == "AFD" and str(key) + " [ style=bold ]" not in Grafo:
                graph += str(key) + " [ style=bold ]\n"
            
            #print(innerKey)
            #print(Transiciones[key][innerKey])
            Grafo = str(Grafo) + str(graph)
    #print(str(name))
    if str(name) == "AFN":
        #print("aaaaaaaaaa")
        Grafo += str(estadosFinales) + " [ style=bold ]\n"
    Grafo = str(Grafo) + "}"
    #print(Grafo)
    createFile(name,Grafo, ".dot")
    return Grafo

def createFile(name, text, extension):
    existe = False
    try:
        with open(str(name) + extension, 'r') as f:
            existe = True
    except FileNotFoundError as e:
        existe = False
    
    if existe == True:
        remove(str(name) + extension)
        f = open(str(name) + extension,'a', encoding='utf-8')
        f.write(str(text))
        f.close()
    else:
        f = open(str(name) + extension,'a', encoding='utf-8')
        f.write(str(text))
        f.close()

def getEstados(transiciones, estadoInicial):
    result = []
    for key in transiciones.keys():
        if key not in result:
            result.append(key)
    if result[0] != estadoInicial:
        ind = result.index(estadoInicial)
        #estadoNotinit = result[0]
        result[ind] = result[0]
        result[0] = estadoInicial
        #for i in range(1,ind):
            
    return result

def getkeys(dict):
    list = []
    #print("dict es: " + str(dict))
    for key in dict.keys():
        list.append(key)
    return list

def getvalues(dict):
    list = []
    for val in dict.values():
        list.append(val)
    return list

def clausuraE1(estados,transiciones):
    theStates = []
    subconjuntos = []
    listEst = []
    listTrans = []
    #print(str(estados))
    #print(str(transiciones))
    for item in estados:
        estadoTrans = item
        conjunto = []
        theStates.append(item)
        #print(estadoTrans)
        find = False
        while(find == False):
            
            if estadoTrans in transiciones:
                Estytrans = transiciones[estadoTrans]
                #print("====== fijate bien aqui con === " + str(Estytrans))
                lista = getkeys(Estytrans) 
                #print(lista)
                for i in range(0,len(lista)):
                    listTrans.append(lista.pop(0))
                lista = getvalues(Estytrans)
                #print(lista)
                for i in range(0,len(lista)):
                    listEst.append(lista.pop(0))
                        
            #print("la lista de transiciones es " + str(listTrans))
            #print("la lista de estados es " + str(listEst))
            size = len(listEst)-1
            for x in range(size,-1,-1):
                #print(str(x))
                #print("Estamos verificando la transicion " + str(listTrans[x]) + " y el estado " + str(listEst[x]))
                if(str(listTrans[x]) != "ε1" and str(listTrans[x]) != "ε2"):
                    #print(str(listTrans[x]) + " es algo que no es epsilon")
                    #print("conjuntos esta asi " + str(conjunto))
                    listTrans.pop()
                    listEst.pop()
                    #print("la lista de transiciones es " + str(listTrans))
                    #print("la lista de estados es " + str(listEst))
                    #print(str(x))
                    #print("antes de entrar listEst esta asi: " + str(listEst) + " y x es " + str(x))
                elif(listEst[x] in conjunto):
                    #print(str(listEst[x]) + " ya se encuentra dentro de conjutnos")
                    #print("conjuntos esta asi " + str(conjunto))
                    listEst.pop()
                    listTrans.pop()
                    #print("la lista de transiciones es " + str(listTrans))
                    #print("la lista de estados es " + str(listEst))
                    pass
                
            if(len(listEst) != 0 and len(listTrans) != 0):
                testTrans = listTrans[-1]
                #print("transicion a testear es " + str(testTrans) + " hacia el estado " + str(listEst[-1]))
                if(testTrans == "ε1" or testTrans == "ε2"):
                    #print("halle epsilon")
                    #print("la lista de transiciones esta asi actualmente " + str(listTrans))
                    #cont += 1
                    estadoTrans = listEst.pop()
                    conjunto.append(estadoTrans)
                    listTrans.pop()
                    #print("conjuntos esta asi " + str(conjunto))
                    #print("la lista de transiciones es " + str(listTrans))
                    #print("la lista de estados es " + str(listEst))
                    #print("siguiente estado a revisar es "+ str(estadoTrans))
            else:
                find = True
                subconjuntos.append(conjunto)
                #print("la lista de estados esta " + str(theStates))
                #print("los subconjuntos respectivo a su estado esta " + str(subconjuntos))
    
    return subconjuntos

def printSubSets(subconjuntos, estados):

    for y in range(0, len(subconjuntos)):
        print(str(estados[y]) + " U " + str(subconjuntos[y]))

def sortSubSets(subconjuntos):
    for set in range(0, len(subconjuntos)):
        subconjuntos[set].sort()
    return subconjuntos

def sortList(list):
    list.sort()
    return list

def clausuraE2(subconjuntos, alfabeto, estadoFinal, transiciones):
    theStates = []
    subSets = []
    allTheStates = []
    allSubSets = []
    listEst = []
    listTrans = []
    listEstadosTemp = []
    conjunto = []
    subSets.append(subconjuntos[0])
    alfa = [e for e in alfabeto if e != "ε"]
    alfa = sortList(alfa)
    '''obtenemos la lista dentro de la lista'''
    print(str(subSets))
    for losEstados in subSets:
        print(str(losEstados))
        '''realizamos ciclo para cada letra del alfabeto'''
        allSubSets.append(losEstados)
        for item in alfa:
            print(item)
            #print("el caracter del alfabeto que toca analizar es: " + str(item) + "     xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            '''obtenemos cada elemento de la lista obtenida anteriormente'''
            for estado in losEstados:
                #print("el estado en el que estamos es: " + str(estado) + " ````````````")
                '''creamos la lista donde estara el conjunto a guardar
                verificamos que no sea el estado final, ya que el estado final no tiene keys'''
                if estado != estadoFinal:
                    '''verificamos si el estado actual posee transiciones iguales a la letra actual'''
                    if item in transiciones[estado].keys(): 
                        '''ya que si tiene el mismo tipo de transicion, lo guardamos en estadoReceptor, en caso en la busqueda haga algun loop'''
                        estadoReceptor = estado
                        #print("el estado receptor es: " + str(estadoReceptor + " +++++++++++++++++++++++++++++++"))
                        #print("el estado con la transicion " + str(item) + " es " + str(estadoReceptor) + "_______________")
                        '''automaticamente guardamos al estado que apunta dentro de conjunto, ya que desde ahi iniciara su recorrido y podemos consentrarnos en los 
                        siguientes estados y sus transiciones. Cabe decir que de esta manera, en caso sea algun or, ya se tendra guardado el estado al que punta
                        ahorrando la busqueda mas adelante.'''
                        conjunto.append(transiciones[estado][item])
                        '''ademas que asi guardamos en estadoTrans dicha transicion a la que apunta para iniciar la busqueda'''
                        estadoTrans = transiciones[estado][item]
                        #print("ya que se sabe que " + str(estado) + " tiene transicion " + str(item) + " al conjunto se añade " + str(estadoTrans))
                        #print("conjunto se ve ahora asi: " + str(conjunto))
                        '''verificamos si no esta guardado el estado en theStates y lo guardamos en theStates y allTheStates
                        en el caso que si, solo lo guardamos en allTheStates para tener la diferencia.
                        hay que recordar, que theStates sirve para referenciar a subSets y saber de que estado salio dicho subconjunto'''
                        if estadoTrans not in theStates:
                            allTheStates.append(estadoTrans)
                        else:
                            allTheStates.append(estadoTrans)
                        '''creamos una variable para dar fin al ciclo'''
                        find = False
                        '''ya que hay un estado, empezamos a analizarlo'''
                        while(find == False):
                            '''si estadoTrans se encuentra en transiciones, obtendremos sus transiciones y estados a los que apunta.'''
                            if estadoTrans in transiciones:
                                '''obtendremos dentro de una lista, todos los keys o transiciones que tiene'''
                                Estytrans = transiciones[estadoTrans]
                                lista = getkeys(Estytrans) 
                                
                                for i in range(0,len(lista)):
                                    listTrans.append(lista.pop(0))
                                '''luego obtendremos todos los estados correspondientes a cada transicion obtenida de antes.'''
                                lista = getvalues(Estytrans)
                                
                                for i in range(0,len(lista)):
                                    listEst.append(lista.pop(0)) 
                            '''mostraremos la lista de transiciones y Estado, para poder saber con que se esta trabajando.'''
                            #print("la lista de transiciones es " + str(listTrans))
                            #print("la lista de estados es " + str(listEst))
                            '''obtenemos el tamaño de la lista de estados
                            en esta seccion queremos evitar revisitar estados que ya pasamos y eliminar las transiciones que no sean epsilon
                            por ellos revisaremos del ultimo al primer elemento de cada lista.'''
                            size = len(listEst)-1
                            for x in range(size,-1,-1):
                                #print(str(estadoTrans) + " es el estado con transicion " + str(listTrans[x] + " hacia " + str(listEst[x])))
                                #Aqui revisamos si dicha transicion no es epsilon o si no del tipo de transicion que estamos trabajando
                                if(str(listTrans[x]) != "ε1" and str(listTrans[x]) != "ε2" and str(listTrans[x]) != item):
                                    #print("aqui se esta realizando las siguiente eliminaciones, ya no nos importan las transiciones distintas a epsilon o " + str(item))
                                    #print( "se ha eliminado la transicion " + listTrans.[-1])
                                    listTrans.pop()
                                    #print("se ha eliminado el estado " + listEst[-1])
                                    listEst.pop()
                                    #print("la lista de transiciones es " + str(listTrans))
                                    #print("la lista de estados es " + str(listEst))
                                    """aqui verificamos si ya existia el estado dentro de conjuntos. Esto sirve para evitar el tener que revisar un estado que ya visitamos
                                junto a sus transiciones. Si ya esta, entocnes procede a eliminar su estado y su transicion respectivamente."""
                                elif(listEst[x] in conjunto):
                                    #print(str(listEst[x]) + " ya se encuentra dentro de conjutnos, por lo que eliminamos tener que recorrerlo de nuevo")
                                    #print( "se ha eliminado la transicion " + listTrans[-1])
                                    listTrans.pop()
                                    #print("se ha eliminado el estado " + listEst[-1])
                                    listEst.pop()
                                    #print("la lista de transiciones es " + str(listTrans))
                                    #print("la lista de estados es " + str(listEst))
                            '''aqui mostramos la lista de transiciones y de estados que quedaron, luego de revisar si ya se habian trabajo con ellas o las transiciones
                            que se encontraban en la lista no eran epsilon o el tipo de transicion con la que vamos a trabajar.'''
                            #print("antes de entrar, estas son:")
                            #print("la lista de EstadoTemp estaba asi: " + str(listEstadosTemp))
                            #print("la lista de transiciones es " + str(listTrans))
                            #print("la lista de estados es " + str(listEst))
                            '''Comenzaremos el tercer proceso de estos estados y tansiciones, donde iniciaremos revisando si las listas proveidas no son vacias.
                            Se hace esta verificacion, ya que al estar vacias, no hay nada que procesar.'''
                            if(len(listEst) != 0 and len(listTrans) != 0):
                                '''ya que no son vacias, procedemos a tomar el ultimo elemento dentro de la lista de transiciones, ya que queremos verificar las transiciones
                                de tipo epsilon para la clausura'''
                                testTrans = listTrans[-1]
                                #print("transicion a testear es " + str(testTrans) + " hacia el estado " + str(listEst[-1]))
                                '''aqui verificamos si el testTrans tiene una transicion del tipo epsilon'''
                                if testTrans == "ε1" or testTrans == "ε2":
                                    '''Si resulta que testTrans si es epsilon, procedemos  a sacar el estado de la lista de estados y se lo asignamos a estadoTrans
                                    de esta forma tendremos el proximo estado a verificar sus transiciones
                                    asi mismo, procedemos a eliminar el estado verificado de la lista de Transiciones, para luego mostrar como esta conjuntos actualmente'''
                                    estadoTrans = listEst.pop()
                                    conjunto.append(estadoTrans)
                                    listTrans.pop()
                                    #print("conjuntos esta asi " + str(conjunto))
                                    #print("la lista de transiciones es " + str(listTrans))
                                    #print("la lista de estados es " + str(listEst))
                                    #print("siguiente estado a revisar es "+ str(estadoTrans))
                                    '''En caso que testTrans no sea un epsilon, eso quiere decir que es una tansicion del mismo tipo, que estamos verificando su 
                                clausura'''    
                                elif testTrans == item:
                                    '''al ser el mismo, procedemos a eliminarlo y a su estado que apunta'''
                                    #print("eliminaremos esta transicion " + str(testTrans) + " y su estado " + str(listEst[-1]) + " ya que tiene la misma transicion")
                                    listEst.pop()
                                    listTrans.pop()
                                    '''cuando llegamos a este punto, necesitamos conseguir el proximo estado a trabajar, pero es posible que ya no hallan.
                                    Esto nos indica que ya se han hallado todos los estados y transiciones posibles.
                                    De no fallar, entonces podra seguir trabajando y revisando las transiciones de los proximos estados'''
                                    try:
                                        estadoTrans = listTrans[-1]
                                        '''si falla, es porque ya no hay nada mas y le indicamso que puede salir del loop, ya que la lista esta totalmente vacia en 
                                    este punto.'''
                                    except:
                                        find = True
                                        #print("hasta aqui llega")
                                    #print("nuevo estado de Transicion es " + str(estadoTrans))
                                '''si hemos llegado aqui, es porque las listas de Transiciones y de estados esta totalmente vacia.
                            dado este caso, debemos asegurarnos por distintos factores si realmente se ha terminado de revisar todos los estados del subconjunto 
                            en la revision de este estado. Es asi que si encontramos que las listas estan vacias y el estado, del cual se esta revisando si tiene
                            alguna transicion del tipo que se esta trabajando en esta vuelta, es el mismo del ultimo elemento del subconjunto.'''
                            elif len(listEst) == 0 and len(listTrans) == 0 and estado == losEstados[-1]:
                                '''si resulta ser asi, le indicamos que puede salir de este loop y procesguir con el siguiento del alfabeto a revisar'''
                                find = True
                                '''mostramos el resultado final de lo que hay en conjuntos y procedemos a ordenarlo'''
                                #print("conjunto sin orden es " + str(conjunto))
                                conjunto = sortList(conjunto)
                                '''verificamos si conjunto se encuentra en subSets, porque no queremos que en esa lista se encuentre repetido y lo metemos a la lista temporal.
                                aqui tambien lo metemos en allSubSets a conjuntos, para tener el record de todo lo trabajado en todo el proceso.'''
                                listEstadosTemp.append(conjunto)
                                '''ya que hemos guardado el conjunto, procedemos a mostrar cual fue el estado final que se trabajo y como esta la lista temporal
                                de conjuntos que luego meteremos a subSets, ademas de vaciar la lista de conjuntos'''
                                #print("el estado final fue: " + str(estado))
                                #print("la lista de listas de subconjuntos unicos es " + str(listEstadosTemp))
                                conjunto = []
                                
                                '''Tambien sabemos que las listas pueden estar vacias y jamas haber llegado al estado final del subconjunto que estamos revisando.
                            por ello se guardo algo llamado el estadoReceptor, para saber si hemos llegado hasta al mismo estado que inicio la
                            busqueda de la clausura. queremos saber si estadoTrans es el mismo a estadoReceptor, porque hemos vuelto al inicio de la busqueda o si
                            estadoReceptor ya esta en conjuntos.Esto es porque de estarlo, puede que ya se le halla encontrado buscando la misma transicion, pero hizo
                            falta mas de alguno, ya que no tenia epsilon, sino que la misma transicion de item. de esta manera le podemos indicar que salga del loop, 
                            porque ya no tiene mas estados a los cuales llegar para buscar.'''
                            elif len(listEst) == 0 and len(listTrans) == 0 and estado != losEstados[-1] and (estadoReceptor == estadoTrans or estadoReceptor in conjunto):
                                #print("el estadoTrans es :" + str(estadoTrans))
                                #print("la lista de EstadoTemp estaba asi: " + str(listEstadosTemp))
                                if len(listEstadosTemp) >= (alfa.index(item) + 1):
                                    listEstadosTemp[alfa.index(item)] = conjunto
                                elif len(listEstadosTemp) <= alfa.index(item):
                                    listEstadosTemp.append(conjunto)
                                #print("agregando conjunto ahora esta asi: " + str(listEstadosTemp))
                                #print("este es el index de " + str(item)+ ": " + str(alfa.index(item)))
                                #print("todo esta vacio **********")
                                find = True
                        '''puede ser que se haya terminado de revisar todos los estados de un subconjunto con todas las transiciones del alfabeto, pero aun hace falta que sea 
                    guardado el conjunto creado en la listaTemporal, ya que aun contiene dicho conjunto de estados'''           
                    elif conjunto != []:
                        '''de ser lo anterior, ordenara la lista de conjunto'''
                        conjunto = sortList(conjunto)
                        '''verificamos si conjunto se encuentra en subSets, porque no queremos que en esa lista se encuentre repetido y lo metemos a la lista temporal.
                        aqui tambien lo metemos en allSubSets a conjuntos, para tener el record de todo lo trabajado en todo el proceso.'''
                        if conjunto not in subSets and len(listEstadosTemp) < len(alfa):
                            listEstadosTemp.append(conjunto)
                        '''en el caso que si este conjunto en subSets, pues solo lo añadimos a la lista de todos los conjuntos hechos.
                        mostramos el estado en el que se estaba trabajando y la lista temporal que trabajaremos al terminar de revisar todo el subconjunto de estados'''
                        #print("el estado en el que estamos es: " + str(estado))
                        #print("la lista de listas de subconjuntos unicos es " + str(listEstadosTemp))
                        conjunto = []
                    '''Tambien esta la posibilidad de que todo un subconjunto no tuviera ninguna transicion de la que tenia item, por lo que procedemos a guardar en
                    alltheStates y allSubSets un espacio vacia y el conjunto vacio respectivamente.'''
            
            #print("Conjunto esta asi : " + str(conjunto) + " y listTemp esta asi: " + str(listEstadosTemp) + " despues de analizar a <" + str(item) + ">")
            if conjunto == [] and listEstadosTemp == []:
                listEstadosTemp.append([])
        '''Se tiene esta condicional para revisar si conjunto no esta vacio. La razon viene de es que posible que los estados, los cuales se estuvieron revisando para formar
        el conjunto, haya llegado al estado final. Cuando llega a ser revisado el estado final, este se omite y no se se sigue procesando, ya que no exite nada mas adelante del mismo.
        por ello se saca del proceso, pero no se añade el conjunto a la lista temporal, por lo que se debe hacer fuera del proceso.'''
        if conjunto != []:
            listEstadosTemp.append(sortList(conjunto))
            conjunto = []
        
        #print("la lista de listas de estados unicos son: " + str(listEstadosTemp) + " con los que procedemos a insertar en Subsets" +" <---------------------------------------")
        '''Al final, añadimos los conjuntos de la lista temporal a la lista de subSets para que pueda seguir trabajando'''
        for SubSetsUni in listEstadosTemp:
            if(SubSetsUni != [] and SubSetsUni not in subSets):
                subSets.append(SubSetsUni)
            allSubSets.append(SubSetsUni)
        listEstadosTemp = []
        '''finalmente, mostramos el resultado de como termino la lista de conjuntos unicos que seran usador para formar el automata finito determinista.'''
        #print("subset se ve asi, despues de añadir la listaTemp" + str(subSets))
        #print("allSubset se ve asi, despues de añadir la listaTemp" + str(allSubSets))
    return subSets, allSubSets, alfa

def printTableOfSubSets(subSets,allSubSets, alfabetoNoe):
    TheStates = newStates(subSets)
    separacion = 0
    for cont in range(0,len(subSets)):
        if separacion == 0:
            separacion = len(subSets[0])
        elif len(subSets[cont]) > len(subSets[cont - 1]):
            separacion = len(subSets[cont])
    separacion *= 5
    columnas = "    Q " + (" " * separacion)
    for letra in alfabetoNoe:
        columnas = columnas + (" " * round(separacion/2)) + str(letra) + (" " * separacion)
    print(columnas)
    #columnas = columnas + (" " * round(separacion/2)) + "tipo" + (" " * separacion)
    fila = ""
    cont = 0
    for state in TheStates:
        fila = str(state) + "   "
        for unConjunto in range(0,len(alfabetoNoe)+1):
            if cont % (len(alfabetoNoe)+1) == 0:
                fila += str(allSubSets[cont]) + (" " * separacion)
            else:
                reference = columnas.index(alfabetoNoe[(cont % (len(alfabetoNoe)+1))-1])
                separacionL = len(fila) - reference

                if separacionL < 0:
                    fila = fila + (" " * (separacionL*-1))
                    fila += str(allSubSets[cont]) + (" " * separacion)
                else:
                    fila = fila[0: len(fila) - separacionL]
                    fila += str(allSubSets[cont]) + (" " * separacion)
            
            cont += 1
        fila += "\n"
        print(fila)
        fila = ""

def newStates(subSets):
    TheStates = []
    for cont in range(0,len(subSets)):
        TheStates.append(str(cont))
    return TheStates

def newFinalStates(subSets, newStates, estadoFinal):
    theNewFinalStates = []
    cont = 0
    for conjunto in subSets:
        if estadoFinal in conjunto:
            theNewFinalStates.append(str(newStates[cont]))
        cont += 1
    return theNewFinalStates

def createFDA(subSets, alfabetoNoe, allSubSets):
    NStates = newStates(subSets)
    newTransitions = {}
    cont1 = 1
    cont2 = 0
    for uniConjunto in subSets:
        newTransitions[NStates[cont2]] = {}
        for item in alfabetoNoe:
            if allSubSets[cont1] != []:
                newTransitions[NStates[cont2]][item] = subSets.index(allSubSets[cont1])
                
            cont1 += 1
        cont1 += 1    
        cont2 += 1
    return newTransitions


def Simulation(newEstadoInicial, newTransitions, cadena, newEstadosFinales):
    estado = newEstadoInicial
    print(newTransitions)
    for item in cadena:
        print("El elemento que vamos a procesar de la cadena es " +str(item))
        #print(str(newTransitions.keys()))
        #print(Funciones.getkeys( newTransitions))
        #print(estado)
        if str(estado) in getkeys(newTransitions):
            print(str(estado) + " posee estas transiciones " + str(newTransitions[str(estado)]))
            try:
                print("por lo que asignamos el estado " + str(newTransitions[str(estado)][item]))
                estado = newTransitions[str(estado)][item]
            except:
                estado = "none"
                pass
            #print(str(estado))
    print(newEstadosFinales)
    if str(estado) in newEstadosFinales:
        return "La cadena ha sido aceptada"
    else:
        return "la cadena no fue aceptada"

def Transformplus(expresion, alfabeto):
    '''Este while existe para que se revise la cantidad de veces que sea necesaria la expresion y se resetee el tamaño
    del primer for'''
    while expresion.find("+") != -1:
        '''son las variables que serviran para tener las posiciones de corte de la expresion'''
        corte1 = 0
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
                    elif expresion[x] == "(":
                        stack.remove(")") 
                        print(str(stack))
                    elif expresion[x] == "|" or expresion[x] == ".":
                        if ")" not in stack:
                            corte2 = x
                            transform = expresion[corte2 +1: corte1 - 1]
                            expresion = expresion[:corte2 + 1] + transform + "." + transform + "*" + expresion[corte1:]
                            print(str(expresion))
                            stack = []
                            break
                        else:
                            stack.insert(0,expresion[x])
                if len(stack) != 0:
                    transform = expresion[:corte1 -1]
                    expresion = transform + "." + transform + "*" + expresion[corte1:]
    return expresion


