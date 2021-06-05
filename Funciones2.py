import Funciones1 
import Clases

def extraction(line):
    firstcut = line.find("=")
    id = line[:firstcut]
    #print("id: " + id)
    terminal = line[firstcut + 1:] 
    #print("terminal: " + terminal)
    return id, terminal

def getText(fileName):
    f = open(fileName, "r")
    COCOr = f.read()
    f.close()
    return COCOr

def generateANY():
    ANY = ""
    for x in range(0,255):
        if chr(x) != '"' and chr(x) != "'": 
            ANY += chr(x) + "ñ"
    return ANY

def atgReader(wordsReserved, COCOr, CHARACTERS, KEYWORDS, TOKENS):
    for posWord in range(0, len(wordsReserved)):
        indexCut1 = 0
        indexCut2 = 0
        if wordsReserved[posWord] != "PRODUCTIONS":
            indexCut1 = COCOr.find(wordsReserved[posWord])
            #print(indexCut1)
            indexCut2 = COCOr.find(wordsReserved[posWord + 1])
            #print(indexCut2)
            text =  COCOr[indexCut1:indexCut2]
            #print(text)
            if wordsReserved[posWord] != "COMPILER":
                text = text.replace(wordsReserved[posWord],"")
                #text = text.replace("\n", "")
                #text = text.replace(" ", "")
                #print(text)
                lines = text.split(".\n")
                for x in range(0,len(lines)):
                    lines[x] = lines[x].replace("\n","")
                    lines[x] = lines[x].replace(" ","")
                #print(str(lines))
                try:
                    lines.remove('')
                except:
                    pass
                #lines.remove('')
                #print(str(lines))
                for line in lines:
                    if wordsReserved[posWord] == wordsReserved[1]:
                        id, terminal = extraction(line)
                        CHARACTERS[id] = terminal
                    if wordsReserved[posWord] == wordsReserved[2]:
                        id, terminal = extraction(line)
                        KEYWORDS[id] = terminal
                    if wordsReserved[posWord] == wordsReserved[3]:
                        #print(line)
                        id, terminal = extraction(line)
                        #print(id +" = " + terminal)
                        #if terminal.find(id) == -1:
                        TOKENS[id] = terminal
    return CHARACTERS, KEYWORDS, TOKENS

def readAndProcess(CHARACTERS):
    charkeys = Funciones1.getkeys(CHARACTERS)
    for key in charkeys:
        line = CHARACTERS[key]
        if line.find("..") != -1:
            indPL = line.find("'")
            limit1 = line[indPL+1 : indPL+2]
            #print("limit1: " + limit1)
            indSL = line.find("'", indPL+3)
            limit2 = line[indSL+1: indSL+2]
            #print("limit2: " + limit2)
            newline = ""
            for x in range(ord(limit1), ord(limit2)+1):
                newline += chr(x)
            line = newline
            CHARACTERS[key] = line

        while line.find("CHR(") != -1:
            letpos = line.find("CHR(")
            initline = line[0:line.find("CHR(")]
            #print("initline: " + initline)
            lastpos = line.find(')',letpos+1)
            seccionToProcess = line[letpos:lastpos]
            #print("seccion to process: " + seccionToProcess)
            endline = line[lastpos:]
            #print("endline: " + endline)
            #print(str(seccionToProcess[4:]))
            line = initline + str(chr(int(seccionToProcess[4:]))) + endline[:-1]
            CHARACTERS[key] = line 
            #print("line after proccess: " + line)
        if line.find("'") != -1:
            line = line.replace("'","")
        if line.find(")") != -1 and line.find("(") == -1:
            #print("mira que si entre")
            line = line.replace(")", "")
        for x in range(0, len(charkeys)-1):
            if line.find(str(charkeys[x])) != -1:
                #print(str(line))
                #print(CHARACTERS[keys[x]])
                #print(keys[x])
                line = line.replace(charkeys[x], CHARACTERS[charkeys[x]])
                #line = line.replace("+","")
                #print(str(line))
                CHARACTERS[key] = line

        CHARACTERS[key] = line
    return charkeys, CHARACTERS

