from main import getFileNum
import numpy as np





def convert(inputPath, outputPath, varCount, conCount):
    rhs = []
    coef = np.zeros((varCount, conCount), int)
    with open(inputPath, "r") as inputFile:
        for _ in range(2):
            inputFile.readline()
        i = 0
        for line in inputFile:
            if (i == conCount):
                break
            vars = line.split()
            for cur, next in zip(vars[1:], vars[2:]):
                print(i)
                if vars[0] == '-' and i == 0:
                    coef[int(cur[1:]) - 1][i] = -1
                elif vars[0] == 'x' and i == 0:
                    coef[int(cur[1:]) - 1][i] = 1
                elif (cur == "-"):
                    continue
                elif cur == ">=":
                    rhs.append(next)
                    break
                coef[int(cur[1:]) - 1][i] = -1
            i += 1
    with open(outputPath, "w") as file:
        file.write("NAME " + file.name + "\n")
        file.write("ROWS\n")
        file.write(" N SUM\n")
        for i in range(conCount):
            file.write(" G con" + str(i) + "\n")
        file.write("COLUMNS\n")
        for var in range(varCount):
            for con in range(0, conCount, 2):
                if (coef[var][con] == 1 and coef[var][con + 1]):
                    file.write(" x" + str(var + 1) + " con" + str(con + 1) + " 1. con" + str(con + 1))
                    if coef[var][con] == -1:
                        file.write(" -1.\n")
                    else:
                        file.write(" 1.\n")
                elif (coef[var][con] == 1):
                    file.write(" x" + str(var + 1) + " con" + str(con + 1) + " 1. con" + str(con + 1) + "\n")
                    break
                if (coef[var][con] == -1 and coef[var][con + 1]):
                    file.write(" x" + str(var + 1) + " con" + str(con + 1) + " -1. con" + str(con + 1))
                    if coef[var][con] == -1:
                        file.write(" -1.\n")
                    else:
                        file.write(" -1.\n")
                elif (coef[var][con] == -1):
                    file.write(" x" + str(var + 1) + " con" + str(con + 1) + " -1. con" + str(con + 1) + "\n")
                    break
        file.write("RHS\n")
        for i in range(0, conCount, 2):
            if (i == conCount - 1):
                file.write("B con" + str(i + 1) + " " + str(rhs[i]) + ".\n")
                break
            file.write(" B con" + str(i + 1) + " " + str(rhs[i]) + ". con" + str(i + 2) + " " + str(rhs[i + 1]) + "\n")
        file.write("ENDATA")

convert("./systems/hornex.txt", "test.mps", 5, 6)