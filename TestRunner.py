import subprocess
from InfeasHCSGenerator import headerGen, constraintGen
from time import sleep
from random import randint
import pandas as pd
import datetime
import os
def testrunner(varCount, conCount, filename):
    hornex = open('hornex.txt', 'w')
    headerGen(varCount, conCount, hornex)
    for i in range(conCount):
        constraintGen(varCount, hornex)
    hornex.close()
    subprocess.run(['clang', '-o', 'lift', 'lift.c'])
    proc = subprocess.run([str('./lift hornex.txt ' + filename)], shell=True)





hundreds = [
        (100, 100),
        (100, 200),
        (100, 700),
        (100, 10000)
]
twoHundreds = [
        (200, 200),
        (200, 400),
        (200, 1600),
        (200, 40000)
    ]   
fiveHundreds = [
        (500, 500),
        (500, 1000),
        (500, 4500),
        (500, 250000)
    ]
thousands = [
        (1000, 2000),
        (1000, 4500),
        (1000, 10000),
        (1000, 1000000)
    ]
twoThousand = [
        (2000, 5000),
        (2000, 4000),
        (2000, 22000),
        (2000, 4000000)
    ]
fiveThousand = [
        (5000, 5000),
        (5000, 10000),
        (5000, 60000),
        (5000, 25000000)
    ]
varCounts = [[(100, 100)]]
testRuns = 1000
for varCount in varCounts:
    for conCount in varCount:
            p = "timing/" + datetime.datetime.now().strftime("%Y_%m_%d/")
            os.makedirs(p, exist_ok=True)
            with open(p + str(conCount[0]) + "_vars" + str(conCount[1]) + "_cons.csv", "w") as statsCSV:
                statsCSV.write("feasible,beginning_to_start,start_to_solution,total\n")
            for i in range(testRuns): 
                testrunner(conCount[0], conCount[1], statsCSV.name)
         

            df = pd.read_csv(statsCSV.name)
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



            infeasibleMax = infeasibleCol.max()
            infeasibleMin = infeasibleCol.min()
            infeasibleAvg = infeasibleCol.mean()

            f = open("ratio.csv", 'a+')
            f.write("ratio\n")
            ratio = feasibleCol.size /  infeasibleCol.size
            f.write(str(ratio) + '\n')
            print(ratio)
"""
            f = open("stats.txt", "a")
            f.write("------------------------\n")
            f.write(str(datetime.datetime.now()) + '\n')
            f.write("Variables: " + str(conCount[0]) + "\n")
            f.write("Constraints: " + str(conCount[1]) + "\n")

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
            statsCSV.close()
            f.close() """