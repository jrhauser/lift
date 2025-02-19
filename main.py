import subprocess
from newFeasHCSGenerator import headerGen, constraintGen
import pandas as pd
import datetime
import numpy as np
import os
import csv
from pathlib import Path
import multiprocessing
def testRunner(varCount, conCount, timing):
    path = "test_systems/" + str(varCount) + "/" + str(conCount) + "/feasible/"
    directoryContents = os.listdir(path)
    subprocess.run(['gcc', '-std=c99', '-o', 'lift', 'lift.c'])
    for file in directoryContents:
        subprocess.run(["./lift", path + file, timing])
    path = "test_systems/" + str(varCount) + "/" + str(conCount) + "/infeasible/"
    directoryContents = os.listdir(path)
    for file in directoryContents:
        subprocess.run(["./lift", path + file, timing])


def getFileNum(hornPath):
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
    return num



def systemGenerator(varCount, conCount, timing, feasNum):
    systems = feasNum * 2
    i = 0
    hornPath = "test_systems/" + str(varCount) + "/" + str(conCount) + "/feasible/"
    fileNum = getFileNum(hornPath)
    feas = True
    if fileNum == 20:
         hornPath = "test_systems/" + str(varCount) + "/" + str(conCount) + "/infeasible/"
         fileNum = getFileNum(hornPath)
         feas = False
    j = systems - fileNum
    while (i < j):
        fileNum += 1
        if fileNum > 20 and feas:
             fileNum = 1
             feas = False
        elif fileNum > 20 and not feas:
            break
        if feas:
             hornPath = "test_systems/" + str(varCount) + "/" + str(conCount) + "/feasible/"
        else:
             hornPath = "test_systems/" + str(varCount) + "/" + str(conCount) + "/infeasible/"
             os.makedirs(hornPath, exist_ok=True)
        fullPath = hornPath + str(varCount) + "_" + str(conCount) + "_" + str(fileNum) + ".txt"
        hornex = open(fullPath, 'w+')
        headerGen(varCount, conCount, hornex)
        conTable = []
        for _ in range(conCount):
            constraintGen(varCount, hornex, conTable, conCount)
        hornex.close()
        subprocess.run(['./lift', hornex.name, timing])
        df = pd.read_csv(timing)
        feasibleCol = df['feasible'].tolist()
        i += 1
        if (feas and feasibleCol[-1] == 0):
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
            fileNum -= 1
        elif (not feas and feasibleCol[-1] == 1):
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
            fileNum -= 1
        




def statsGenerator(timing, conCount):
            df = pd.read_csv(timing)
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
            
            
            
            #ratio = feasibleCol.size / df.size
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
            f.close()


def testRun():
    for varCount in varCounts:
        for conCount in varCount:
            p = "timing/" + datetime.datetime.now().strftime("%Y_%m_%d/")
            os.makedirs(p, exist_ok=True)
            f = open(p + str(conCount[0]) + "_vars_" + str(conCount[1]) + "_cons.csv", 'w+')
            f.write("feasible,beginning_to_start,start_to_solution,total,zero_solution,lifts\n")
            timing = f.name
            f.close()
            for _ in range(testRuns): 
                testRunner(conCount[0], conCount[1], timing) 
            statsGenerator(timing, conCount)






def procLoop(varCount):
    for conCount in varCount:
            p = "generatorTiming" + str(timingNum) +"/" + datetime.datetime.now().strftime("%Y_%m_%d/")
            os.makedirs(p, exist_ok=True)
            with open(p + str(conCount[0]) + "_vars_" + str(conCount[1]) + "_cons.csv", 'w+') as timing:
                timing.write("feasible,beginning_to_start,start_to_solution,total,zero_solution,lifts\n")
            systemGenerator(conCount[0], conCount[1], timing.name, testRuns)


def multiProcGenerate():
    processes = []
    for varCount in varCounts:
        p = multiprocessing.Process(target=procLoop, args=(varCount,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()


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
        (1000, 4500)
    ]
thousandsPT2 = [
        (1000, 10000),
        (1000, 1000000)
    ]
twoThousand = [
        (2000, 5000),
        (2000, 4000)
    ]
twoThousandPT2 = [
        (2000, 22000),
        (2000, 4000000)
    ]
fiveThousand = [
        (5000, 5000),
        (5000, 10000)
    ]
fiveThousand1 = [
        (5000, 60000),
        (5000, 25000000)
    ]
fiveThousand2 = [
        (5000, 25000000)
    ]
#varCounts = [fiveHundreds, thousands, thousandsPT2, twoThousand, twoThousandPT2, fiveThousand, fiveThousand1, fiveThousand2]
varCounts = [hundreds]
testRuns = 1
timingNum = 1


if __name__ == "__main__":
    # multiProcGenerate()
    testRun()