#COMPILER
''''''
#CHARACTERS
ANY = "( |!|#|$|%|&|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~|||||||||||||||||||||||||||||||||| |¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|­|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ)*"
letter = "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|Ã|‘|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|Ã|±|o|p|q|r|s|t|u|v|w|x|y|z)*"
digit = "(0|1|2|3|4|5|6|7|8|9)*"
cr = chr(13)
lf = chr(10)
tab = chr(9)
ignore = cr+lf+tab
comillas = chr(34)
stringletter = ANY-comillas-ignore
operadores = "(+|-|=|(|)|[|]|{|}|||.|<|>)*"
MyANY = ANY-operadores
#KEYWORDS
keywords = []
#TOKENS
ident = letter + "(" +letter + "|" + digit + ")*" + "EXCEPTKEYWORDS"
char = "'" + "(" + "/" + ")?" + letter + "'"
charnumber = "chr(" +digit + "(" +digit + ")*" +")"
charinterval = "chr(" +digit + "(" +digit + ")*" +")chr(" +digit + "(" +digit + ")*" +")"
nontoken = MyANY
startcode = "(."
endcode = ".)"
