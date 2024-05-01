import sys
import os
from parserPackage.locator import *
from Benchmarks_Traces.detectTrace import *
import copy
from trackerPackage.dataSource import *
from fetchPackage.fetchTrace import fetcher 
from crawlPackage.crawlQuicknode import CrawlQuickNode
from crawlPackage.crawlEtherscan import CrawlEtherscan
from constraintPackage.txCounterHelper import *
from utilsPackage.compressor import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import toml
settings = toml.load("settings.toml")
proportion = settings["experiment"]["trainingSetRatio"] # how much transactions used as traning set






def printFPMap(invariantMap, FPMap, benchmarkName):

    invariants = ['NonReentrantLocks']

    print(invariants)

    if invariantMap["NonReentrantLocks"] is False:
        print("N/A\t", end = "")
    else:
        print("{}\t".format(len(FPMap["NonReentrantLocks"]) ), end ="" )

    print("")

    for invariant in invariants:
        if invariant in FPMap:
            print("5 sampled FPs for {}".format(invariant))
            sampledFPs = sample_five_elements(FPMap[invariant])
            for fp in sampledFPs:
                print(fp)


# check 2 invariants:
# 1. re-entrant locks only on one type of functions - enter or exit
# 2. re-entrant locks on both types of functions - enter and exit
#
# functions regarding token transfers cannot be re-entrant
# for some special cases



def inferReentrancy(accesslistTable, verbose = False):
    
    crawlQuickNode = CrawlQuickNode()
    crawlEtherscan = CrawlEtherscan()

    invariantMapMap = {}

    
    for category, benchmarkName, contract, accessList, exploitTx, l1, l2, l3 in accesslistTable:
        if benchmarkName == "VisorFi":
            exploitTx = "0x69272d8c84d67d1da2f6425b339192fa472898dce936f24818fda415c1c1ff3f"
        if benchmarkName == "Warp_interface2":
            # this benchmark is originally collected but later removed because it is not a victim contract 
            continue


        # if benchmarkName != "RevestFi_interface":
        #     continue
        # elif benchmarkName == "RevestFi":
        #     pass
        # else:
        #     continue


        enterFunction, exitFunction = benchmark2EnterExitFuncs(benchmarkName)

        print("====== benchmark {}: ".format(benchmarkName))
        tokenInFunctions = enterFunction
        tokenOutFunctions = exitFunction

        tokenMoveFunctions = tokenInFunctions + tokenOutFunctions
        tokenMoveFunctions = list(set(tokenMoveFunctions))
        

# check 1 invariant:
# 1. re-entrant locks on both types of functions - enter and exit

