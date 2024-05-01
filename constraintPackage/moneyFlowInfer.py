import sys
import os
from parserPackage.locator import *
from parserPackage.parser import proxyMap
from Benchmarks_Traces.detectTrace import *
import copy
from trackerPackage.dataSource import *
from fetchPackage.fetchTrace import fetcher 
from crawlPackage.crawlQuicknode import CrawlQuickNode
from crawlPackage.crawlEtherscan import CrawlEtherscan
from constraintPackage.txCounterHelper import *
from utilsPackage.compressor import *
from parserPackage.decoder import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import toml
settings = toml.load("settings.toml")
proportion = settings["experiment"]["trainingSetRatio"] # how much transactions used as traning set

import numpy as np





def printFPMap(invariantMap, FPMap, benchmarkName):
    invariants = ['tokenInUpperBound', "tokenOutUpperBound", 'tokenInRatioUpperBound', "tokenOutRatioUpperBound"]
    print(invariants)
    for invariant in invariants:
        if invariant in FPMap:
            print("{}\t".format(len(FPMap[invariant]) ), end ="" )
        else:
            print("N/A\t", end = "")
    print("")


    for invariant in invariants:
        if invariant in FPMap:
            print("5 sampled FPs for {}".format(invariant))
            sampledFPs = sample_five_elements(FPMap[invariant])
            for fp in sampledFPs:
                print(fp)


["0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", # 3cRV good! 2 sstores  transferFrom 0, 1
 "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", # USDC good! 2 sstores 
 "0xdac17f958d2ee523a2206206994597c13d831ec7", # USDT good! 2 sstores
 "0x853d955acef822db058eb8505911ed77f175b99e", # Frax good! 2 sstores
 "0x6b175474e89094c44da98b954eedeac495271d0f", # DAI good! 2 sstores
 "0x865377367054516e17014ccded1e7d814edc9ce4", # DOLA good! 2 sstores
 "0xff20817765cb7f73d4bde2e66e067e58d11095c2", # AMP CreamFi1_1
 "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", # UNI good! 2 sstores
 "0x956f47f50a910163d8bf957cf5846d573e7f87ca", # FEI good! 2 sstores
 "0xf938424f7210f31df2aee3011291b658f872e91e", # Visor good! 2 sstores
 "0xb1bbeea2da2905e6b0a30203aef55c399c53d042", # Uniswap UMB4 good! 2 sstores
 "0x56de8bc61346321d4f2211e3ac3c0a7f00db9b76"] # Rena good! 2 sstores

benchmark2token = {
    "BeanstalkFarms": "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", 
    "BeanstalkFarms_interface": None,
    "HarmonyBridge": "ether",
    "HarmonyBridge_interface": "ether",
    "XCarnival": "ether",
    "RariCapital2_1": "ether",
    "RariCapital2_2": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "RariCapital2_3": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "RariCapital2_4": "0x853d955acef822db058eb8505911ed77f175b99e",
    "DODO": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "PickleFi": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "Nomad": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "PolyNetwork": "ether",
    "Punk_1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "Punk_2": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "Punk_3": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "SaddleFi": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "Eminence": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "Harvest1_fUSDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "Harvest2_fUSDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "bZx2": "ether",
    "Warp": "0x6b175474e89094c44da98b954eedeac495271d0f", 
    "Warp_interface": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "CheeseBank_1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "CheeseBank_2": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "CheeseBank_3": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "ValueDeFi": "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490",
    "InverseFi": "0x865377367054516e17014ccded1e7d814edc9ce4",
    "Yearn1":  "0x6b175474e89094c44da98b954eedeac495271d0f",
    "Yearn1_interface":  "0x6b175474e89094c44da98b954eedeac495271d0f",
    "Opyn": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "CreamFi1_1": "0xff20817765cb7f73d4bde2e66e067e58d11095c2",
    "CreamFi1_2": "ether",
    "IndexFi": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "CreamFi2_1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "CreamFi2_2": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "CreamFi2_3": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "CreamFi2_4": "0x956f47f50a910163d8bf957cf5846d573e7f87ca",
    "RariCapital1": "ether", 
    "VisorFi": "0xf938424f7210f31df2aee3011291b658f872e91e",
    "UmbrellaNetwork": "0xb1bbeea2da2905e6b0a30203aef55c399c53d042",
    "RevestFi": "0x56de8bc61346321d4f2211e3ac3c0a7f00db9b76",
    "RevestFi_interface": None,
    "RoninNetwork": "ether"

}