def plusAndLessSubsets(charkeys, CHARACTERS):
    for key in charkeys:
        line = CHARACTERS[key]
        if line.find("+") != -1 and key != "ignore" and key != "blanco" and key != "whitespace" and key != "sign" and key != "ANY" and key != "stringletter" and key != "MyANY":
            line = line.replace("+","")
            listLine = sorted(set(list(line)))
            line = ""
            for item in listLine:
                line += item 
            line = line +'"'
            CHARACTERS[key] = line
            #print(line)
        elif(key == "ignore" or key == "whitespace"):
            line = line.replace("+", "|")
            line = "(" + line + ")"
            CHARACTERS[key] = line
        elif key == "blanco":
            line = line.replace("+", "|")
            line = "(" + line + " )"
            CHARACTERS[key] = line
        elif key == "sign":
            line = line.replace("++","+|")
            line = "(" + line + ")"
            CHARACTERS[key] = line
        #print(str(CHARACTERS))
        if line.find("-") != -1 and key != "ANY" and key != "operadores" and key != "sign":
            listOfSubsets = []
            #print("hay un -")
            val = 150
            #print(str(key))
            ##print(line.find("-"))
            while line.find("-") != -1:
                lista = line[:line.find("-",val)]
                line = line[line.find("-",val)+1:]
                val = 0
                listOfSubsets.append(lista)
                #print("estoy dentro")
            else:
                listOfSubsets.append(line)
            
            if "+" in listOfSubsets[1]:
                list1 = listOfSubsets.pop()
                list2 = listOfSubsets.pop()
                thelist = list2 + "-" + list1
                listOfSubsets.append(thelist[1:-1])
            
            for x in range(1,len(listOfSubsets)):
                for item in listOfSubsets[x]:
                    #print(item)
                    listOfSubsets[0] = listOfSubsets[0].replace(item,"")
            while listOfSubsets[0].find("ññ") != -1:
                listOfSubsets[0] = listOfSubsets[0].replace("ññ",'')
            #print(listOfSubsets[0].find("ññ"))
            CHARACTERS[key] = listOfSubsets[0]
            #print("la lista de subconjuntos es: " + str(listOfSubsets))
    return CHARACTERS

def fixingDetailsCHARACTERS(charkeys, CHARACTERS, file):

    for key in charkeys:
        line = CHARACTERS[key]
        if line[0] == '"' and line[-1] == '"' and key != "comillas":
            #print(line)
            line = line.replace("", "|")
            line = "(" + line[3:-3] + ")"
            #print(key)
            #print(line)
            CHARACTERS[key] = line
        elif line.find("/ñ") != -1:
            line = line.replace("ñ", "|")
            line = line.replace("*,", "*|,")
            line = line.replace(";?", ";|?")
            line = "(" + line[2:] + ")"
            #print(key)
            #print(line)
            CHARACTERS[key] = line
        file += key + " = " + CHARACTERS[key] + "\n"
    return CHARACTERS, file

def gettingKeywords(KEYWORDS, file):
    values = Funciones1.getvalues(KEYWORDS)
    listKeywords = []
    if KEYWORDS != {}:
        for vals in values:
            file += vals +", "
            listKeywords.append(vals[1:-1])
        file = file[:-2] + "]\n"
    else: 
        file += "]\n"
    #print(str(listKeywords))
    return file, listKeywords

