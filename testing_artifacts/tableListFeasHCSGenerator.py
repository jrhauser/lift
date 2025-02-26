from random import randint
from random import shuffle
import numpy as np

def headerGen(varCount, conCount, hornex):
    hornex.write(str(varCount) + "\n")
    hornex.write(str(conCount) + "\n")

def printPosRHS(newConstraint, hornex, conTable, vars):
    rhs = randint(1000, 5000)
    posVar = vars[0]
    hornex.write("x" + str(vars[0]))
    slice = vars[1:len(newConstraint)]
    conTable.append(([] , rhs))
    for i in slice:
        bad = False
        for conEntry in conTable:
            if ((posVar in conEntry[0]) and (rhs + conEntry[1] > 0)):
                bad = True
                break
        if (bad):
            continue
        conTable[-1][0].append(i)
        hornex.write(" - " + "x" + str(i))    
    hornex.write(' >= ')
    hornex.write(str(rhs))
    hornex.write("\n")


def prinNegRHS(newConstraint, hornex, conTable, vars):
    rhs = randint(-5000, -1000)
    posVar = vars[0]
    hornex.write("x" + str(vars[0]))
    slice = vars[1:len(newConstraint)]
    conTable.append(([] , rhs))
    for i in slice:
        bad = False
        for conEntry in conTable:
            if ((posVar in conEntry[0]) and (rhs + conEntry[1] > 0)):
                bad = True
                break
        if (bad):
            continue
        conTable[-1][0].append(i)
        hornex.write(" - " + "x" + str(i))    
    hornex.write(' >= ')
    hornex.write(str(rhs))
    hornex.write("\n")


def constraintGen(varCount, hornex, conTable, conCount):
    width = randint(1, varCount)
    vars = [var for var in range(1, varCount + 1)]
    shuffle(vars)
    newConstraint = []
    for i in range(width):
        if (i == 0):
            newConstraint.append(1)
        else:
            newConstraint.append(-1)
    if (randint(0, conCount // 5) ==  0):
        prinNegRHS(newConstraint, hornex, conTable, vars)      
    else:
       printPosRHS(newConstraint, hornex, conTable, vars) 