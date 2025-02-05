from random import randint
from random import shuffle
import numpy as np

def headerGen(varCount, conCount, hornex):
    hornex.write(str(varCount) + "\n")
    hornex.write(str(conCount) + "\n")

def printPosRHS(newConstraint, hornex, matrix, varCount, con):
    matrix[con[0] - 1] = np.ones(varCount)
    for x in con:
        if (newConstraint[x - 1] == 1):
            hornex.write("x" + str(x))
        elif (newConstraint[x - 1] == 0):
            if (matrix[x - 1][con[0] - 1] == 1):
                continue
            hornex.write(" - " + "x" + str(x))    
    hornex.write(' >= ')
    hornex.write(str(randint(1000, 5000)))
    hornex.write("\n")


def prinNegRHS(newConstraint, hornex, matrix, varCount, con):
    matrix[con[0] - 1] = np.ones(varCount)
    for x in con:
        if (newConstraint[x - 1] == 1):
            hornex.write("x" + str(x))
        elif (newConstraint[x - 1] == 0):
            if (matrix[x - 1][con[0] - 1] == 1):
                continue
            hornex.write(" - " + "x" + str(x))    
    hornex.write(' >= ')
    hornex.write(str(randint(-10000, -5000)))
    hornex.write("\n")


def constraintGen(varCount, hornex, conCount, matrix):
    width = randint(1, varCount)
    con = [var for var in range(1, varCount + 1)]
    shuffle(con)
    newConstraint = np.zeros(varCount)
    for i in range(width):
        if (i == 0):
            newConstraint[con[i] - 1] = 1
        else:
            newConstraint[con[i] - 1] = -1
        if (randint(0, 5) ==  0):
            printPosRHS(newConstraint, hornex, matrix, varCount, con) 
        else:
            prinNegRHS(newConstraint, hornex, matrix, varCount, con)
