import subprocess
from generator import headerGen, constraintGen
import pandas as pd
import datetime
import subprocess
import os
import multiprocessing

""" 
Main test run function, loops through provided loop of var constraint value pairs and calls testRunner
Then calls statsRunner to compile the result stats

No params

NOTE: Overwrites the result data every day, this means the tests data that is preserved is the last one executed on a given day, 
        the results can be put into the stats file before being destroyed entirely if statsRunner is called
"""
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

""" 
Test runner function, loops through file directory "systems" and executes the c algorithm on each test file using python's subprocess

Params: 
    varCount - the number of variables to be tested 
    conCount - the number of constraints to be tested 
    timing - a csv file where the timing results will be stored
NOTE: The c file is compiled every time just to be safe an
"""
def testRunner(varCount, conCount, timing):
    path = "systems/" + str(varCount) + "/" + str(conCount) + "/feasible/"
    directoryContents = os.listdir(path)
    subprocess.run(['gcc', '-std=c99', '-o', 'lift', 'lift.c'])
    for file in directoryContents:
        subprocess.run(["./lift", path + file, timing])
    path = "systems/" + str(varCount) + "/" + str(conCount) + "/infeasible/"
    directoryContents = os.listdir(path)
    for file in directoryContents:
        subprocess.run(["./lift", path + file, timing])

""" 
Stats generator function, reads the provided timing file and generates statistics based off of it's content,  uses pandas

Params: 
    timing - the csv file to be analyzed 
    conCount - bit of a misnomer, its actually a tuple containing the var count and con count, so something like (100, 700)
"""
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
            
            
            #left in so I could see the ratio of feasible to infeasible systems
            
            #ratio = feasibleCol.size / df.size
            #print(df[df['zero_solution'] == 1].size / feasibleCol.size)

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

""" 
Helper function to get the number of a horn file in the testing set located in the systems directory

Params: 
    hornPath - the subdirectory that this function should go looking for numbers in text file names. Should be the systems directory in the format
        "systems/'# of vars'/'# of cons'/feasible/" or "systems/'# of vars'/'# of cons'/infeasible/"
NOTE: only supports files with a maximum of 2 digit numbers for ID
"""
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

""" 
System generator function to create test systems. Uses the existing file numbers to determine which number and how many system files to generate.
Calls the generator.py file to generate the header and each constraint. This seems weird but I actually need to maintain a dictionary throughout the file generation process so it works out
Params: 
        varCount - number of variables for each generated system 
        conCount - number of constraints for each generated system
        timing - csv file to capture the results
            (this is a bit hacky but its how I know a system is feasible)
        feasNum - the number of each type (feasible or infeasible) system to generate. This can be thought of as the upper limit to how many systems this function will make.
            If there are already n systems in the folder it will generate n+1 to feasNum files per type

NOTE: if it generates a feasible system when it wants an infeasible system or vice versa, I do the incredibly lazy thing and just try again deleting the old one.
        This should probably be fixed, but they only need to be made once
"""
def systemGenerator(varCount, conCount, timing, feasNum):
    systems = feasNum * 2
    i = 0
    hornPath = "systems/" + str(varCount) + "/" + str(conCount) + "/feasible/"
    fileNum = getFileNum(hornPath)
    feas = True
    if fileNum == feasNum:
         hornPath = "systems/" + str(varCount) + "/" + str(conCount) + "/infeasible/"
         fileNum = getFileNum(hornPath)
         feas = False
    j = systems - fileNum
    while (i < j):
        fileNum += 1
        if fileNum > feasNum and feas:
             fileNum = 1
             feas = False
        elif fileNum > feasNum and not feas:
            break
        if feas:
             hornPath = "systems/" + str(varCount) + "/" + str(conCount) + "/feasible/"
        else:
             hornPath = "systems/" + str(varCount) + "/" + str(conCount) + "/infeasible/"
             os.makedirs(hornPath, exist_ok=True)
        fullPath = hornPath + str(varCount) + "_" + str(conCount) + "_" + str(fileNum) + ".txt"
        hornex = open(fullPath, 'w+')
        headerGen(varCount, conCount, hornex)
        
        varDict = {}
        for _ in range(conCount):
            constraintGen(varCount, conCount, hornex, varDict)
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

""" 
procLoop - The function I call when multiprocessing. This splits up each file generation task by variable and constraint number. Makes a new folder for the generator timing since it is 
basically only used to read feasibility
Params: 
        varCount - again a bit of a misnomer it's actually an array of tuples containing the # of vars and # of constraints to be generated the structure is like
        [(100, 100), (100, 200) ...] where the first entry in the tuple is the var count and the second is the constraint count 

NOTE: Overwrites the result data every day, again not an issue because it is only used for testing feasibility but its good to know
"""
def procLoop(varCount):
    for conCount in varCount:
            p = "generatorTiming" + str(timingNum) +"/" + datetime.datetime.now().strftime("%Y_%m_%d/")
            os.makedirs(p, exist_ok=True)
            with open(p + str(conCount[0]) + "_vars_" + str(conCount[1]) + "_cons.csv", 'w+') as timing:
                timing.write("feasible,beginning_to_start,start_to_solution,total,zero_solution,lifts\n")
            systemGenerator(conCount[0], conCount[1], timing.name, 20)

""" 
multiProcGenerate - The function I call to start multiprocessing. This splits up each file generation task by entry in the varCounts array. More entries in the array = more processes
more granular control is possible, I could create a child process for each file being generated, currently I split it up by var count and con count. This means each process is 
required to create at most 40 versions of its designated var/con pair.
Params: 
       None
NOTE: This slows my PC down a lot, and unfortunately I can't find a good way to stop and come back to file generation, currently being considered, but it may just need to be offloaded to a server somewhere
so I can play league of legends
"""
def multiProcGenerate():
    processes = []
    for varCount in varCounts:
        p = multiprocessing.Process(target=procLoop, args=(varCount,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

"""
Arrays containing the variable constraint pairs determined to be researched. 
Each array corresponds to a variable count and each tuple in the array contains the variable count and the constraint count conviently named to match the variable names to make testing pieces easier
NOTE: A few variables have been split into parts eg. "thousands" and "thousandsPT2", this is to further divide the workload of creating the files.
"""
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

"""
varCounts - An array containing all of the varaible counts to be tested or generated. Each has a name so I can quickly add and delete them with VIM when working over SSH. 
See above comment for more information.
"""
# varCounts = [fiveHundreds, thousands, thousandsPT2, twoThousand, twoThousandPT2, fiveThousand, fiveThousand1, fiveThousand2]
varCounts = [hundreds]

"""
systemsCount - determines the maximum number of systems to be generated
timingNum - gives an arbitrary integer to slap on the end of the timing folders when generating systems, pretty sure it's deprecated
testRuns - number of times to test each system
"""
systemsCount = 20
timingNum = 1
testRuns = 1
"""
I guess this is python for "the part of the code that only the parent process runs." That's why it has two lines, one commented out.
Both functions are explained above, but the tldr is multiProcGenerate() makes the systesms using multi processing and testRun tests those systems generating runtime stats
"""
if __name__ == "__main__":
    multiProcGenerate()
    # testRun()