benchmark2vault = {
    "BeanstalkFarms": "0x3a70dfa7d2262988064a2d051dd47521e43c9bdd", 
    "BeanstalkFarms_interface": "0xc1e088fc1323b20bcbee9bd1b9fc9546db5624c5",
    "HarmonyBridge": "0xf9fb1c508ff49f78b60d3a96dea99fa5d7f3a8a6",
    "HarmonyBridge_interface": "0x715cdda5e9ad30a0ced14940f9997ee611496de6",
    "XCarnival": "0xb38707e31c813f832ef71c70731ed80b45b85b2d", # 0x5417da20ac8157dd5c07230cfc2b226fdcfc5663",
    "RariCapital2_1": "0x26267e41ceca7c8e0f143554af707336f27fa051",
    "RariCapital2_2": "0xebe0d1cb6a0b8569929e062d67bfbc07608f0a47",
    "RariCapital2_3": "0xe097783483d1b7527152ef8b150b99b9b2700c8d",
    "RariCapital2_4": "0x8922c1147e141c055fddfc0ed5a119f3378c8ef8",
    "DODO": "0x051ebd717311350f1684f89335bed4abd083a2b6", # "0x509ef8c68e7d246aab686b6d9929998282a941fb", # "0x2bbd66fc4898242bdbd2583bbe1d76e8b8f71445",
    # "PickleFi": "0x6949bb624e8e8a90f87cd2058139fcd77d2f3f87", # "0x6847259b2B3A4c17e7c43C54409810aF48bA5210",
    "PickleFi": "0x6949bb624e8e8a90f87cd2058139fcd77d2f3f87", # "0x6847259b2B3A4c17e7c43C54409810aF48bA5210",

    "Nomad": "0x88a69b4e698a4b090df6cf5bd7b2d47325ad30a3",
    "PolyNetwork": "0x250e76987d838a75310c34bf422ea9f1ac4cc906",
    # "Punk_1": "0x3BC6aA2D25313ad794b2D67f83f21D341cc3f5fb",
    # "Punk_2": "0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D",
    # "Punk_3": "0x929cb86046E421abF7e1e02dE7836742654D49d6",
    "SaddleFi": "0x2069043d7556b1207a505eb459d18d908df29b55",

    "Eminence": "0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8",
    "Harvest1_fUSDT": "0x053c80ea73dc6941f518a68e2fc52ac45bde7c9c",
    "Harvest2_fUSDC": "0xf0358e8c3cd5fa238a29301d0bea3d63a17bedbe",
    # "bZx2": "0x77f973fcaf871459aa58cd81881ce453759281bc",
    "Warp": "0x6046c3Ab74e6cE761d218B9117d5c63200f4b406", 
    "Warp_interface": "0xba539b9a5c2d412cb10e5770435f362094f9541c",
    "CheeseBank_1": "0x5E181bDde2fA8af7265CB3124735E9a13779c021",
    "CheeseBank_2": "0x4c2a8A820940003cfE4a16294B239C8C55F29695",
    "CheeseBank_3": "0xA80e737Ded94E8D2483ec8d2E52892D9Eb94cF1f",
    # "ValueDeFi": "0x55bf8304c78ba6fe47fd251f37d7beb485f86d26",  # "0xddd7df28b1fb668b77860b473af819b03db61101"
    "ValueDeFi": "0x55bf8304c78ba6fe47fd251f37d7beb485f86d26",  # "0xddd7df28b1fb668b77860b473af819b03db61101"

    "InverseFi": "0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670",
    # "Yearn1":  "0x9c211bfa6dc329c5e757a223fb72f5481d676dc1", will not be used
    # "Yearn1":  "0x9c211bfa6dc329c5e757a223fb72f5481d676dc1", will not be used

    "Yearn1_interface": "0xacd43e627e64355f1861cec6d3a6688b31a6f952",
    "Opyn": "0x951d51baefb72319d9fbe941e1615938d89abfe2",
    "CreamFi1_1": "0x2db6c82ce72c8d7d770ba1b5f5ed0b6e075066d6",  # 0x3c710b981f5ef28da1807ce7ed3f2a28580e0754
    "CreamFi1_2": "0xd06527d5e56a3495252a528c4987003b712860ee",
    "IndexFi": "0xfa6de2697d59e88ed7fc4dfe5a33dac43565ea41", # "0x5bd628141c62a901e0a83e630ce5fafa95bbdee4",
    "CreamFi2_1": "0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322",
    "CreamFi2_2": "0x797aab1ce7c01eb727ab980762ba88e7133d2157",
    "CreamFi2_3": "0xe89a6d0509faf730bd707bf868d9a2a744a363c7",
    "CreamFi2_4": "0x8c3b7a4320ba70f8239f83770c4015b5bc4e6f91",
    # "RariCapital1": "0xa422890cbbe5eaa8f1c88590fbab7f319d7e24b6", # 0xd6e194af3d9674b62d1b30ec676030c23961275e", # "0xec260f5a7a729bb3d0c42d292de159b4cb1844a3", 
    "VisorFi": "0xc9f27a50f82571c1c8423a42970613b8dbda14ef",
    "UmbrellaNetwork": "0xb3fb1d01b07a706736ca175f827e4f56021b85de",
    "RevestFi": "0xa81bd16aa6f6b25e66965a2f842e9c806c0aa11f",
    "RevestFi_interface": "0x2320a28f52334d62622cc2eafa15de55f9987ed9",
    "RoninNetwork": "0x1a2a1c938ce3ec39b6d47113c7955baa9dd454f2",  # 0x8407dc57739bcda7aa53ca6f12f82f9d51c2f21e

}

