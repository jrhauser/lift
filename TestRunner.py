import subprocess
from HCSGenerator import headerGen, constraintGen
from time import sleep
from random import randint
import pandas as pd
def testrunner(varCount, conCount):
    hornex = open('hornex.txt', 'w')
    headerGen(varCount, conCount, hornex)
    for i in range(conCount):
        constraintGen(varCount, hornex)
    hornex.close()
    subprocess.run(['clang', '-o', 'lift', 'lift.c'])
    proc = subprocess.run(['./lift hornex.txt'], shell=True)
    # print(proc.stdout.decode())


varCount = 100
conCount = 100
testRuns = 10
with open('timing.csv', 'w', newline='') as statsCSV:
    statsCSV.write("feasible,beginning_to_start,start_to_solution,total\n")

for i in range(testRuns):
    testrunner(varCount, conCount)

df = pd.read_csv('timing.csv')
feasibleCol = df[df['feasible'] == 1]

infeasibleCol = df[df['feasible'] == 0]
overall = df.drop('feasible', axis=1)

overallMax = overall.max()
overallMin = overall.min()
overallAvg = overall.mean()







feasibleCol = feasibleCol.drop('feasible', axis=1)


feasibleMax = feasibleCol.max()
feasibleMin = feasibleCol.min()
feasibleAvg = feasibleCol.mean()

infeasibleCol = infeasibleCol.drop('feasible', axis=1)


print(infeasibleCol)

infeasibleMax = infeasibleCol.max()
infeasibleMin = infeasibleCol.min()
infeasibleAvg = infeasibleCol.mean()

f = open("stats.txt", "a")
f.write("------------------------\n")
f.write("Variables: " + str(varCount) + "\n")
f.write("Constraints: " + str(conCount) + "\n")

f.write("total average: ")
f.write("\n")
f.write(overallAvg.to_string() + "\n")

f.write("\n")
f.write("total max:")
f.write("\n")
f.write(overallMax.to_string() + "\n")

f.write("\n")

f.write("total min:")
f.write("\n")
f.write(overallMin.to_string() + "\n")

f.write("feasible average:")
f.write("\n")
f.write(feasibleAvg.to_string() + "\n")

f.write("\n")
f.write("feasible max:")
f.write("\n")
f.write(feasibleMax.to_string() + "\n")

f.write("\n")

f.write("feasible min:" )
f.write("\n")
f.write(feasibleMin.to_string() + "\n")

f.write("\n")

f.write("infeasible average:")
f.write("\n")
f.write(infeasibleAvg.to_string() + "\n")

f.write("\n")
f.write("infeasible max:")
f.write("\n")
f.write(infeasibleMax.to_string() + "\n")

f.write("\n")

f.write("infeasible min:")
f.write("\n")
f.write(infeasibleMin.to_string() + "\n")

f.write("--------------------------")