def processAndConvert(TOKENS, Tokkeys, charkeys, file, CHARACTERS):
    
    #print(str(Tokkeys))
    cont = 0
    for key in Tokkeys:
        #print(str(key))
        expresion = TOKENS[key]
        if expresion.find("EXCEPTKEYWORDS") != -1:
            # EXCEPT = expresion[expresion.find("EXCEPTKEYWORDS"): expresion.find("EXCEPTKEYWORDS") + len("EXCEPTKEYWORDS")]
            # #print( EXCEPT)
            # EXCEPT = ' + "' + EXCEPT + '"'
            expresion = expresion[:expresion.find("EXCEPTKEYWORDS")]
        #print(expresion)
        expresion = expresion.replace('"(', ' + ".(')
        expresion = expresion.replace(')"', ')"')
        expresion = expresion.replace('|', ' + "|" + ')
        expresion = expresion.replace('."', '"')
        expresion = expresion.replace("{",' + ".(" +')
        expresion = expresion.replace("}",' + ")*" +')
        #el cambio lo hice aqui
        expresion = expresion.replace("[",' + "" + ')
        expresion = expresion.replace("]",' + "?" + ')
        #hasta aqui
        expresion = expresion.replace('""', '')
        expresion = expresion.replace('"("', '"+"("+')
        expresion = expresion.replace('.(" + ".(', '.(" + "(')
        expresion = expresion.replace("+ +", "+")
        expresion = expresion.replace("+  +", "+")
        expresion = expresion.replace('".(" + ".("', '".(" + "("')
        #estas 2 son nuevas y es de ver si no arruinan nada de las anteriores
        expresion = expresion.replace(' + (', ' + ".(" + ')
        expresion = expresion.replace(') + ', ' + ")" + ')
        expresion = expresion.replace('+ ")*"(', '+ ")*" + ".(" + ')
        expresion = expresion.replace('letter"', 'letter + "')
        while expresion.find("CHR(") != -1:
            letpos = expresion.find("CHR(")
            initline = expresion[0:expresion.find("CHR(")]
            #print("initline: " + initline)
            lastpos = expresion.find(')',letpos+1)
            seccionToProcess = expresion[letpos:lastpos]
            #print("seccion to process: " + seccionToProcess)
            endline = expresion[lastpos:]
            #print("endline: " + endline)
            expresion = initline + 'CHR.(" +' +  seccionToProcess[5:] + endline
            #print("line after proccess: " + line)
            expresion.replace('CHR("', 'CHR(" + ')
        #print(expresion)
        #print(expresion[-2])
        if expresion[-1] == "+":
            expresion = expresion[:-2]
        if expresion[-2] == "+":
            expresion = expresion[:-3]
        if expresion[-1] == ")":
            expresion = expresion[:-1] + ' + ")"'
        if expresion.find("startcode") != -1:
            expresion = 'startcode = "(."'
        expresion = expresion.replace('.(', '(')
        expresion = expresion.replace(').', ')')
        expresion = expresion.replace(' ', '')
        expresion = expresion.replace('+', '')
        if key == "startcode":
            expresion = '"((.)"'
        if key == "endcode":
            expresion = '"(.))"'
        expresion = expresion.replace('"', '')
        if expresion.find("CHR",8) != -1:
            #print("si entre")
            part1 = expresion[:expresion.find("CHR",5)]
            #print(part1)
            part2 = expresion[expresion.find("CHR",5):]
            #print(part2)
            expresion = part1 + ".." + part2
        #print(key + " = " + expresion)
        #expresion = expresion.replace('|||', '|')
        TOKENS[key] = expresion
        #print(file)
        #file += Tokkeys[cont] + " = " + expresion + "\n"
        cont += 1 
    
    
        
    for x in range(0, len(Tokkeys)):
        line = TOKENS[Tokkeys[x]]
        for c in range(len(charkeys)-1, -1, -1):
            key = charkeys[c]
            #print(key)
            #print(Tokkeys[x])
            if line.find(key) != -1  and (Tokkeys[x] != 'nontoken' and key != 'ANY') and (Tokkeys[x] != 'hexnumber' or key != 'digit'):
                #print("entre")
                #print(key)
                line = line.replace(key, CHARACTERS[key])
                #print("nueva linea: " + line)
                #line = line.replace("+","")
                #print(str(line))
            elif Tokkeys[x] == 'nontoken' and key == 'MyANY':
                theline = CHARACTERS[key].replace("z~", "z|~")
                theline = theline.replace("?|", "")
                theline = theline.replace("*|", "")
                theline = theline.replace(".|", "")
                line = theline
        file += Tokkeys[x] + " = " + line + "\n"
        TOKENS[Tokkeys[x]] = line
        #print(str(TOKENS))
    return TOKENS, file




def CreateAFN(expresion, name = "", cont = 0):
    metaCaracteres = ["*","(",")","|","?","ʚ"]
    operadores = ["*","|","?","ʚ"]
    alfabeto = []
    #recibimos la expresion para formar el alfabeto y la cadena para el posfix
    alfabeto, expresion = Funciones1.procesandoAlfabeto(expresion,alfabeto, metaCaracteres)
    #transformamos a posfix
    expresionPosfix = Funciones1.infijoAPosfix(expresion,alfabeto)
    #llamamos la funcion de Thompson para generar las transiciones y obtener el estado
    #inicial y final
    transiciones, estadoFinal, estadoInicial = Funciones1.Thompson(expresionPosfix, alfabeto, cont)
    #obtenemos todos los estados el automata
    estados = Funciones1.getEstados(transiciones, estadoInicial)
    estados.append(estadoFinal)
    #damos forma al Automata en un objeto
    AFN = Clases.Automata(estadoInicial, estadoFinal, estados, alfabeto, transiciones, name)
    #generamos el grafo
    Funciones1.crearGrafoDelAutomata(AFN.transiciones, "AFN" + name, estadoFinal)
    return AFN

