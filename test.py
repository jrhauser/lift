from feasHCSGenerator import headerGen, constraintGen

hornex = open('hornextest.txt', 'w')
headerGen(100, 100, hornex)
for i in range(100):
    constraintGen(100, hornex)
hornex.close()