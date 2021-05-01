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

'''Extraemos todas las lineas dentro con su identificados y su valor'''
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

contEstadosAFD = 0
contEstadosAFN = 0
listExceptions = []
listOfAFN = []
listOfAFD = []
for x in range(0,len(Tokkeys)):
    #aqui obtenemos lo necesario para los AFN
    expresionRegular = TOKENS[Tokkeys[x]]
    if expresionRegular.find("EXCEPTKEYWORDS") != -1:
        expresionRegular = expresionRegular[:expresionRegular.find("EXCEPTKEYWORDS")]
        listExceptions.append(Tokkeys[x])
    print(expresionRegular)
    listOfAFN.append(Funciones2.CreateAFN(expresionRegular, Tokkeys[x], contEstadosAFN))
    contEstadosAFN += len(listOfAFN[x].estados)

    
    #ahora crearemos los AFD en base a los AFN en la lista
    listOfAFD.append(Funciones2.CreateAFD(listOfAFN[x],contEstadosAFD))
    #print(listOfAFD[x].estados)
    contEstadosAFD += len(listOfAFD[x].estados)
    print("este es el valor del cont para los AFD " + str(contEstadosAFD))


    

                