def CreateAFD(AFN, cont = 0, listaFinales = []):
    #con los estados y el automata con sus transiciones y a quien apunta se forman los subconjutos
    subconjuntos = Funciones1.clausuraE1(AFN.estados,AFN.transiciones)
    #ordenamos los conjuntos para que sea mas simple de tratarlos.
    subconjuntos = Funciones1.sortSubSets(subconjuntos)
    #aqui en la segunda clausura se envian los subconjuntos, el alfabeto, el estado inicial y el automata. 
    #el alfabeto es enviado, para que sepa por cuales transiciones pasar y quizas sea necesario eliminar el los
    #"()", porque es posible que eso de errores o sino añadirlos. los subconjuntos, ya que con ello se decide si usar el
    #primer conjuntos o el estado incial, en el caso sea una concatenacion la primera operacion. Ademas del uso del
    #automata, ya que con el se obtiene parte imporante de los subconjuntos de la siguiente parte para hacer el AFD
    subSets, allSubSets, alfabetoNoe = Funciones1.clausuraE2(subconjuntos, AFN.alfabeto,AFN.estadoInicial, AFN.transiciones)
    #Funciones1.printTableOfSubSets(subSets,allSubSets, alfabetoNoe)
    #añadimos el estado inicial, que esta relacionado con el valor del cont, el cual da forma a los estados de inicio
    #a fin
    newEstadoInicial = cont
    #print(str(cont))
    #aqui generamos los estaods en base a la cantidad de subconjuntos unicos obtenidos, ya que seran quienes
    #se contecten entre si
    newStates = Funciones1.newStates(subSets, cont)
    #En esta funcion se crea un array de los nuevos estados finales, ya que estos son aquellos que posean en su
    #subconjunto el valor del estado final o finales.
    newEstadosFinales = Funciones1.newFinalStates1(subSets, newStates, AFN.estadosFinales)
    #print(str(cont))
    #print(str(newStates))
    #print(str(newEstadosFinales))
    newTransitions = Funciones1.createFDA(subSets, alfabetoNoe, allSubSets,newStates)
    #print(newStates)
    AFD = Clases.Automata(newEstadoInicial, newEstadosFinales, newStates, alfabetoNoe, newTransitions)
    
    Funciones1.crearGrafoDelAutomata(AFD.transiciones, "AFD" + AFN.nombre, newEstadosFinales)
    return AFD

def CreateSuperAFD(estados, transiciones, alfabeto, estadoInicial,listaFinales, name, cont = 0):
    #con los estados y el automata con sus transiciones y a quien apunta se forman los subconjutos
    subconjuntos = Funciones1.clausuraE1(estados, transiciones)
    #ordenamos los conjuntos para que sea mas simple de tratarlos.
    subconjuntos = Funciones1.sortSubSets(subconjuntos)
    #aqui en la segunda clausura se envian los subconjuntos, el alfabeto, el estado inicial y el automata. 
    #el alfabeto es enviado, para que sepa por cuales transiciones pasar y quizas sea necesario eliminar el los
    #"()", porque es posible que eso de errores o sino añadirlos. los subconjuntos, ya que con ello se decide si usar el
    #primer conjuntos o el estado incial, en el caso sea una concatenacion la primera operacion. Ademas del uso del
    #automata, ya que con el se obtiene parte imporante de los subconjuntos de la siguiente parte para hacer el AFD
    subSets, allSubSets, alfabetoNoe = Funciones1.clausuraE2(subconjuntos, alfabeto, estadoInicial, transiciones)
    #Funciones1.printTableOfSubSets(subSets,allSubSets, alfabetoNoe)
    #añadimos el estado inicial, que esta relacionado con el valor del cont, el cual da forma a los estados de inicio
    #a fin
    newEstadoInicial = cont
    #print(str(cont))
    #aqui generamos los estaods en base a la cantidad de subconjuntos unicos obtenidos, ya que seran quienes
    #se contecten entre si
    newStates = Funciones1.newStates(subSets, cont)
    #print(str(newStates))
    #print("\n" + str(listaFinales))
    #En esta funcion se crea un array de los nuevos estados finales, ya que estos son aquellos que posean en su
    #subconjunto el valor del estado final o finales.
    newEstadosFinales = Funciones1.newFinalStates2(subSets, newStates, listaFinales)
    #print(str(newEstadosFinales))
    #print(str(cont))
    #print(str(newStates))
    #print(str(newEstadosFinales))
    newTransitions = Funciones1.createFDA(subSets, alfabetoNoe, allSubSets,newStates)
    #print(newStates)
    AFD = Clases.Automata(newEstadoInicial, newEstadosFinales, newStates, alfabetoNoe, newTransitions, "AFDSuperAutomata" + name)
    
    Funciones1.crearGrafoDelAutomata(AFD.transiciones, "AFDSuperAutomata" + name, newEstadosFinales)
    return AFD



