from random import randrange
from random import randint
from random import shuffle


def headerGen(varCount, conCount, f):
    f.write(str(varCount) + "\n")
    f.write(str(conCount) + "\n")

def constraintGen(varCount, f):
    width = randint(1, varCount)
    con = [var for var in range(1, varCount + 1)]
    shuffle(con)
    for i in range(width):
        if (i == 0):
            neg = randint(0, 1)
            if (neg == 1):
                if (width == 1):
                    f.write('-x' + str(con[i]))
                else:
                    f.write('-x' + str(con[i]) + ' - ')
            else:
                if (width == 1):
                    f.write('x' + str(con[i]))
                else:
                    f.write('x' + str(con[i]) + ' - ')
        elif (i < width - 1):
            f.write('x' + str(con[i]) + ' - ')
        else:
            f.write('x' + str(con[i]))
    f.write(' >= ')
    f.write(str(randint(-1000, 1000)))
    f.write('\n')
