import subprocess
from newFeasHCSGeneratorTest import headerGen, constraintGen
import pandas as pd
import datetime
import numpy as np
import os
import csv

def testTestRunner(varCount, conCount, timing):
    hornex = open('hornex.txt', 'w+')
    headerGen(varCount, conCount, hornex)
    conDict = {}
    for i in range(conCount):
        constraintGen(varCount, hornex, conDict, conCount)
    hornex.close()
    subprocess.run(['gcc', '-std=c99', '-o', 'lift', 'lift.c'])
    proc = subprocess.run([str('./lift hornex.txt ' + timing)], shell=True)



def testRunner(varCount, conCount, timing):
    for hornex in os.listdir("test_systems_test/" + str(varCount) + "/" + str(conCount) + "/feasible/"):
            subprocess.run(['gcc', '-std=c99', '-o', 'lift', 'lift.c'])
            subprocess.run([str('./lift hornex.txt ' + timing)])
            hornex.close()


def testRunner(varCount, conCount, timing):
    hornex = open('hornex.txt', 'w+')
    headerGen(varCount, conCount, hornex)
    conDict = {}
    for i in range(conCount):
        constraintGen(varCount, hornex, conDict, conCount)
    hornex.close()
    subprocess.run(['gcc', '-std=c99', '-o', 'lift', 'lift.c'])
    subprocess.run([str('./lift hornex.txt ' + timing)])


def systemGenerator(varCount, conCount, timing, feasNum):
    systems = feasNum 
    i = 0
    while (i < systems):
        if (i < feasNum):
             hornPath = "test_systems_test/" + str(varCount) + "/" + str(conCount) + "/infeasible/"
        else:
             hornPath = "test_systems_test/" + str(varCount) + "/" + str(conCount) + "/feasible/"
        os.makedirs(hornPath, exist_ok=True)
        directoryContents = os.listdir(hornPath)
        num = 0
        fileNums = []
        for file in directoryContents:
            if file[-6] != '_':
                fileNums.append(int(file[-6:-4]))
            else:
                fileNums.append(int(file[-5]))
        fileNums.sort()
        if not fileNums:
            num = 0
        else:
            num = fileNums[-1]
        fullPath = hornPath + str(varCount) + "_" + str(conCount) + "_" + str(num + 1) + ".txt"
        hornex = open(fullPath, 'w+')
        headerGen(varCount, conCount, hornex)
        conDict = {}
        for _ in range(conCount):
            constraintGen(varCount, hornex, conDict, conCount)
        hornex.close()
        subprocess.run(['gcc', '-std=c99', '-o', 'lift', 'lift.c'])
        subprocess.run(['./lift', hornex.name, timing])
        df = pd.read_csv(timing)
        feasibleCol = df['feasible'].tolist()
        i += 1
        if (i > feasNum and feasibleCol[-1] == 0):
            f = open(timing, 'r+')
            lines = f.readlines()
            if len(lines) != 1:
                lines = lines[:-1]
                f.close()
                f = open(timing, 'w+')
                f.writelines(lines)
            f.close()
            os.remove(fullPath)
            i -= 1
        elif (i < feasNum and feasibleCol[-1] == 1):
            f = open(timing, 'r+')
            lines = f.readlines()
            if len(lines) != 1:
                lines = lines[:-1]
                f.close()
                f = open(timing, 'w+')
                f.writelines(lines)
            f.close()
            os.remove(fullPath)
            i -= 1
        




def statsGenerator(timing, testRuns):
            df = pd.read_csv(timing.name)
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
            timing.close()
            f.close()


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
systemsToGenerate = 20
testRuns = 20
for varCount in varCounts:
    for conCount in varCount:
            p = "timing_test/" + datetime.datetime.now().strftime("%Y_%m_%d/")
            os.makedirs(p, exist_ok=True)
            with open(p + str(conCount[0]) + "_vars_" + str(conCount[1]) + "_cons.csv", 'w+') as timing:
                timing.write("feasible,beginning_to_start,start_to_solution,total,zero_solution,lifts\n")
            
            #systemGenerator(conCount[0], conCount[1], timing.name, systemsToGenerate)
            for _ in range(testRuns):
                testTestRunner(conCount[0], conCount[1], timing.name) 
            statsGenerator(timing, testRuns)




