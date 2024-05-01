

# read json file under same directory
import json
import os
import sys
import time
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPT_DIR = SCRIPT_DIR + "/../constraintPackage/cache/gas"
# read json file
def readJsonFile(fileName):
    with open(fileName, 'r') as f:
        data = json.load(f)
    return data

# write json file
def writeJsonFile(fileName, data):
    with open(fileName, 'w') as f:
        json.dump(data, f)

benchmarks = ["HarmonyBridge", "Harvest1_fUSDT", "CreamFi2_1", "BeanstalkFarms"]
invariants = ["EOA", "GC", "OB", "DF"]

for benchmark in benchmarks:
    
    # original gas
    fileName = SCRIPT_DIR + '/' + benchmark  + '.json'
    testingSetMap = readJsonFile(fileName)
    
    # EOA gas
    fileName = SCRIPT_DIR + '/' + benchmark  + '_EOA.json'
    testingSetMap_EOA = readJsonFile(fileName)

    # GC gas
    testingSetMap_GC = None
    fileName = SCRIPT_DIR + '/' + benchmark  + '_GC.json'
    if os.path.exists(fileName):
        testingSetMap_GC = readJsonFile(fileName)

    # OB gas
    fileName = SCRIPT_DIR + '/' + benchmark  + '_OB.json'
    testingSetMap_OB = readJsonFile(fileName)

    # DF gas
    fileName = SCRIPT_DIR + '/' + benchmark  + '_DF.json'
    testingSetMap_DF = readJsonFile(fileName)

    # OB or DFU gas
    fileName = SCRIPT_DIR + '/' + benchmark  + '_OBorDFU.json'
    testingSetMap_OBorDFU = readJsonFile(fileName)

    totalGas = 0
    totalGas_EOA = 0
    totalGas_GC = 0
    totalGas_OB = 0
    totalGas_DF = 0
    totalGas_OBorDFU = 0

    for tx in testingSetMap:
        totalGas += testingSetMap[tx]

        if tx in testingSetMap_EOA:
            totalGas_EOA += testingSetMap_EOA[tx]
        else:
            totalGas_EOA += testingSetMap[tx]

        if tx in testingSetMap_OB:
            totalGas_OB += testingSetMap_OB[tx]
        else:
            totalGas_OB += testingSetMap[tx]
        if testingSetMap_GC != None:
            if tx in testingSetMap_GC:
                totalGas_GC += testingSetMap_GC[tx]
            else:
                totalGas_GC += testingSetMap[tx]

        if tx in testingSetMap_DF:
            totalGas_DF += testingSetMap_DF[tx]
        else:
            totalGas_DF += testingSetMap[tx]
        

        # if tx in testingSetMap_OB:
        #     if testingSetMap_OB[tx] - testingSetMap[tx] > 100:
        #         print("OB gas is larger than original gas")
        #         print(testingSetMap_OB[tx])
        #         print(testingSetMap[tx])

        if tx in testingSetMap_OBorDFU:
            totalGas_OBorDFU += testingSetMap_OBorDFU[tx]

        elif tx in testingSetMap_OB:
            totalGas_OBorDFU += testingSetMap_OB[tx]


        else:
            totalGas_OBorDFU += testingSetMap[tx]

        # if tx in testingSetMap_OB and tx in testingSetMap_OBorDFU:
        #     x = testingSetMap_OB[tx]
        #     y = testingSetMap_OBorDFU[tx]
        #     if x >  y:
        #         sys.exit("OB gas is larger than OBorDFU gas")


    print(benchmark)

    print("totalGas: " + str(totalGas))
    print("totalGas_EOA: " + str(totalGas_EOA))
    print("totalGas_OB: " + str(totalGas_OB))
    print("totalGas_GC: " + str(totalGas_GC))
    print("totalGas_DF: " + str(totalGas_DF))
    print("totalGas_OBorDFU: " + str(totalGas_OBorDFU))

    print("average overhead EOA: " + str((totalGas_EOA - totalGas) / totalGas * 100))
    print("average overhead OB: " + str((totalGas_OB - totalGas) / totalGas * 100))

    if benchmark == "BeanstalkFarms":
        print("average overhead GC: None (Vyper does not support )")
        totalGas_GC = totalGas
    else:
        print("average overhead GC: " + str((totalGas_GC - totalGas) / totalGas * 100))

    print("average overhead DF: " + str((totalGas_DF - totalGas) / totalGas * 100))

    print("average overhead Combined for EOA and GC and DFU: " + str((totalGas_EOA - totalGas + totalGas_GC - totalGas + totalGas_DF - totalGas) / totalGas * 100))

    print("average overhead Combined for EOA and (OB or DFU): " + str((totalGas_EOA - totalGas + totalGas_OBorDFU - totalGas) / totalGas * 100))

    print("")

# fileName = SCRIPT_DIR + '/HarmonyBridge_EOA.json'
# data = readJsonFile(fileName)
# print(data)