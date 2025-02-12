from random import randint
from random import shuffle
import numpy as np

def headerGen(varCount, conCount, hornex):
    hornex.write(str(varCount) + "\n")
    hornex.write(str(conCount) + "\n")

def printPosRHS(newConstraint, hornex, conDict, vars):
    rhs = randint(1000, 50000)
    posVar = vars[0]
    hornex.write("x" + str(vars[0]))
    slice = vars[1:len(newConstraint)]
    if posVar not in conDict:
        conDict[posVar] = ([], rhs)
    for negVar in slice:
        if negVar not in conDict:
            hornex.write(" - " + "x" + str(negVar))
            conDict[posVar][0].append(negVar)
            continue
        if (posVar in conDict[negVar][0]) and (rhs + conDict[negVar][1] > 0):
            continue
        conDict[posVar][0].append(negVar)
        hornex.write(" - " + "x" + str(negVar))    
    hornex.write(' >= ')
    hornex.write(str(rhs))
    hornex.write("\n")


def prinNegRHS(newConstraint, hornex, conDict, vars):
    rhs = randint(-500000, -100000)
    posVar = vars[0]
    hornex.write("x" + str(vars[0]))
    slice = vars[1:len(newConstraint)]
    if posVar not in conDict:
        conDict[posVar] = ([], rhs)
    for negVar in slice:
        if negVar not in conDict:
            hornex.write(" - " + "x" + str(negVar))
            conDict[posVar][0].append(negVar)
            continue
        if (posVar in conDict[negVar][0]) and (rhs + conDict[negVar][1] > 0):
            continue
        conDict[posVar][0].append(negVar)
        hornex.write(" - " + "x" + str(negVar))    
    hornex.write(' >= ')
    hornex.write(str(rhs))
    hornex.write("\n")


def constraintGen(varCount, hornex, conDict, conCount):
    width = randint(1, varCount)
    vars = [var for var in range(1, varCount + 1)]
    shuffle(vars)
    newConstraint = []
    for i in range(width):
        if (i == 0):
            newConstraint.append(1)
        else:
            newConstraint.append(-1)
    if (randint(0, 10) ==  0):
        printPosRHS(newConstraint, hornex, conDict, vars)
    else:
       prinNegRHS(newConstraint, hornex, conDict, vars)  
