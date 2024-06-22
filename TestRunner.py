import subprocess
from HCSGenerator import headerGen, constraintGen
from time import sleep
from random import randint
import pandas as pd
def testrunner():
    f = open('hornex.txt', 'w')
    varCount = 10
    conCount = 10
    headerGen(varCount, conCount, f)
    for i in range(10):
        constraintGen(varCount, f)
    f.close()

    subprocess.run(['clang', '-o', 'lift', 'lift.c'])
    proc = subprocess.run(['./lift hornex.txt'], shell=True, capture_output=True)
    # print(proc.stdout.decode())

for i in range(10):
    testrunner()

df = pd.read_csv('timing.csv')

overall = df.drop("feasible", axis=1)

overallMax = overall.max()
overallMin = overall.min()
overallAvg = overall.mean()





feasibleCol = df[df["feasible"] == 1]

infeasibleCol = df[df["feasible"] == 0]

feasibleCol = feasibleCol.drop('feasible', axis=1)


feasibleMax = feasibleCol.max()
feasibleMin = feasibleCol.min()
feasibleAvg = feasibleCol.mean()

infeasibleCol = infeasibleCol.drop('feasible', axis=1)


infeasibleMax = feasibleCol.max()
infeasibleMin = feasibleCol.min()
infeasibleAvg = feasibleCol.mean()


print("total average:")

print(overallAvg.to_string())

print("\n")
print("total max:")

print(overallMax.to_string())

print("\n")

print("total min:")

print(overallMin.to_string())

print("feasible average:")

print(feasibleAvg.to_string())

print("\n")
print("feasible max:")

print(feasibleMax.to_string())

print("\n")

print("feasible min:")

print(feasibleMin.to_string())

print("\n")

print("infeasible average:")

print(infeasibleAvg.to_string())

print("\n")
print("infeasible max:")

print(infeasibleMax.to_string())

print("\n")

print("infeasible min:")

print(infeasibleMin.to_string())


