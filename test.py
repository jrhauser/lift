from newFeasHCSGenerator import headerGen, constraintGen
import numpy as np
hornex = open('hornextest.txt', 'w')
matrix = np.zeros((10, 10))
headerGen(10, 10, hornex)
for i in range(10):
    constraintGen(10, hornex, 10, matrix)
hornex.close()