# functions regarding token transfers cannot be re-entrant
# for some special cases
        # stage 1: training

        lastTokenMove = (0, [])
        #   (transaction, [ (structLogsStart, structLogsEnd), ... ] )

        invariantMap = {
            "NonReentrantLocks": len(tokenInFunctions) >  0 or len(tokenOutFunctions) > 0,
        }

        counter = -1

        txList = []
        for tx, funcCallList in accessList:
            counter += 1
            if tx not in txList:
                txList.append(tx)

            if len(funcCallList) != 1:
                print(funcCallList)
                sys.exit("access control infer: not one function call in a transaction")

            for funcCall in funcCallList[0]:
                name = ""
                if "name" in funcCall:
                    name += funcCall["name"]
                    if funcCall["name"] not in tokenMoveFunctions:
                        continue

                structLogsStart = funcCall["structLogsStart"]
                structLogsEnd = funcCall["structLogsEnd"]

                if name in tokenMoveFunctions:
                    if tx == lastTokenMove[0]:
                        for oldStructLogsStart, oldStructLogsEnd, oldName in lastTokenMove[1]:
                            if (structLogsStart > oldStructLogsStart and structLogsEnd < oldStructLogsEnd) or \
                                (oldStructLogsStart > structLogsStart and oldStructLogsEnd < structLogsEnd):
                                # find one re-entrancy
                                invariantMap["NonReentrantLocks"] = False
                            
                            if structLogsStart == oldStructLogsStart and structLogsEnd == oldStructLogsEnd and name == oldName:
                                # find one re-entrancy
                                print("now is the time")
                        lastTokenMove[1].append((structLogsStart, structLogsEnd, name))
                    else:
                        lastTokenMove = (tx, [ (structLogsStart, structLogsEnd, name) ])


            if len(txList) > benchmark2txCount(benchmarkName) * proportion:
                counter += 1
                break
        

        # # store training set for each benchmark
        # path = SCRIPT_DIR + "/cache/trainingSet/{}.pickle".format(benchmarkName)
        # writeList(path, txList)

        # stage 2: infer
        # functions regarding token transfers cannot be re-entrant
        # for some special cases
        

        print("==invariant list: ")
        print(invariantMap)

        

        # stage 3: validation
        FPMap = {
            "NonReentrantLocks": [],
        }
        
        txList2 = []
        for ii, (tx, funcCallList) in enumerate(accessList[counter:]):
            currentIndex = ii + counter
            if tx not in txList2:
                txList2.append(tx)

            if tx == exploitTx:
                # # store testing set for each benchmark
                # path = SCRIPT_DIR + "/cache/testingSet/{}.pickle".format(benchmarkName)
                # writeList(path, txList2)

                isFiltered = False
                for funcCall in funcCallList[0]:
                    name = ""
                    if "name" in funcCall:
                        name += funcCall["name"]
                        if funcCall["name"] not in tokenMoveFunctions:
                            continue
                        
                    structLogsStart = funcCall["structLogsStart"]
                    structLogsEnd = funcCall["structLogsEnd"]


                    if invariantMap["NonReentrantLocks"] and name in tokenMoveFunctions:
                        if tx == lastTokenMove[0]:
                            for oldStructLogsStart, oldStructLogsEnd, oldName in lastTokenMove[1]:
                                if (structLogsStart > oldStructLogsStart and structLogsEnd < oldStructLogsEnd) or \
                                    (oldStructLogsStart > structLogsStart and oldStructLogsEnd < structLogsEnd):
                                    # find one re-entrancy
                                    isFiltered = True
                                    print("old name: {}, old structLogsStart: {}, old structLogsEnd: {}".format(oldName, oldStructLogsStart, oldStructLogsEnd))
                                    print("new name: {}, new structLogsStart: {}, new structLogsEnd: {}".format(name, structLogsStart, structLogsEnd))
                                    print("Successfully stops the exploit using MoveNonReentrantLocks")

                                    if structLogsStart == oldStructLogsStart and structLogsEnd == oldStructLogsEnd and name == oldName:
                                        # find one re-entrancy
                                        print("now is the time")
                            lastTokenMove[1].append((structLogsStart, structLogsEnd, name))
                        else:
                            lastTokenMove = (tx, [ (structLogsStart, structLogsEnd, name) ])
                    


                if len(accessList) == currentIndex + 1 or accessList[currentIndex + 1][0] != exploitTx:
                    print("exploitTx: ", exploitTx)
                    print("FPMap: ", end="")
                    printFPMap(invariantMap, FPMap, benchmarkName)
                    if benchmarkName == "Nomad":
                        print(FPMap)
                    break
            
            else:
                for funcCall in funcCallList[0]:
                    name = ""
                    if "name" in funcCall:
                        name += funcCall["name"]
                    # if "Selector" in funcCall:
                    #     name += funcCall["Selector"]
                    if name not in invariantMap and invariantMap["NonReentrantLocks"] is False:
                        continue

                    structLogsStart = funcCall["structLogsStart"]
                    structLogsEnd = funcCall["structLogsEnd"]

                    if invariantMap["NonReentrantLocks"] and name in tokenMoveFunctions:
                        if tx == lastTokenMove[0]:
                            for oldStructLogsStart, oldStructLogsEnd, oldName in lastTokenMove[1]:
                                if (structLogsStart > oldStructLogsStart and structLogsEnd < oldStructLogsEnd) or \
                                    (oldStructLogsStart > structLogsStart and oldStructLogsEnd < structLogsEnd):
                                    print("old name: {}, old structLogsStart: {}, old structLogsEnd: {}".format(oldName, oldStructLogsStart, oldStructLogsEnd))
                                    print("new name: {}, new structLogsStart: {}, new structLogsEnd: {}".format(name, structLogsStart, structLogsEnd))
                                    print("tx: {}".format(tx))
                                    if tx not in FPMap["NonReentrantLocks"]:
                                        FPMap["NonReentrantLocks"].append(tx)
                                
                                if structLogsStart == oldStructLogsStart and structLogsEnd == oldStructLogsEnd and name == oldName:
                                    # find one re-entrancy
                                    print("now is the time")
                                    
                            lastTokenMove[1].append((structLogsStart, structLogsEnd, name))
                        else:
                            lastTokenMove = (tx, [ (structLogsStart, structLogsEnd, name) ])

                    

