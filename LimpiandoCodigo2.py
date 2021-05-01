import Funciones1 
import Clases

def newFinalStates(subSets, newStates, estadoFinal):
    theNewFinalStates = []
    print(estadoFinal.type())

    cont = 0
    #tomamos conjunto por conjunto
    for conjunto in subSets:
        #se verifica si en dicho conjunto se encuentra cierto estado final
        if estadoFinal in conjunto:
            theNewFinalStates.append(str(newStates[cont]))
        cont += 1
    return theNewFinalStates