def GeneradorDeAutomatas(Tokkeys, TOKENS):
    contEstadosAFD = 0
    contEstadosAFN = 0
    listExceptions = []
    listOfAFN = []
    listOfAFD = []
    for x in range(0,len(Tokkeys)):
        #aqui obtenemos lo necesario para los AFN
        expresionRegular = TOKENS[Tokkeys[x]]
        # if expresionRegular.find("EXCEPTKEYWORDS") != -1:
        #     expresionRegular = expresionRegular[:expresionRegular.find("EXCEPTKEYWORDS")]
        #     listExceptions.append(Tokkeys[x])
        #print(expresionRegular)
        #print(Tokkeys[x])
        listOfAFN.append(CreateAFN(expresionRegular, Tokkeys[x], contEstadosAFN))
        contEstadosAFN += len(listOfAFN[x].estados)

        
        #ahora crearemos los AFD en base a los AFN en la lista
        listOfAFD.append(CreateAFD(listOfAFN[x],contEstadosAFD))
        #print(listOfAFD[x].estados)
        contEstadosAFD += len(listOfAFD[x].estados)
        #print("este es el valor del cont para los AFD " + str(contEstadosAFD))

    return listExceptions, listOfAFN, listOfAFD

def getTokenAri(SUPERAFD, estado, listToken):
    cont = 0
    for estadosFinales in SUPERAFD.estadosFinales:
        
        if str(estado) in estadosFinales:
            print(listToken[cont])
        cont += 1
    estado = SUPERAFD.estadoInicial
    return estado

def aritmeticaScanner(TOKENS, SUPERAFD, content):
    listToken = Funciones1.getkeys(TOKENS)
    print(str(listToken))
    estado = SUPERAFD.estadoInicial
    for item in content:
        print("'" + item + "'")
        if item in SUPERAFD.alfabeto:
            #print("im in")
            estado = SUPERAFD.transiciones[str(estado)][item]
            
        else:
            estado = getTokenAri(SUPERAFD, estado, listToken)
        
    if estado != 0:
        estado = getTokenAri(SUPERAFD, estado, listToken)

def getToken(SUPERAFD, listToken,listKeyWords, word):
    #word = word.strip()
    #print("'" + word + "'")
    token = ""
    cont = 0
    estado = SUPERAFD.estadoInicial
    if word == "(.":
        token = "startcode"
    elif word == ".)":
        token = "endcode"
    elif word[0] == '"' and word[-1] =='"':
        token =  "string"
    elif len(word) == 4 and word[0] == "'" and word[-1] == "'" and word[1] == "/" and ((ord(word[2]) >= 97 and ord(word[2]) <= 122) or (ord(word[2]) >= 65 and ord(word[2]) <= 90)):
        token =  "char"
    elif word == "=" or word == "+" or word == "-" or word == "==" or word == "<=" or word == ">=" or word == "/" or word == "<" or word == ">" or word == "*":
        token = "operador"
    else:
        for letter in word:
            if letter != "(" and letter != ")" and letter != "{" and letter != "}" and letter != "|":
                #print(letter)
                try:
                    estado = SUPERAFD.transiciones[str(estado)][letter]
                except:
                    print(letter + " error")
                    token = "ERROR"    

    if token == "":
        for estadosFinales in SUPERAFD.estadosFinales:
            
            if str(estado) in estadosFinales:
                token = listToken[cont]
            cont += 1

    if token == "ident" or token == "number":
        if word in listKeyWords:
            token = "keyword"

    return token

