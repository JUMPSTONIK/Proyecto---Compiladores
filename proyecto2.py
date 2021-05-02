import Funciones2 
import Funciones1

'''Estos son los textos de prueba'''
#COCOr = Funciones2.getText("Aritmetica.ATG")
#COCOr = Funciones2.getText("HexNumber.ATG")
COCOr = Funciones2.getText("CoCoL.ATG")
#COCOr = Funciones2.getText("Double.ATG")
#print(COCOr)

'''guardamos las palabras que definen cada seccion'''
wordsReserved = ["COMPILER", "CHARACTERS", "KEYWORDS", "TOKENS", "PRODUCTIONS"]
COMPILER = ""
CHARACTERS = {}
KEYWORDS = {}
TOKENS = {}
PRODUCTIONS = {}

'''extraemos la informacion dentro de la seccion compiler'''
COMPILER = "'''" + str(COCOr[COCOr.find("/*"):COCOr.find("*/")+2]) + "'''"
#print(COMPILER)


if COCOr.find("ANY") != -1:
    CHARACTERS["ANY"] = Funciones2.generateANY()[:-1]

#print(CHARACTERS)

'''Extraemos todas las lineas dentro con su identificador y su valor'''
CHARACTERS, KEYWORDS, TOKENS = Funciones2.atgReader(wordsReserved, COCOr, CHARACTERS, KEYWORDS, TOKENS)

#print("CHARACTERS: " + str(CHARACTERS))
#print("KEYWORDS: " + str(KEYWORDS))
#print("TOKENS" + str(TOKENS))
'''añadimos lo al file algunos textos'''
file = "#" + wordsReserved[0] + "\n" + COMPILER +"\n"
file += "#CHARACTERS\n"

'''Esta es la primer funcion que obtendra los rangos tipo "A-Z", procesara los CHR() 
limpiara algunos signos y tambien añadira al resto de CHARACTERS los otros que esten
dentro de la misma variable '''

charkeys, CHARACTERS = Funciones2.readAndProcess(CHARACTERS)

'''Los CHARACTERS poseen dentro de la sintaxis de COCOl algo llamado las operacions
de union y resta de conjuntos y eso es lo que ejecutamos en el siguiente proceso
sobre los valores de CHARACTERS '''

CHARACTERS = Funciones2.plusAndLessSubsets(charkeys, CHARACTERS)

'''Finalmente nos encontramos con algunos problemas que se llegan a dar dentro de la
Gramatica de Cocol, por lo que con la siguiente funcion se arreglan algunos pequeños
detalles, por la forma en la que se ha procesado el texto de los CHARTACTERS '''

CHARACTERS, file = Funciones2.fixingDetailsCHARACTERS(charkeys, CHARACTERS, file)

'''En esta parte nos enfocaremos en trabajar con las KEYWORDS para limpiarlas y 
tambien obtener una lista con todas las keywords, que nos podira servir despues '''
file += "#KEYWORDS\n" + "keywords = ["
file, listKeywords = Funciones2.gettingKeywords(KEYWORDS, file)

'''Ahora procederemos a limpiar y traducir los TOKENS del lenguage de Cocol a
Expresiones regulares que podamos procesar. Tambien se añadiran los CHARACTERS
dentro de las Expresiones regulares. Asi estaran listas para trabajar con ellas. '''

file += "#TOKENS\n"
Tokkeys = Funciones1.getkeys(TOKENS)
TOKENS, file = Funciones2.processAndConvert(TOKENS, Tokkeys, charkeys, file, CHARACTERS)

#print(file)

Funciones1.createFile("file", file, ".py")


listExceptions, listOfAFN, listOfAFD = Funciones2.GeneradorDeAutomatas(Tokkeys,TOKENS)
superCont = 1
root = "q#"
superAutomata = {}
superAutomata[root] = {}
superEstados = []
superEstados.append(root)
ListaFinales = []
superAlfabeto = []
#print(str(superAutomata))

for AFN in listOfAFN:
    print(str(superCont))
    #añadimos nuevo estado inicial, llamado root al super automata y su transicion epsilon hacia
    #el estado inicial del AFN de la lista
    superAutomata[root]["ε" + str(superCont)] = str(AFN.estadoInicial)
    #hacemos un merge del diccionario del super automata y el AFN correspondiente
    superAutomata = {**superAutomata, **AFN.transiciones}
    #obtenemos los estados finales de cada AFN para crear el AFD y sus estados finales
    ListaFinales.append(AFN.estadosFinales)
    #unimos las listas de estados de los AFN para crear la lista con todos los estados
    superEstados = superEstados + AFN.estados
    superAlfabeto = Funciones1.sortList(list(set(superAlfabeto + AFN.alfabeto)))
    superCont += 1

#print(str(superAlfabeto))
#print(str(superAutomata))

SUPERAFD = Funciones2.CreateSuperAFD(superEstados, superAutomata, superAlfabeto, root, ListaFinales)

print(str(SUPERAFD.transiciones))



#Tomar en cuenta que el problema con los (), puede que sea en thompson o en cualquier operacion que utilice
#el alfabeto y puede sea necesario añadirlos. Esto es un recordatorio para asi poder
#dar una solucion a ello a futuro y puede que eso sea lo que esta afectando el uso
#de dicho simbolo.
#*****Revisar todas las funciones que hagan uso del alfabeto y verificar que no discriminena ()***

#deberia poner en las condiciona donde se descriminan los () y los operadores, que si ya se hallo un "("
#significa que tanto ( y ) son del alfabeto y operandos