# the benchmark contracts that does not support money flow ratio analysis
vaultContractBenchmarks = ["Punk_1", "Punk_2", "Punk_3", \
                           "ValueDeFi", "Yearn1", "RariCapital1", \
                            "bZx2", "PickleFi"]

vaultContractBenchmarks = ["bZx2", "RariCapital1"]


etherBenchmarks = [
    "bZx2", "RoninNetwork", "HarmonyBridge", "XCarnival", \
    'RariCapital2_1', "RariCapital1", "PolyNetwork", \
    "IndexFi"  # UNI, its transfer and transferFrom haev multiple sstores
]


# check X invariants
# 1. upper bounds for data flow
# 2. ranges for data flow

def inferMoneyFlows(executionTable):
    crawlQuickNode = CrawlQuickNode()
    crawlEtherscan = CrawlEtherscan()

    isStart = False
    
    for category, benchmarkName, contract, executionList, exploitTx, l1, l2, l3 in executionTable:

        if benchmarkName == "Warp_interface2":
            # this benchmark is originally collected but later removed because it is not a victim contract 
            continue
        

        print("====== benchmark {}: ".format(benchmarkName))

        path = SCRIPT_DIR + "/cache/trainingSet/{}.pickle".format(benchmarkName)
        trainTxList = readDataSource(path)[0]

        path = SCRIPT_DIR + "/cache/testingSet/{}.pickle".format(benchmarkName)
        # testingTxList = readDataSource(path)[0]

        if benchmark2token[benchmarkName] == None:
            print("benchmark {} does not support money flow analysis".format(benchmarkName))
            continue
        
        # if benchmarkName != "CreamFi1_2":
        #     continue

        # if benchmarkName == "RariCapital2_2" or benchmarkName == "RariCapital2_3" or \
        #     benchmarkName == "RariCapital2_4":
        #     continue

        # if benchmarkName == "RevestFi" or benchmarkName == "Eminence":
        #     continue



        originalContract = benchmark2vault[benchmarkName] if benchmarkName in benchmark2vault else None
        if contract in proxyMap:
            contract = proxyMap[contract]

        # build read-only functions
        ABI = crawlEtherscan.Contract2ABI(contract)
        readOnlyFunctions = ["fallback"]
        nonReadOnlyFunctions = []
        for function in ABI:
            if function["type"] == "function" and (function["stateMutability"] == "view" or function["stateMutability"] == "pure"):
                readOnlyFunctions.append(function["name"])
            if function["type"] == "function" and (function["stateMutability"] != "view" and function["stateMutability"] != "pure"):
                nonReadOnlyFunctions.append(function["name"])

        # stage 1: training
        moneyFlowMap = {
        # { "func+type": 
        #          { 
        #             "transferAmount": []
        #             "transferPC": []
        #             "transferTokenBalance": []
        #          }
        # }
        }

        lastBlockBalance = [0, 0]

        counter = -1

        blocks = []

        transferToken = benchmark2token[benchmarkName]


        # executionList = executionList[:200]


