from random import randrange
from random import randint
from random import shuffle


def headerGen(varCount, conCount, hornex):
    hornex.write(str(varCount) + "\n")
    hornex.write(str(conCount) + "\n")

def constraintGen(varCount, hornex):
    width = randint(1, varCount)
    con = [var for var in range(1, varCount + 1)]
    shuffle(con)
    for i in range(width):
        if (i == 0):
            if (width == 1):
                hornex.write('x' + str(con[i]))
            else:
                hornex.write('x' + str(con[i]) + ' - ')
        elif (i < width - 1):
            hornex.write('x' + str(con[i]) + ' - ')
        else:
            hornex.write('x' + str(con[i]))
    hornex.write(' >= ')
    if (randint(0, 1) == 1):
        hornex.write(str(randint(-50000, -5000)))
    else:
        hornex.write(str(randint(5000, 10000)))
    hornex.write('\n')
