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
            neg = randint(0, 1)
            if (neg == 1):
                if (width == 1):
                    hornex.write('-x' + str(con[i]))
                else:
                    hornex.write('-x' + str(con[i]) + ' - ')
            else:
                if (width == 1):
                    hornex.write('x' + str(con[i]))
                else:
                    hornex.write('x' + str(con[i]) + ' - ')
        elif (i < width - 1):
            hornex.write('x' + str(con[i]) + ' - ')
        else:
            hornex.write('x' + str(con[i]))
    hornex.write(' >= ')
    hornex.write(str(randint(-10000, 10000)))
    hornex.write('\n')