# dataFlowInfer: error: temp=302562360222770519155260 != lastBlockBalance[1]=302565360222770519155260
# tx = 0x9572b2330c6e54138223ba0876d01bfacd1bc441261a68c63dc3f1b1822881ec
        for tx, dataS in executionList:
            counter += 1
            # print("counter = {} / {}".format(counter, len(executionList)))

            # if tx == "0x9572b2330c6e54138223ba0876d01bfacd1bc441261a68c63dc3f1b1822881ec":
            #     print("now is the time")
            
            if tx not in trainTxList:
                break
            
            if tx == "0x30fd944ddd5a68a9ab05048a243b852daf5f707e0448696b172cea89e757f4e5" or \
                tx == "0x7ae864faf81979eba3bffa7a2a72f4ded858694ced79c63d613020d064bc06f4":
                # buggy tx
                continue


            sources = dataS["sources"]
            children = dataS["children"]
            metaData = dataS["metaData"]

            targetFunc = metaData["targetFunc"]
            targetFuncType = metaData["targetFuncType"]
            name = targetFunc + "+" + targetFuncType 

            if name not in moneyFlowMap:
                if benchmarkName not in vaultContractBenchmarks:
                    moneyFlowMap[ name ] = {
                        "transferAmount": [], 
                        "transferPC": [],
                        "transferTokenBalance": []    
                    }
                else:
                    moneyFlowMap[ name ] = {
                        "transferAmount": [], 
                        "transferPC": [],
                    }

            pc = None
            if "pc" in metaData:
                pc = metaData["pc"]
            elif len(sources) == 1 and isinstance(sources[0], str) and sources[0] ==  "msg.value":
                pc = -1
            else:
                sys.exit("dataFlowInfer: pc is not in metaData")
            if pc == None:
                sys.exit("dataFlowInfer: pc is None")
            # gas = metaData["gas"]
            # type = metaData["type"]
            # if type != "uint256":
            #     print(type)

            transferAmount = None
            if "value" in metaData:
                transferAmount = metaData["value"]
            elif len(sources) == 1 and isinstance(sources[0], str) and sources[0] ==  "msg.value":
                # if "msg.value" not in metaData:
                #     print(tx)
                #     continue
                transferAmount = metaData["msg.value"] 
                if isinstance(transferAmount, str):
                    transferAmount = int(transferAmount, 16)
            else:
                print(sources)
                sys.exit("dataFlowInfer: transferAmount is not in metaData")
            
            if isinstance(transferAmount, str):
                transferAmount = int(transferAmount, 16)
            
            if transferAmount == None:
                print(sources)
                sys.exit("dataFlowInfer: transferAmount is None")

            # if transferAmount > 2857486346845890372134:
            #     print("transferAmount = {}".format(transferAmount))
            #     print(tx)


            moneyFlowMap[name]["transferAmount"].append(transferAmount)
            moneyFlowMap[name]["transferPC"].append(pc)

            # if benchmarkName == "RoninNetwork":
            #     sys.exit("dataFlowInfer: transferToken is None")

            if benchmarkName not in vaultContractBenchmarks: # and transferToken == benchmark2token[benchmarkName]:                    
                
                transferTokenBalance = None
                block = crawlQuickNode.Tx2Block(tx)
                if benchmarkName != "IndexFi" and "sstore" in metaData and len(metaData["sstore"]) == 3 and isinstance(metaData["sstore"][0], str) and \
                    (metaData["sstore"][0] == "transferFrom" or metaData["sstore"][0] == "transfer"):
                    if metaData["sstore"][0] == "transferFrom":
                        postBalance = int(metaData["sstore"][2][1], 16)
                        transferTokenBalance = postBalance - transferAmount
                        lastBlockBalance = [block, transferTokenBalance]
                    elif metaData["sstore"][0] == "transfer":
                        postBalance = int(metaData["sstore"][1][1], 16)
                        transferTokenBalance = postBalance + transferAmount
                        lastBlockBalance = [block, transferTokenBalance]
                else:
                    # print("sstore not in metaData")
                    if block not in blocks:
                        blocks.append(block)
                        blocks.append(block - 1)

                    transferTokenBalance = None
                    if lastBlockBalance[0] == block - 1:
                        transferTokenBalance = lastBlockBalance[1]
                    else:
                        if lastBlockBalance[0] != 0:
                            # we are about to replace lastBlockBalance
                            # print("tx: ", counter, tx)
                            temp = crawlQuickNode.TokenBalanceOf(transferToken, originalContract, lastBlockBalance[0] + 1)
                            if temp != lastBlockBalance[1] and benchmarkName not in etherBenchmarks:
                                print("dataFlowInfer: error: temp={} != lastBlockBalance[1]={}".format(temp, lastBlockBalance[1]))
                                for jj in range(counter, counter-20 ,-1):
                                    if jj == 0:
                                        break
                                    tempBlock = crawlQuickNode.Tx2Block(executionList[jj][0])
                                    if tempBlock == lastBlockBalance[0] + 1:
                                        print("tx = {}".format(executionList[jj][0]))


                        transferTokenBalance = crawlQuickNode.TokenBalanceOf(transferToken, originalContract, block - 1)
                        lastBlockBalance = [block - 1, transferTokenBalance]
                        # print("lastBlockBalance = {}".format(lastBlockBalance))
                
                if targetFuncType == "withdraw" or targetFuncType == "invest":
                    lastBlockBalance[1] -= transferAmount
                    if lastBlockBalance[1] < 0:
                        sys.exit("dataFlowInfer: lastBlockBalance[1] < 0")
                elif targetFuncType == "deposit":
                    lastBlockBalance[1] += transferAmount
                else:
                    sys.exit("dataFlowInfer: targetFuncType is not withdraw or invest or deposit")
                # print("transferTokenBalance = {} for contract {} at block {} at transaction {}".format(transferTokenBalance, originalContract, block - 1, tx))
                # print("transferAmount = {} for {}".format(transferAmount, name))

                moneyFlowMap[name]["transferTokenBalance"].append(transferTokenBalance)



        
        print("moneyFlowMap")
        for func in moneyFlowMap:
            print("{}: {}".format(func, moneyFlowMap[func]))


        for name in moneyFlowMap:
            if "transferPC" in moneyFlowMap[name] and len(moneyFlowMap[name]["transferPC"]) >= 2:
                maxPC = max(moneyFlowMap[name]["transferPC"])
                minPC = min(moneyFlowMap[name]["transferPC"])
                if maxPC != minPC and name != "unlock+withdraw" and name != "borrowTokenFromDeposit+deposit" and \
                    name != "deposit+deposit" and name != "redeemUnderlying+withdraw":
                    print("name = {}, maxPC = {}, minPC = {}".format(name, maxPC, minPC))
                    # sys.exit("dataFlowInfer: error: maxPC != minPC")

                
        invariantMap = {
        # { "func": 
        #          { 
        #             "transferAmount": (smallest value, largest value)
        #             "transferRatio": (smallest value, largest value)
        #          }
        # }
        }



        # stage 2: infer
        # print(moneyFlowMap)
        for func in moneyFlowMap:
            maxValue = max(moneyFlowMap[func]["transferAmount"])
            minValue = min(moneyFlowMap[func]["transferAmount"])
            if len(moneyFlowMap[func]["transferAmount"]) >= 2 and maxValue != minValue:
                invariantMap[func] = {"transferAmount": (minValue, maxValue)}

        for func in moneyFlowMap:
            # transferRatio = transferAmount / transferTokenBalance
            if "transferAmount" in moneyFlowMap[func] and "transferTokenBalance" in moneyFlowMap[func]:
                transferRatioList = []
                for x, y in zip(moneyFlowMap[func]["transferAmount"], moneyFlowMap[func]["transferTokenBalance"]):
                    if y == 0 or x == 0:
                        continue
                    transferRatioList.append(x / y)
                # apply z-score method to filter outliers
                data = np.array(transferRatioList)
                data_mean = np.mean(data)
                data_std = np.std(data)
                transferRatioList = [x for x in transferRatioList if abs(x - data_mean) <= 3 * data_std]
                maxValue = max(transferRatioList)
                minValue = min(transferRatioList)
                if len(transferRatioList) >= 2 and maxValue != minValue:
                    invariantMap[func]["transferRatio"] = (minValue, maxValue)
                    isHaveRatio = True

        print("==invariant map: ")
        print(invariantMap)

        isHaveToken = False
        isHaveRatio = False
        for func in invariantMap:
            if "transferAmount" in invariantMap[func] and len(invariantMap[func]["transferAmount"]) > 0:
                isHaveToken = True
            if "transferRatio" in invariantMap[func] and len(invariantMap[func]["transferRatio"]) > 0:
                isHaveRatio = True



        positivePath = SCRIPT_DIR + "/cache/positives/tokenOutCap/{}.txt".format(benchmarkName)
        # positivePathRatio = SCRIPT_DIR + "/cache/positives/tokenOutRatioCap/{}.txt".format(benchmarkName)


        # stage 3: validation
        FPMap = {}
        if isHaveToken:
            FPMap["tokenInUpperBound"] = []
            FPMap["tokenOutUpperBound"] = []
        if isHaveRatio:
            FPMap["tokenInRatioUpperBound"] = []
            FPMap["tokenOutRatioUpperBound"] = []


        

        txList2 = []

        isFiltered = False
        isFilteredByTokenOutCap = False
        isFilteredByTokenOutCapRatio = False
        
        for ii, (tx, dataS) in enumerate(executionList[counter:]):
            currentIndex = ii + counter
            if tx not in txList2:
                txList2.append(tx)

            sources = dataS["sources"]
            children = dataS["children"]
            metaData = dataS["metaData"]

            targetFunc = metaData["targetFunc"]
            targetFuncType = metaData["targetFuncType"]
            name = targetFunc + "+" + targetFuncType 

            transferAmount = None
            if "value" in metaData:
                transferAmount = metaData["value"]
            elif len(sources) == 1 and isinstance(sources[0], str) and sources[0] ==  "msg.value":
                # if "msg.value" not in metaData:
                #     print(tx)
                #     continue
                transferAmount = metaData["msg.value"] 
            else:
                print(sources)
                sys.exit("dataFlowInfer: transferAmount is not in metaData")

            if isinstance(transferAmount, str):
                transferAmount = int(transferAmount, 16)

            # print("transferAmount = {} for {}".format(transferAmount, name))

            ratio = None

            if benchmarkName not in vaultContractBenchmarks:
                block = crawlQuickNode.Tx2Block(tx)
                transferTokenBalance = None
                if benchmarkName != "IndexFi" and "sstore" in metaData and len(metaData["sstore"]) == 3 and isinstance(metaData["sstore"][0], str) and \
                    (metaData["sstore"][0] == "transferFrom" or metaData["sstore"][0] == "transfer"):
                    if metaData["sstore"][0] == "transferFrom":
                        postBalance = int(metaData["sstore"][2][1], 16)
                        transferTokenBalance = postBalance - transferAmount
                        lastBlockBalance = [block, transferTokenBalance]
                    elif metaData["sstore"][0] == "transfer":
                        postBalance = int(metaData["sstore"][1][1], 16)
                        transferTokenBalance = postBalance + transferAmount
                        lastBlockBalance = [block, transferTokenBalance]
                else:
                    # print("sstore not in metaData")
                    block = crawlQuickNode.Tx2Block(tx)
                    if block not in blocks:
                        blocks.append(block)
                        blocks.append(block - 1)

                    transferTokenBalance = None
                    if lastBlockBalance[0] == block - 1:
                        transferTokenBalance = lastBlockBalance[1]
                    else:
                        if lastBlockBalance[0] != 0:
                            # we are about to replace lastBlockBalance
                            temp = crawlQuickNode.TokenBalanceOf(transferToken, originalContract, lastBlockBalance[0] + 1)
                            if temp != lastBlockBalance[1] and benchmarkName not in etherBenchmarks:
                                print("dataFlowInfer: error: temp={} != lastBlockBalance[1]={}".format(temp, lastBlockBalance[1]))
                                for jj in range(currentIndex, currentIndex-20 ,-1):
                                    if jj == 0:
                                        break
                                    tempBlock = crawlQuickNode.Tx2Block(executionList[jj][0])
                                    if tempBlock == lastBlockBalance[0] + 1:
                                        print("tx = {}".format(executionList[jj][0]))

                        transferTokenBalance = crawlQuickNode.TokenBalanceOf(transferToken, originalContract, block - 1)
                        lastBlockBalance = [block - 1, transferTokenBalance]
                    
            
                if targetFuncType == "withdraw" or targetFuncType == "invest":
                    lastBlockBalance[1] -= transferAmount

                    if lastBlockBalance[1] < 0:
                        sys.exit("dataFlowInfer: lastBlockBalance[1] < 0")

                elif targetFuncType == "deposit":
                    lastBlockBalance[1] += transferAmount
                else:
                    sys.exit("dataFlowInfer: targetFuncType is not withdraw or invest or deposit")

                # print("transferTokenBalance = {} for contract {} at block {} at transaction {}".format(transferTokenBalance, originalContract, block - 1, tx))
                
                ratio = None
                if transferAmount != 0 and transferTokenBalance != 0:
                    ratio = transferAmount / transferTokenBalance
                    


            if tx == exploitTx:
                
                print("name {}, transferAmount = {}, transferPrebalance = {}, ratio = {}".format(name, transferAmount, transferTokenBalance, ratio))
                if name in invariantMap:
                    if "transferAmount" in invariantMap[name]:
                        print("func {} transfers {} tokens".format(name, transferAmount))
                        minValue, maxValue = invariantMap[name]["transferAmount"]
                        print("maxValue = {}, minValue = {}".format(maxValue, minValue))

                        if transferAmount > maxValue:
                            isFiltered = True
                            if "+deposit" in name:
                                print("Successfully stops the exploit using tokenInUpperBound")
                            
                            if "+invest" in name or "+withdraw" in name:
                                print("Successfully stops the exploit using tokenOutUpperBound")
                                isFilteredByTokenOutCap = True
                    
                    if "transferRatio" in invariantMap[name]:
                        print("func {} transfers {} ratio".format(name, ratio))
                        minValue, maxValue = invariantMap[name]["transferRatio"]
                        print("maxValue = {}, minValue = {}".format(maxValue, minValue))

                        if ratio != None and ratio > maxValue:
                            isFiltered = True
                            if "+deposit" in name:
                                print("Successfully stops the exploit using tokenInRatioUpperBound")

                            if ("+invest" in name or "+withdraw" in name) and tx not in FPMap["tokenOutRatioUpperBound"]:
                                print("Successfully stops the exploit using tokenOutRatioUpperBound")
                                isFilteredByTokenOutCapRatio = True

                            if tx in FPMap["tokenOutRatioUpperBound"]:
                                sys.exit("dataFlowInfer: error: tx in FPMap[tokenOutRatioUpperBound]")

                if len(executionList) == currentIndex + 1 or executionList[currentIndex + 1][0] != exploitTx:
                    print("exploitTx: ", exploitTx)
                    print("FPMap: ", end="")
                    printFPMap(invariantMap, FPMap, benchmarkName)

                    newList = copy.deepcopy(FPMap["tokenOutUpperBound"] if "tokenOutUpperBound" in FPMap else [])
                    newList.insert(0, 'exploitTx: {}'.format(exploitTx))
                    

                    if isFilteredByTokenOutCap:
                        newList.append(exploitTx)
                    if isHaveToken:
                        writeListTxt(positivePath, newList)


                    # newList2 = copy.deepcopy(FPMap["tokenOutRatioUpperBound"] if "tokenOutRatioUpperBound" in FPMap else [])
                    # newList2.insert(0, 'exploitTx: {}'.format(exploitTx))
                    # if isFilteredByTokenOutCapRatio:
                    #     newList2.append(exploitTx)
                    # if isHaveToken:
                    #     writeListTxt(positivePath, newList2)
                    break
            
            elif len(executionList) == currentIndex + 1:
                print("does not meet the exploit tx")
                print("FPMap: ", end="")
                printFPMap(invariantMap, FPMap, benchmarkName)


                newList = copy.deepcopy(FPMap["tokenOutUpperBound"] if "tokenOutUpperBound" in FPMap else [])
                newList.insert(0, 'exploitTx: {}'.format(exploitTx))
                
                if isHaveToken:
                    writeListTxt(positivePath, newList)
          

            else: 
                if name in invariantMap:
                    if "transferAmount" in invariantMap[name]:
                        minValue, maxValue = invariantMap[name]["transferAmount"]
                        if transferAmount > maxValue:
                            if "+deposit" in name and tx not in FPMap["tokenInUpperBound"]:
                                FPMap["tokenInUpperBound"].append(tx)
                            if ("+invest" in name or "+withdraw" in name) and tx not in FPMap["tokenOutUpperBound"]:
                                FPMap["tokenOutUpperBound"].append(tx)

                    if "transferRatio" in invariantMap[name]:
                        minValue, maxValue = invariantMap[name]["transferRatio"]
                        if ratio != None and ratio > maxValue:
                            if "+deposit" in name and tx not in FPMap["tokenInRatioUpperBound"]:
                                FPMap["tokenInRatioUpperBound"].append(tx)
                            if ("+invest" in name or "+withdraw" in name) and tx not in FPMap["tokenOutRatioUpperBound"]:
                                FPMap["tokenOutRatioUpperBound"].append(tx)




        # crawlQuickNode.BatchTokenBalanceOfHelper(transferToken, originalContract, blocks)

        # # time.sleep(1)