def fixAlfabeth(SUPERAFD):
    SUPERAFD.alfabeto.append("(")
    SUPERAFD.alfabeto.append(")")
    SUPERAFD.alfabeto.append("}")
    SUPERAFD.alfabeto.append("{")
    SUPERAFD.alfabeto.append("+")
    SUPERAFD.alfabeto.append("-")
    SUPERAFD.alfabeto.append("=")
    SUPERAFD.alfabeto.append("[")
    SUPERAFD.alfabeto.append("]")
    SUPERAFD.alfabeto.append("<")
    SUPERAFD.alfabeto.append(">")
    SUPERAFD.alfabeto.append("|")
    SUPERAFD.alfabeto.append('"')

    return SUPERAFD

def cleanWord(word):
    word = word.replace("{"," ")
    word = word.replace("}"," ")
    word = word.replace("|"," ")
    word = word.replace("["," ")
    word = word.replace("]"," ")
    return word

def Scanner(content, SUPERAFD, listToken, listKeywords):
    listOfWordsInContent = []
    listOfTokenFromContent = []
    word = ""
    line = 0
    pos = 1
    for item in content:
        #print("'" + item + "'")
        if item != " " and item != "\n" and item != "\t" :
            if item in SUPERAFD.alfabeto:
                word += item
                pos += 1
            else:
                if item != " " and item != "\n" and item != "\t":
                    word += item
                    print("Se ha detectado un caracter no aceptable: " + str(item) + " En la posicion " + str(pos) + " linea " + str(line))
                    pos += 1
        else:
            #print("x"+word+"x")
            if word != "":
                #print(word)
                if word[0] == '"' and word[-1] == '"':
                    if word[1:-2].find('"') == -1:
                        listOfWordsInContent.append(word)
                        listOfTokenFromContent.append(getToken(SUPERAFD, listToken,listKeywords, word))
                        #word = ""
                        #print("El token de " + str(listOfWordsInContent[-1] + " es " + str(listOfTokenFromContent[-1])))
                    else:
                        word = cleanWord(word)
                        word = word.replace('"',' " ')
                        listOfwords = []
                        listOfwords = word.split()
                        newListOfWords = []
                        #print(str(listOfwords))
                        posi = 0
                        while posi < len(listOfwords):
                            if listOfwords[posi] == '"':
                                #print(str(x))
                                palabra = listOfwords[posi] + listOfwords[posi+1] +listOfwords[posi+2]
                                #print(palabra)
                                posi += 3
                                newListOfWords.append(palabra)
                            else:
                                #print(listOfwords[posi])
                                newListOfWords.append(listOfwords[posi])
                                posi += 1 
                        #print(str(newListOfWords))
                        palabra = ""
                        for palabra in newListOfWords:
                            #print(palabra)
                            listOfWordsInContent.append(palabra)
                            listOfTokenFromContent.append(getToken(SUPERAFD, listToken,listKeywords, palabra))
                            #print("El token de " + str(listOfWordsInContent[-1] + " es " + str(listOfTokenFromContent[-1])))

                        
                elif word.find("{") == -1 and word.find("}") == -1 and word.find("|") == -1:
                    listOfWordsInContent.append(word)
                    listOfTokenFromContent.append(getToken(SUPERAFD, listToken,listKeywords, word))
                    #word = ""
                    #print("El token de " + str(listOfWordsInContent[-1] + " es " + str(listOfTokenFromContent[-1])))
                else:
                    word = cleanWord(word)
                    listOfwords = word.split()
                    #print(str(listOfwords))

                    for palabra in listOfwords:
                        #print(palabra)
                        listOfWordsInContent.append(palabra)
                        listOfTokenFromContent.append(getToken(SUPERAFD, listToken,listKeywords, palabra))
                        #print("El token de " + str(listOfWordsInContent[-1] + " es " + str(listOfTokenFromContent[-1])))

            word = ""
        if(item == "\n"):
            pos = 1
            line += 1

    return listOfWordsInContent, listOfTokenFromContent

    