from random import randint
from random import shuffle
from random import sample

def headerGen(varCount, conCount, hornex):
    hornex.write(str(varCount) + "\n")
    hornex.write(str(conCount) + "\n")

def constraintGen(varCount, hornex):
    width = randint(1, varCount)
    lhs = sample(range(0, 1000), varCount)
    con = [var for var in range(1, varCount + 1)]
    lhs = list(zip(con, lhs))
    shuffle(con)
    rhs = 0
    for i in range(width):
        if (i == 0):
            neg = randint(0, 1)
            if (neg == 1):
                if (width == 1):
                    hornex.write('-x' + str(con[i]))
                    rhs -= lhs[con[i] - 1][1]
                else:
                    hornex.write('-x' + str(con[i]) + ' - ')
                    rhs -= lhs[con[i] - 1][1]
            else:
                if (width == 1):
                    hornex.write('x' + str(con[i]))
                    rhs += lhs[con[i] - 1][1]
                else:
                    hornex.write('x' + str(con[i]) + ' - ')
                    rhs += lhs[con[i] - 1][1]
        elif (i < width - 1):
            rhs -= lhs[con[i] - 1][1]
            hornex.write('x' + str(con[i]) + ' - ')
        else:
            hornex.write('x' + str(con[i]))
            rhs -= lhs[con[i] - 1][1]
    print(lhs)
    hornex.write(' >= ')
    hornex.write(str(rhs))
    hornex.write('\n')
