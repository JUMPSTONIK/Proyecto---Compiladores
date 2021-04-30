import Funciones1 
import Clases

def CreateAFN(expresion, name = ""):
    metaCaracteres = ["*","+","(",")","|","?","<"]
    operadores = ["*","+","|","?","<"]
    alfabeto = []
    alfabetoNoe = []
    #recibimos la expresion para formar el alfabeto y la cadena para el posfix
    alfabeto, expresion = Funciones1.procesandoAlfabeto(expresion,alfabeto, metaCaracteres)
    #transformamos a posfix
    expresionPosfix = Funciones1.infijoAPosfix(expresion,alfabeto)
    #llamamos la funcion de Thompson para generar las transiciones y obtener el estado
    #inicial y final
    transiciones, estadoFinal, estadoInicial = Funciones1.Thompson(expresionPosfix, alfabeto)
    #obtenemos todos los estados el automata
    estados = Funciones1.getEstados(transiciones, estadoInicial)
    estados.append(estadoFinal)
    #damos forma al Automata en un objeto
    AFN = Clases.Automata(estadoInicial, estadoFinal, estados, alfabeto, transiciones, name)
    #generamos el grafo
    Grafo = Funciones1.crearGrafoDelAutomata(AFN.transiciones, "AFN", estadoFinal)
    return AFN