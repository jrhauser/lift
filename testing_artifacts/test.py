import subprocess
from genTest import headerGen, constraintGen
import pandas as pd
import datetime
import numpy as np
import os
def testrunner(varCount, conCount, filename):
    hornex = open('hornextest.txt', 'w')
    headerGen(varCount, conCount, hornex)
    conTable = []
    for i in range(conCount):
        constraintGen(varCount, hornex, conTable, conCount)
    hornex.close()
    subprocess.run(['gcc', '-std=c99', '-o', 'lift', 'lift.c'])
    proc = subprocess.run([str('./lift hornextest.txt ' + filename)], shell=True)






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
        #(500, 250000)
    ]
thousands = [
        (1000, 2000),
        (1000, 4500),
        (1000, 10000),
        #(1000, 1000000)
    ]
twoThousand = [
        (2000, 5000),
        (2000, 4000),
        (2000, 22000),
       # (2000, 4000000)
    ]
fiveThousand = [
        (5000, 5000),
        (5000, 10000),
        (5000, 60000),
       # (5000, 25000000)
    ]
varCounts = [hundreds, twoHundreds]
testRuns = 1
for varCount in varCounts:
    for conCount in varCount:
            with open("testing.csv", "w") as statsCSV:
                statsCSV.write("feasible,beginning_to_start,start_to_solution,total,zero_solution,lifts\n")
            for i in range(testRuns): 
                testrunner(conCount[0], conCount[1], statsCSV.name)
         

            df = pd.read_csv(statsCSV.name)
            feasibleCol = df[df['feasible'] == 1]

            infeasibleCol = df[df['feasible'] == 0]

            zeroCol = df[df['zero_solution'] == 1]

            overall = df.drop('feasible', axis=1)

            overallMax = overall["start_to_solution"].max()
            overallMin = overall["start_to_solution"].min()
            overallAvg = overall["start_to_solution"].mean()




            feasibleCol = feasibleCol.drop('feasible', axis=1)


            feasibleMax = feasibleCol["start_to_solution"].max()
            feasibleMin = feasibleCol["start_to_solution"].min()
            feasibleAvg = feasibleCol["start_to_solution"].mean()



            infeasibleCol = infeasibleCol.drop('feasible', axis=1)

            infeasibleMax = infeasibleCol["start_to_solution"].max()
            infeasibleMin = infeasibleCol["start_to_solution"].min()
            infeasibleAvg = infeasibleCol["start_to_solution"].mean()
            
            
            zero_max = zeroCol["start_to_solution"].max()
            zero_min = zeroCol["start_to_solution"].min()
            zero_avg = zeroCol["start_to_solution"].mean()
            
            
            
            ratio = feasibleCol.size /  df.size
            print(ratio)
           # print(df[df['zero_solution'] == 1].size / feasibleCol.size)

            f = open("stats.csv", "a+")
            f.write(str(testRuns) + ',')
            f.write(str(conCount[0]) + ",")
            f.write(str(conCount[1]) + ',')
            f.write(str(datetime.datetime.now()) + ",")
            f.write(str(overallAvg) + ",")
            f.write(str(overallMax) + ",")
            f.write(str(overallMin) + ",")
            f.write(str(feasibleAvg) + ",")
            f.write(str(feasibleMax) + ",")
            f.write(str(feasibleMin) + ",")
            f.write(str(infeasibleAvg) + ",")
            f.write(str(infeasibleMax) + "," + str(infeasibleMin) + "," + str(zero_max) + "," + str(zero_min) + ',' +  str(zero_avg) +"\n")
            statsCSV.close()
            f.close()