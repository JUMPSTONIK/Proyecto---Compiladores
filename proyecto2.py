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
ANY = 'ANY = "('
ANYexist = False
if COCOr.find("ANY"):
    ANYexist = True
    for x in range(32,255):
        if chr(x) != '"' and chr(x) != "'": 
            ANY += chr(x) + "|"

ANY = ANY [:-1] + ')*"'
#theany = ANY.split("","|")
print(ANY)
'''Extraemos todas las lineas dentro con su identificados y su valor'''
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
                    id, terminal = Funciones2.extraction(line)
                    CHARACTERS[id] = terminal
                if wordsReserved[posWord] == wordsReserved[2]:
                    id, terminal = Funciones2.extraction(line)
                    KEYWORDS[id] = terminal
                if wordsReserved[posWord] == wordsReserved[3]:
                    #print(line)
                    id, terminal = Funciones2.extraction(line)
                    print(id +" = " + terminal)
                    if terminal.find(id) == -1:
                        TOKENS[id] = terminal

#print("CHARACTERS: " + str(CHARACTERS))
#print("KEYWORDS: " + str(KEYWORDS))
#print("TOKENS" + str(TOKENS))

file = "#" + wordsReserved[0] + "\n" + COMPILER +"\n"
file += "#CHARACTERS\n"
if ANYexist == True:
    file += ANY + "\n"
keys = Funciones1.getkeys(CHARACTERS)
#print(str(keys))
for key in keys:
    line = CHARACTERS[key]
    #print(line)
    for letpos in range(0,len(line)):
        if line[letpos] == '"':
            #print("entre")
            initline = line[0:letpos]
            #print("initline: " + initline)
            lastpos = line.find('"',letpos+1)
            seccionToProcess = line[letpos + 1:lastpos]
            #print("seccion to process: " + seccionToProcess)
            endline = line[lastpos+1:]
            #print("endline: " + endline)
            seccionToProcess = seccionToProcess.replace("","|")
            seccionToProcess = seccionToProcess[1:-1]
            seccionToProcess = '"(' + seccionToProcess + ')*"'
            line = initline + seccionToProcess + endline
            letpos += len(seccionToProcess) + 2 
            #print("letpos: " + str(letpos))
    while line.find("CHR(") != -1:
        letpos = line.find("CHR(")
        initline = line[0:line.find("CHR(")]
        #print("initline: " + initline)
        lastpos = line.find(')',letpos+1)
        seccionToProcess = line[letpos:lastpos]
        #print("seccion to process: " + seccionToProcess)
        endline = line[lastpos:]
        #print("endline: " + endline)
        line = initline + "chr" + seccionToProcess[3:] + endline
        #print("line after proccess: " + line)
    if line.find("..") != -1:
        indPL = line.find("'")
        limit1 = line[indPL+1 : indPL+2]
        #print("limit1: " + limit1)
        indSL = line.find("'", indPL+3)
        limit2 = line[indSL+1: indSL+2]
        #print("limit2: " + limit2)
        newline = '"('
        for x in range(ord(limit1), ord(limit2)+1):
            newline += chr(x) + '|'
        newline = newline[:-1] + ')*"'
        line = newline
    if line.find("+''") != -1:
        part1 = line[:line.find("+''") +2]
        part2 = line[line.find("+''") + 2:]
        line = part1 + " " + part2
        
    line.replace("+" , "' '")
    #print(line)

    CHARACTERS[key] = line
    file += key + " = " + CHARACTERS[key] + "\n"


values = Funciones1.getvalues(KEYWORDS)

file += "#KEYWORDS\n" + "keywords = ["
if KEYWORDS != {}:
    for vals in values:
        file += vals +", "
    file = file[:-2] + "]\n"
else: 
    file += "]\n"

file += "#TOKENS\n"
keys = Funciones1.getkeys(TOKENS)
values = Funciones1.getvalues(TOKENS)
charkeys = Funciones1.getkeys(CHARACTERS)
#print(values)
cont = 0
for val in values:
    expresion = ""
    expresion += keys[cont] + " = "
    expresion += val
    #print(expresion)
    expresion = expresion.replace('"(', ' + ".(')
    expresion = expresion.replace(')"', ')"')
    expresion = expresion.replace('|', ' + "|" + ')
    expresion = expresion.replace('."', '"')
    expresion = expresion.replace("{",' + ".(" +')
    expresion = expresion.replace("}",' + ")*" +')
    expresion = expresion.replace("[",' + ".(" + ')
    expresion = expresion.replace("]",' + ")?" + ')
    expresion = expresion.replace('""', '')
    if expresion.find("EXCEPTKEYWORDS") != -1:
        EXCEPT = expresion[expresion.find("EXCEPTKEYWORDS"): expresion.find("EXCEPTKEYWORDS") + len("EXCEPTKEYWORDS")]
        #print( EXCEPT)
        EXCEPT = ' + "' + EXCEPT + '"'
        expresion = expresion[:expresion.find("EXCEPT")]
        expresion +=  EXCEPT
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
        expresion = initline + 'chr.(" +' +  seccionToProcess[5:] + endline
        #print("line after proccess: " + line)
        expresion.replace('chr("', 'chr(" + ')
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
    file += expresion + "\n"
    cont += 1 

Funciones1.createFile("file", file, ".py")
#print(file)               

#parecera que todo esta bien pero hay que ver que los | tengan concatenacion y al lado de las variables
#hay variables que no tiene el concatenar a su izquierda, por lo que se debe revisar.

    



            
            
