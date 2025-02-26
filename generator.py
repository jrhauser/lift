from random import randint
from random import shuffle
import numpy as np

"""
Generates the header for the system file, first line is var count, second is con count
Parameters:
    varCount - variables in this system
    conCount - constraints in this system
    hornex - the file handler to write this header to
"""
def headerGen(varCount, conCount, hornex):
    hornex.write(str(varCount) + "\n")
    hornex.write(str(conCount) + "\n")

"""
Generates the constraint for the system file. Starting with a list of all the variables, shuffling it and then only using the first randomly generated width members of the list.
This function increases the likliehood of feasiability by not allowing positive varables (say xi) who are followed by another neagtive variable (xj) 
to appear negatively in a constraint where xj is positive and their corresponding right hand sides sum greater than one. That's what the dictionary is for. 
By using this method we have acheived ~50% feasibility rate of non trivial random systems. 
The other big area of chance comes in the value and positive or negative nature of each rhs. This also requried tweaking.
Parameters:
    varCount - variables in this system
    conCount - constraints in this system
    hornex - the file handler to write this constraint (line) to
    varDict - a dictionary of integers mapped to tuples of sets and integers used to maintain feasibility in the random system
        structure is:
        {i: ({}, rhs)}
        where i is the variable number (not it's coefficent!)
        () is a tuple
        {} - the first element of the tuple: a set of other variable numbers that have appeared negatively after i
        rhs - the first rhs that the variable i appears positively in
        example would be :
        {1: {3, 5, 6}, 500}
        1 is the varaible number 
        {3, 5, 6} are all the varaibles that have appeared negatively after 1
        500 is the first rhs that 1 appears positively in
NOTE: This only keeps track of the first rhs a variable sees, which could be an issue, but it's supposed to be random anyway so it's not a problem. 
        Also conCount is purely used to help pick the likelihood of a positive or negative rhs, this is more of an art than a science, 
        but I have found proababilites/values that seem to scale well
DIRTY SECRET: I wrote this whole thing with lists and it was so slow, it's still really slow, but lists? really?
"""
def constraintGen(varCount, conCount, hornex, varDict):
    width = randint(1, varCount)
    vars = [var for var in range(1, varCount + 1)]
    shuffle(vars)
    newConstraint = []
    for i in range(width):
        if (i == 0):
            newConstraint.append(1)
        else:
            newConstraint.append(-1)
    rhs = 0
    if (randint(0, conCount // 5) ==  0):
        rhs = randint(-5000, -1000)
    else:
        rhs = randint(1000, 5000)
    posVar = vars[0]
    hornex.write("x" + str(vars[0]))
    slice = vars[1:len(newConstraint)]
    if posVar not in varDict:
        varDict[posVar] = (set(), rhs)
    for negVar in slice:
        if negVar not in varDict[posVar][0]:
            if (varDict[posVar][1] + rhs > 0):
                continue
            hornex.write(" - " + "x" + str(negVar))
            varDict[posVar][0].add(negVar) 
    hornex.write(' >= ')
    hornex.write(str(rhs))
    hornex.write("\n")
