import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Benchmarks_Traces.listBenchmark import *
from Benchmarks_Traces.filterTx import *
from Benchmarks_Traces.detectTrace import *
from parserPackage.locator import *
from parserPackage.parser import *
from parserPackage.parserRunnerUtils import *
from constraintPackage.accessControlInfer import *
from constraintPackage.txCounterHelper import *
from constraintPackage.timeLockInfer import *
from constraintPackage.dataFlowInfer import *
from constraintPackage.oracleControl import *
from constraintPackage.moneyFlowInfer import *
from constraintPackage.specialStorage import *
from constraintPackage.gasControlInfer import *
from constraintPackage.reentrancyInfer import *

import pickle
import gc

def writeDataSource(contract, tx, dataSourceMapList):
    path = SCRIPT_DIR + "/../cache/" + contract + "/{}.pickle".format(tx)
    # print("write", path)
    # print(dataSourceMapList)
    with open(path, 'wb') as f:
        pickle.dump(dataSourceMapList, f)

def readDataSource(contract, tx):
    path = SCRIPT_DIR + "/../cache/" + contract + "/{}.pickle".format(tx)
    objects = []
    # check if file exists
    if not os.path.exists(path):
        return objects
    with (open(path, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects


def writeAccessList(contract, tx, accessList):
    path = SCRIPT_DIR + "/../cache/" + contract + "_Access/{}.pickle".format(tx)
    # print("write", path)
    # print(dataSourceMapList)
    with open(path, 'wb') as f:
        pickle.dump(accessList, f)

def readAccessList(contract, tx):
    path = SCRIPT_DIR + "/../cache/" + contract + "_Access/{}.pickle".format(tx)
    objects = []
    # check if file exists
    if not os.path.exists(path):
        return objects
    with (open(path, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects


def writeSplitedTraceTree(contract, tx, splitedTraceTree):
    path = SCRIPT_DIR + "/../cache/" + contract + "_SplitedTraceTree/{}.pickle".format(tx)
    # print("write", path)
    # print(dataSourceMapList)
    with open(path, 'wb') as f:
        pickle.dump(splitedTraceTree, f)

def readSplitedTraceTree(contract, tx):
    path = SCRIPT_DIR + "/../cache/" + contract + "_SplitedTraceTree/{}.pickle".format(tx)
    objects = []
    # check if file exists
    if not os.path.exists(path):
        return objects
    with (open(path, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects




# depositLocator
# investLocator
# withdrawLocator

def analyzeOneTxHelper(category, contract, tx, path, depositLocator, investLocator, withdrawLocator):
    dataSourceMapList = None
    try:
        dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contract, tx, path, depositLocator, investLocator, withdrawLocator)
        printdataSourceMapList(dataSourceMapList)

        writeDataSource(contract, tx, dataSourceMapList)
        writeAccessList(contract, tx, accessList)
        writeSplitedTraceTree(contract, tx, splitedTraceTree)
        kk = readSplitedTraceTree(contract, tx)
        # if kk != [[]]:
        #     print("kk: {}".format(kk))
        return
    except Exception as e:
        print(e)
        # fe = fetcher()
        # fe.storeTrace(category = category, contract = contract, Tx = tx, FullTrace = False)
        # time.sleep(10)

    try:
        dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contract, tx, path, depositLocator, investLocator, withdrawLocator)
        printdataSourceMapList(dataSourceMapList)
        
        writeDataSource(contract, tx, dataSourceMapList)
        writeAccessList(contract, tx, accessList)
        writeSplitedTraceTree(contract, tx, splitedTraceTree)
        return
    except Exception as e:
        print(e, file=sys.stderr)
        print("Some error happened when analyzing tx: {} path: {}".format(tx, path), file=sys.stderr)
        sys.exit("Some error happened when analyzing tx: {} path: {}".format(tx, path))

    
    # if len(dataSourceMapList) > 0:
        # print("================== dataSourceMapList ==================")
        # print("tx: {}".format(tx))

        # for item in dataSourceMapList:
        #     print(item)
        # print("========================= end =========================")


reCollect = False
def analyzeAllTx(category, contract, depositLocators, investLocators, withdrawLocators):
    # if directory does not exist, create it
    if not os.path.exists(SCRIPT_DIR + "/../cache/" + contract):
        os.makedirs(SCRIPT_DIR + "/../cache/" + contract)

    if not os.path.exists(SCRIPT_DIR + "/../cache/" + contract + "_Access"):
        os.makedirs(SCRIPT_DIR + "/../cache/" + contract + "_Access")

    if not os.path.exists(SCRIPT_DIR + "/../cache/" + contract + "_SplitedTraceTree"):
        os.makedirs(SCRIPT_DIR + "/../cache/" + contract + "_SplitedTraceTree")

    startTime = time.time()
    # listTxDetails(contract, category)
    txList, pathList = categoryContract2Paths(category, contract)


    NumOfProcesses = 4
    processes = []
    processStats = []
    for _ in range(NumOfProcesses):
        processStats.append(0)
    ProcessesRunning = 0
    l1 = depositLocators
    l2 = investLocators
    l3 = withdrawLocators


    # # print index of tx
    # index = txList.index("0x0016745693d68d734faa408b94cdf2d6c95f511b50f47b03909dc599c1dd9ff6")
    # print("index: {}".format(index))
    

    # ignore the create transaction
    for ii in range(0, len(txList)):

        tx = txList[ii]
        path = pathList[ii]

        # if tx != "0x20507b57f480e4140548ff0039928dd903e6e9043d2a59f6859e79b0771e5f1b":
        #     continue
        
        if tx == "0x52a0541deff2373e1098881998b60af4175d75c410d67c86fcee850b23e61fc2" \
            or tx == "0xca13006944e6eba2ccee0b2d96a131204491641014622ef2a3df3db3e6939062" \
            or tx == "0x12cd6005c1b58c0f9148d20762e9f2f707bcb8e421b99c6bfc1acd6e61d6194a" \
            or tx == "0xed7efd5bf771ae1e115fb59b9f080c2f66d74bf3c9234a89acb0e91e48181aec" \
            or tx == "0x4d9fa1d76e0d0b16a864072f9ef21eead69b7334d96c970ca2e25a50324c3719" \
            or tx == "0xafc546d25451f63f18956374b9c4015bea6e8e6bc2820591416d620ca6c8b510" \
            or tx == "0xc84663786789f846ea8887b3b3782e87618813eee75c9359ef2ec413df7001dc":
            # this tx trace is too big
            continue

        if tx == "0x9704d47c0b93310fd916f49a915a03de7ba3d53388bdd290bbc40211ccfccfa0" or \
            tx == "0x7298417f8680cb4c76903fa18c6150a8d46238e4c0fce0fb9c48b51c2962b84f":
            # this tx is mint CHI tokens
            continue

        if tx == "0x5db5d214fb307c214183e69fc342ebfd66951818410b08ab50ef2b5c8da78c49":
            # it's depoly tx of yDAI of Yearn_interface
            continue

        picklePath = SCRIPT_DIR + "/../cache/" + contract + "/{}.pickle".format(tx)

        print(picklePath)

        # if not reCollect:
        if os.path.exists(picklePath):
            print("data source exists {}/{} tx: {}  path: {}".format(ii+1,  len(txList), tx, path))
            continue

        if ProcessesRunning < NumOfProcesses:
            p = multiprocessing.Process(target=analyzeOneTxHelper, args=(category, contract, tx, path, l1, l2, l3 ))
            p.start()
            processes.append(p)
            processStats[ProcessesRunning] = [tx, ii, time.time()]
            ProcessesRunning += 1
            if ProcessesRunning == NumOfProcesses:
                print("From now on, all processes are running")
        else:
            # spinning wait
            ifbreak = False
            while True:
                for jj in range(NumOfProcesses):
                    if not processes[jj].is_alive():
                        processes[jj].join()
                        # print("Process {} finished for {}(progress: {}/{}), takes time {} s".format(jj, processStats[jj][0], processStats[jj][1], len(txList), time.time() - processStats[jj][2]))
                        # checkFileSize(logPath)
                        p = multiprocessing.Process(target=analyzeOneTxHelper, args=(category, contract, tx, path, l1, l2, l3 ))
                        p.start()
                        processes[jj] = p
                        processStats[jj] = [tx, ii, time.time()]
                        ifbreak = True
                        break
                if ifbreak:
                    break
                # sleep 100 ms
                # time.sleep(1)

        print("now analyze {}/{} tx: {}  path: {}".format(ii+1,  len(txList), tx, path))

    endTime = time.time()
    print("time: {}".format(endTime - startTime))
    if endTime - startTime > 15:
        time.sleep(50)
    executionListList = []
    # now read all execution List
    for ii in range(0, len(txList)):
        tx = txList[ii]
        executionList = readDataSource(contract, tx)
        if len(executionList) > 0 and len(executionList[0]) > 0 :
            for execution in executionList[0]:
                executionListList.append( (tx, execution) )

    # now read all access List
    accessListList = []
    for ii in range(0, len(txList)):
        tx = txList[ii]
        accessList = readAccessList(contract, tx)
        if len(accessList) > 0:
            accessListList.append( (tx, accessList) )
            


    # time.sleep(20)
    return executionListList, accessListList



# token: DAI
def mainEminence():
    category = "FlashSyn"
    contract = "0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8" # 
    # deposit locator
    l1 = [
            locator("buy", FUNCTION, name="transferFrom", position=2)
        ]
    # invest locator
    l2 = []  
    # Withdraw locator
    l3 = [
            locator("sell", FUNCTION, name="transfer", position=1)
        ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: USDT
def mainHarvest1_fUSDT():
    category = "FlashSyn"
    contract = "0x053c80ea73dc6941f518a68e2fc52ac45bde7c9c"     # 
    changeLoggingUpperBound(6)
    # deposit locator
    l1 = [
            locator("deposit", FUNCTION, name="transferFrom", position=2),
            locator("depositFor", FUNCTION, name="transferFrom", position=2)
    ]
    # invest locator
    l2 = [
        locator("doHardWork", FUNCTION, name="transfer", position=1),
        locator("rebalance", FUNCTION, name="transfer", position=1)
    ]
    # Withdraw locator
    l3 = [ locator("withdraw", FUNCTION, name="transfer", position=1) ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: USDC
def mainHarvest2_fUSDC():
    category = "FlashSyn"
    contract = "0xf0358e8c3cd5fa238a29301d0bea3d63a17bedbe"     # 
    changeLoggingUpperBound(6)
    # deposit locator
    l1 = [
        locator("deposit", FUNCTION, name="transferFrom", position=2),
        locator("depositFor", FUNCTION, name="transferFrom", position=2)
    ]
    # invest locator
    l2 = [
        locator("doHardWork", FUNCTION, name="transfer", position=1),
        locator("rebalance", FUNCTION, name="transfer", position=1)
    ]
    # Withdraw locator
    l3 = [ locator("withdraw", FUNCTION, name="transfer", position=1) ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



# token: ETH
def mainbZx2(): 
    category = "FlashSyn"
    contract = "0x85ca13d8496b2d22d6518faeb524911e096dd7e0"     # bZx2 asset: WETH
    changeLoggingUpperBound(16)
    l1 = [
        locator("borrowTokenFromDeposit", FUNCTION, fromAddr= "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",\
                name="transferFrom", position=2),
    ]
    l2 = []  
    l3 = [
        locator("burn", FUNCTION, fromAddr= "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", \
                name="transfer", position=1),
        locator("burnToEther", FUNCTION, name="claimEther", position=1),
        locator("borrowTokenFromDeposit", FUNCTION, name="claimEther", position=1),
        locator("marginTradeFromDeposit", FUNCTION, name="claimEther", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: DAI
def mainWarp():
    category = "FlashSyn"
    contract = '0x6046c3Ab74e6cE761d218B9117d5c63200f4b406'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("repayBorrow", FUNCTION, name="transferFrom", position=2),
        locator("_repayLiquidatedLoan", FUNCTION, name="transferFrom", position=2),   # onlyWarpControl
        locator("lendToWarpVault", FUNCTION, name="transferFrom", position=2)
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("_borrow", FUNCTION, name="transfer", position=1),  # onlyWarpControl
        locator("redeem", FUNCTION, name="transfer", position=1)
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: DAI
def mainWarp_interface():
    category = "FlashSyn"
    contract = '0xba539b9a5c2d412cb10e5770435f362094f9541c'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = []
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



# token: DAI
def mainWarp_interface2():
    category = "FlashSyn"
    contract = '0x13db1cb418573f4c3a2ea36486f0e421bc0d2427'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("provideCollateral", FUNCTION, name="transferFrom", position=2),
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawCollateral", FUNCTION, name="transfer", position=1),  
        locator("_liquidateAccount", FUNCTION, name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



# token: USDC
def mainCheeseBank_1():
    category = "FlashSyn"
    contract = '0x5E181bDde2fA8af7265CB3124735E9a13779c021'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("_becomeImplementation", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name = "transferFrom", position=2),
        locator("_setImplementation", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name = "transferFrom", position=2),
        locator("mint", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name = "transferFrom", position=2),
        locator("repayBorrow", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name = "transferFrom", position=2),
        locator("repayBorrowBehalf", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name = "transferFrom", position=2),
        locator("liquidateBorrow", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name = "transferFrom", position=2),
        locator("_addReserves", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name = "transferFrom", position=2),
    ]        
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("redeem", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name="transfer", position=1),
        locator("redeemUnderlying", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                 name="transfer", position=1),
        locator("borrow", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name="transfer", position=1),
        locator("_reduceReserves", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",\
                name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: USDT
def mainCheeseBank_2():
    category = "FlashSyn"
    contract = '0x4c2a8A820940003cfE4a16294B239C8C55F29695'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("_becomeImplementation", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name = "transferFrom", position=2),
        locator("_setImplementation", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name = "transferFrom", position=2),
        locator("mint", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name = "transferFrom", position=2),
        locator("repayBorrow", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name = "transferFrom", position=2),
        locator("repayBorrowBehalf", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name = "transferFrom", position=2),
        locator("liquidateBorrow", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name = "transferFrom", position=2),
        locator("_addReserves", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name = "transferFrom", position=2),
    ]    
    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
        locator("redeem", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name="transfer", position=1),
        locator("redeemUnderlying", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                 name="transfer", position=1),
        locator("borrow", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name="transfer", position=1),
        locator("_reduceReserves", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7",\
                name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: DAI
def mainCheeseBank_3():
    category = "FlashSyn"
    contract = '0xA80e737Ded94E8D2483ec8d2E52892D9Eb94cF1f'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("_becomeImplementation", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name = "transferFrom", position=2),
        locator("_setImplementation", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name = "transferFrom", position=2),
        locator("mint", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name = "transferFrom", position=2),
        locator("repayBorrow", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name = "transferFrom", position=2),
        locator("repayBorrowBehalf", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name = "transferFrom", position=2),
        locator("liquidateBorrow", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name = "transferFrom", position=2),
        locator("_addReserves", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name = "transferFrom", position=2),
    ]    
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("redeem", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name="transfer", position=1),
        locator("redeemUnderlying", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                 name="transfer", position=1),
        locator("borrow", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name="transfer", position=1),
        locator("_reduceReserves", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",\
                name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: DAI
def mainValueDeFi():
    category = "FlashSyn"
    contract = '0xddd7df28b1fb668b77860b473af819b03db61101'
    changeLoggingUpperBound(4)
    l1 = [
        locator("deposit", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transferFrom", position=2),
        locator("depositFor", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transferFrom", position=2),
        locator("depositAllFor", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transferFrom", position=2),
        locator("depositAll", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transferFrom", position=2),     
    ]
    l2 = []
    l3 = [ 
        locator("earn", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("depositFor", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("deposit", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("depositAllFor", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("depositAll", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("convert_nonbased_want", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("earnExtra", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("harvest", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("claimInsurance", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("governanceRecoverUnsupported", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("withdrawFor", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),
        locator("withdraw", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
                name="transfer", position=1),

    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



# Dola, also == a USD
def mainInverseFi():   # encounter mint 
    category = "FlashSyn"
    contract = '0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670'
    changeLoggingUpperBound(6)
    l1 = [
        locator("mint", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transferFrom", position=2),  
        locator("repayBorrow", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transferFrom", position=2),  
        locator("repayBorrowBehalf", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transferFrom", position=2),  
        locator("liquidateBorrow", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transferFrom", position=2),  
        locator("_addReserves", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transferFrom", position=2),  

    ]
    l2 = [
    ]
    l3 = [
        locator("redeem", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transfer", position=1),
        locator("redeemUnderlying", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transfer", position=1),
        locator("borrow", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transfer", position=1),
        locator("_reduceReserves", FUNCTION, funcAddress = "0x865377367054516e17014ccded1e7d814edc9ce4", \
                name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



# token: DAI
def mainYearn1():
    category = "FlashSyn"
    contract = '0x9c211bfa6dc329c5e757a223fb72f5481d676dc1'
    changeLoggingUpperBound(4)
    l1 = []
    l2 = []
    l3 = [
        locator("withdraw", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
        locator("withdrawAll", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
        locator("migrate", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
        locator("forceW", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
        locator("forceD", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),   
        locator("deposit", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),   
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


# token: DAI
def mainYearn1_interface():
    category = "FlashSyn"
    contract = '0xacd43e627e64355f1861cec6d3a6688b31a6f952'
    changeLoggingUpperBound(5)
    l1 = [
        locator("deposit", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transferFrom", position=2),
        locator("depositAll", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transferFrom", position=2),

    ]
    l2 = []
    l3 = [
        locator("earn", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
        locator("harvest", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
        locator("withdraw", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
        locator("withdrawAll", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3




def mainOpyn(): 
    category = "DeFiHackLabs"
    contract = '0x951d51baefb72319d9fbe941e1615938d89abfe2'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("sellOTokens", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2),
        locator("uniswapBuyOToken", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2),
        locator("addERC20Collateral", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2),
        locator("exercise", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2)
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("transferFee", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("removeCollateral", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("redeemVaultBalance", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("liquidate", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("exercise", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("removeUnderlying", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainCreamFi1_1():
    category = "DeFiHackLabs"
    contract = '0x2db6c82ce72c8d7d770ba1b5f5ed0b6e075066d6'
    changeLoggingUpperBound(8)
    # deposit locator
    l1 = [
            locator("liquidateBorrow", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transferFrom", position=2),
            locator("repayBorrowBehalf", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transferFrom", position=2),
            locator("repayBorrow", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transferFrom", position=2),
            locator("mint", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transferFrom", position=2),
            locator("_addReserves", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transferFrom", position=2)
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
            locator("redeem", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transfer", position=1),
            locator("redeemUnderlying", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transfer", position=1),
            locator("borrow", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transfer", position=1),
            locator("_reduceReserves", FUNCTION, funcAddress = "0xff20817765cb7f73d4bde2e66e067e58d11095c2", \
                name="transfer", position=1)
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainCreamFi1_2():
    category = "DeFiHackLabs"
    contract = '0xd06527d5e56a3495252a528c4987003b712860ee'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
            locator("liquidateBorrow", SELFCALLVALUE),
            locator("repayBorrowBehalf", SELFCALLVALUE),
            locator("repayBorrow", SELFCALLVALUE),
            locator("mint", SELFCALLVALUE),
            locator("_addReserves", SELFCALLVALUE)
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
            locator("_reduceReserves", FALLBACK),
            locator("redeemUnderlying", FALLBACK),
            locator("borrow", FALLBACK),
            locator("_reduceReserves", FALLBACK)
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainIndexFi():
    category = "DeFiHackLabs"
    contract = '0x5bd628141c62a901e0a83e630ce5fafa95bbdee4'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("joinPool", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
        locator("joinswapExternAmountIn", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
        locator("joinswapPoolAmountOut", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
        locator("swapExactAmountIn", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
        locator("swapExactAmountOut", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),  
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("exitPool", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
        locator("exitswapPoolAmountIn", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
        locator("exitswapExternAmountOut", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
        locator("gulp", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
        locator("swapExactAmountIn", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
        locator("swapExactAmountOut", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainCreamFi2_1():  # crUSDC Token
    category = "DeFiHackLabs"
    contract = '0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322'
    changeLoggingUpperBound(10)
    # deposit locator
    l1 = [
            locator("liquidateBorrow", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transferFrom", position=2),
            locator("repayBorrowBehalf", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transferFrom", position=2),
            locator("repayBorrow", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transferFrom", position=2),
            locator("mint", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transferFrom", position=2),
            locator("_addReserves", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transferFrom", position=2)
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
            locator("redeem", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transfer", position=1),
            locator("redeemUnderlying", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transfer", position=1),
            locator("borrow", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transfer", position=1),
            locator("_reduceReserves", FUNCTION, funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
                name="transfer", position=1)
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainCreamFi2_2():  # crUSDT Token
    category = "DeFiHackLabs"
    contract = '0x797aab1ce7c01eb727ab980762ba88e7133d2157'
    changeLoggingUpperBound(10)
    # deposit locator
    l1 = [
            locator("liquidateBorrow", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transferFrom", position=2),
            locator("repayBorrowBehalf", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transferFrom", position=2),
            locator("repayBorrow", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transferFrom", position=2),
            locator("mint", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transferFrom", position=2),
            locator("_addReserves", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transferFrom", position=2)
    ]

    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
            locator("redeem", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transfer", position=1),
            locator("redeemUnderlying", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transfer", position=1),
            locator("borrow", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transfer", position=1),
            locator("_reduceReserves", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
                name="transfer", position=1)
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainCreamFi2_3():  # crUNI Token
    category = "DeFiHackLabs"
    contract = '0xe89a6d0509faf730bd707bf868d9a2a744a363c7'
    changeLoggingUpperBound(10)
    # deposit locator
    l1 = [
            locator("liquidateBorrow", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
            locator("repayBorrowBehalf", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
            locator("repayBorrow", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
            locator("mint", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2),
            locator("_addReserves", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transferFrom", position=2)
    ]
    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
            locator("redeem", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
            locator("redeemUnderlying", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
            locator("borrow", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1),
            locator("_reduceReserves", FUNCTION, funcAddress = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", \
                name="transfer", position=1)
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainCreamFi2_4():
    category = "DeFiHackLabs"
    contract = '0x8c3b7a4320ba70f8239f83770c4015b5bc4e6f91'
    changeLoggingUpperBound(10)
    # deposit locator
    l1 = [
            locator("liquidateBorrow", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transferFrom", position=2),
            locator("repayBorrowBehalf", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transferFrom", position=2),
            locator("repayBorrow", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transferFrom", position=2),
            locator("mint", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transferFrom", position=2),
            locator("_addReserves", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transferFrom", position=2)
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
            locator("redeem", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transfer", position=1),
            locator("redeemUnderlying", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transfer", position=1),
            locator("borrow", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transfer", position=1),
            locator("_reduceReserves", FUNCTION, funcAddress = "0x956f47f50a910163d8bf957cf5846d573e7f87ca", \
                name="transfer", position=1)
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3




def mainRariCapital1():
    category = "DeFiHackLabs"
    contract = '0xec260f5a7a729bb3d0c42d292de159b4cb1844a3'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("deposit", SELFCALLVALUE),
        locator("depositTo", SELFCALLVALUE),
        locator("exchangeAndDeposit", SELFCALLVALUE),
        locator("withdrawAndExchange", SELFCALLVALUE),
    ]

    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
        locator("withdraw", FALLBACK),
        locator("withdrawFrom", FALLBACK),
        locator("withdrawAndExchange", FALLBACK),
        locator("deposit", FALLBACK),
        locator("depositTo", FALLBACK),
    ]

    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



def mainVisorFi():
    category = "DeFiHackLabs"
    contract = '0xc9f27a50f82571c1c8423a42970613b8dbda14ef'
    changeLoggingUpperBound(10)
    # deposit locator
    l1 = [
            locator("deposit", FUNCTION, funcAddress = "0xf938424f7210f31df2aee3011291b658f872e91e", \
                name="transferFrom", position=2), 
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
            locator("withdraw", FUNCTION, funcAddress = "0xf938424f7210f31df2aee3011291b658f872e91e", \
                name="transfer", position=1), 
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    # one transaction to exploit, another one to withdraw
    # exploitTx = ["0x69272d8c84d67d1da2f6425b339192fa472898dce936f24818fda415c1c1ff3f", "0x6eabef1bf310a1361041d97897c192581cd9870f6a39040cd24d7de2335b4546"]

    # exploitTx = "0x69272d8c84d67d1da2f6425b339192fa472898dce936f24818fda415c1c1ff3f"

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainUmbrellaNetwork():
    category = "DeFiHackLabs"
    contract = '0xb3fb1d01b07a706736ca175f827e4f56021b85de'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("stake", FUNCTION, funcAddress = "0xb1bbeea2da2905e6b0a30203aef55c399c53d042", \
            name="transferFrom", position=2),
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("rescueToken", FUNCTION, funcAddress = "0xb1bbeea2da2905e6b0a30203aef55c399c53d042", \
            name="transfer", position=1),
        locator("withdraw", FUNCTION, funcAddress = "0xb1bbeea2da2905e6b0a30203aef55c399c53d042", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainRevestFi():
    category = "DeFiHackLabs"
    contract = '0xa81bd16aa6f6b25e66965a2f842e9c806c0aa11f'
    changeLoggingUpperBound(10)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawToken", FUNCTION, funcAddress = "0x56de8bc61346321d4f2211e3ac3c0a7f00db9b76", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainRevestFi_interface():
    category = "DeFiHackLabs"
    contract = '0x2320a28f52334d62622cc2eafa15de55f9987ed9'
    changeLoggingUpperBound(12)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = []
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3




def mainRoninNetwork():
    category = "DeFiHackLabs"
    contract = '0x8407dc57739bcda7aa53ca6f12f82f9d51c2f21e'
    changeLoggingUpperBound(4)
    # deposit locator
    l1 = [
        locator("deposit", SELFCALLVALUE), 
        locator("depositEthFor", SELFCALLVALUE),        
    ]
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawERC20For", FALLBACK), 
        locator("withdrawTokenFor", FALLBACK),
        locator("withdrawERC20", FALLBACK),
    ]
    f = FilterTx()
    exploitTx = "0xc28fad5e8d5e0ce6a2eaf67b6687be5d58113e16be590824d6cfa1a94467d0b7"
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3




def mainBeanstalkFarms():
    category = "DeFiHackLabs"
    contract = '0x3a70dfa7d2262988064a2d051dd47521e43c9bdd'
    changeLoggingUpperBound(4)
    l1 = [
        locator("exchange", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transferFrom", position=2),
        locator("exchange_underlying", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transferFrom", position=2),
        locator("add_liquidity", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transferFrom", position=2),
    ]
    l2 = []
    l3 = [
        locator("exchange", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transfer", position=1),
        locator("exchange_underlying", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transfer", position=1),
        locator("remove_liquidity", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transfer", position=1),
        locator("remove_liquidity_imbalance", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transfer", position=1),
        locator("remove_liquidity_one_coin", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transfer", position=1),
        locator("withdraw_admin_fees", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainBeanstalkFarms_interface():
    category = "DeFiHackLabs"
    contract = '0xc1e088fc1323b20bcbee9bd1b9fc9546db5624c5'
    changeLoggingUpperBound(6)
    l1 = []
    l2 = []
    l3 = []
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)
    return category, contract, executionList, accessList, exploitTx, l1, l2, l3




def mainHarmonyBridge():
    category = "DeFiHackLabs"
    contract = '0xf9fb1c508ff49f78b60d3a96dea99fa5d7f3a8a6'
    changeLoggingUpperBound(4)
    l1 = [
        locator("lockEth", SELFCALLVALUE),
    ]
    l2 = []
    l3 = [
        locator("unlockEth", FALLBACK),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



def mainXCarnival():
    category = "DeFiHackLabs"
    contract = '0x5417da20ac8157dd5c07230cfc2b226fdcfc5663'
    changeLoggingUpperBound(8)
    l1 = [
        locator("fallback", SELFCALLVALUE),
        locator("mint", SELFCALLVALUE),
        locator("repayBorrow", SELFCALLVALUE),
        locator("repayBorrowAndClaim", SELFCALLVALUE),
        locator("liquidateBorrow", SELFCALLVALUE),
    ]
    l2 = []
    l3 = [
        locator("redeem", FALLBACK),
        locator("redeemUnderlying", FALLBACK),
        locator("borrow", FALLBACK),
        locator("reduceReserves", FALLBACK),
        locator("fallback", FALLBACK),
        locator("repayBorrow", FALLBACK),
        locator("repayBorrowAndClaim", FALLBACK),
        locator("liquidateBorrow", FALLBACK),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



def mainRariCapital2_1():
    category = "DeFiHackLabs"
    contract = '0x26267e41ceca7c8e0f143554af707336f27fa051'
    changeLoggingUpperBound(10)
    l1 = [
        locator("mint", SELFCALLVALUE ),
        locator("repayBorrow", SELFCALLVALUE),
        locator("repayBorrowBehalf",SELFCALLVALUE ),
        locator("liquidateBorrow", SELFCALLVALUE),
        locator("fallback", SELFCALLVALUE),
        locator("repayBehalfExplicit", SELFCALLVALUE),
    ]
    l2 = []
    l3 = [
        locator("redeem", FALLBACK),
        locator("redeemUnderlying", FALLBACK),
        locator("borrow", FALLBACK),
        locator("_reduceReserves", FALLBACK),
        locator("_withdrawFuseFees", FALLBACK),
        locator("_withdrawAdminFees", FALLBACK),
        locator("repayBehalfExplicit", FALLBACK),
        locator("repayBehalf", FALLBACK),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3





def mainRariCapital2_2():
    category = "DeFiHackLabs"
    contract = '0xebe0d1cb6a0b8569929e062d67bfbc07608f0a47'
    changeLoggingUpperBound(10)
    l1 = [
        locator("mint", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2),
        locator("repayBorrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2),
        locator("repayBorrowBehalf", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2),
        locator("liquidateBorrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transferFrom", position=2),
    ]
    l2 = []
    l3 = [
        locator("redeem", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("redeemUnderlying", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("borrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("_reduceReserves", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("_withdrawFuseFees", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("_withdrawAdminFees", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3





def mainRariCapital2_3():
    category = "DeFiHackLabs"
    contract = '0xe097783483d1b7527152ef8b150b99b9b2700c8d'
    changeLoggingUpperBound(10)
    l1 = [
        locator("mint", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transferFrom", position=2),
        locator("repayBorrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transferFrom", position=2),
        locator("repayBorrowBehalf", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transferFrom", position=2),
        locator("liquidateBorrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transferFrom", position=2),
    ]
    l2 = []
    l3 = [
        locator("redeem", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("redeemUnderlying", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("borrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("_reduceReserves", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("_withdrawFuseFees", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("_withdrawAdminFees", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3





def mainRariCapital2_4():
    category = "DeFiHackLabs"
    contract = '0x8922c1147e141c055fddfc0ed5a119f3378c8ef8'
    changeLoggingUpperBound(10)
    l1 = [
        locator("mint", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transferFrom", position=2),
        locator("repayBorrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transferFrom", position=2),
        locator("repayBorrowBehalf", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transferFrom", position=2),
        locator("liquidateBorrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transferFrom", position=2),
    ]
    l2 = []
    l3 = [
        locator("redeem", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transfer", position=1),
        locator("redeemUnderlying", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transfer", position=1),
        locator("borrow", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transfer", position=1),
        locator("_reduceReserves", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transfer", position=1),
        locator("_withdrawFuseFees", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transfer", position=1),
        locator("_withdrawAdminFees", FUNCTION, fromAddr= "0x67db14e73c2dce786b5bbbfa4d010deab4bbfcf9", funcAddress = "0x853d955acef822db058eb8505911ed77f175b99e", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3




def mainDODO():
    category = "DeFiHackLabs"
    contract = '0x051ebd717311350f1684f89335bed4abd083a2b6'
    changeLoggingUpperBound(8)
    l1 = []
    l2 = []
    l3 = [
        locator("sellQuote", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("flashLoan", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("sellShares", FUNCTION, funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



def mainPickleFi():
    category = "DeFiHackLabs"
    contract = '0x6847259b2B3A4c17e7c43C54409810aF48bA5210'
    changeLoggingUpperBound(4)
    l1 = [
        locator("swapExactJarForJar", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("deposit", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("depositAll", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("harvest", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("leverageUntil", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("convertWETHPair", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("stake", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("convert", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
    ]
    l2 = []
    l3 = [
        locator("earn", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("yearn", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("inCaseTokensGetStuck", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("swapExactJarForJar", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("convert", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("harvest", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("withdraw", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("claimRewards", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("test_staking", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("test_jar_converter_curve_curve_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="approve", position=1),
        locator("test_jar_converter_curve_curve_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="approve", position=1),
        locator("test_jar_converter_curve_curve_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="approve", position=1),
        locator("test_jar_converter_curve_curve_3", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="approve", position=1),
        locator("test_jar_converter_curve_curve_4", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="approve", position=1),
        locator("test_jar_converter_curve_uni_0_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="approve", position=1),
        locator("test_jar_converter_curve_uni_0_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="approve", position=1),
        locator("test_jar_converter_curve_uni_0_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="approve", position=1),
        locator("test_jar_converter_curve_uni_0_3", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="approve", position=1),
        locator("test_jar_converter_curve_uni_1_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="approve", position=1),
        locator("test_jar_converter_curve_uni_1_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="approve", position=1),
        locator("test_jar_converter_curve_uni_1_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="approve", position=1),
        locator("test_jar_converter_curve_uni_1_3", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="approve", position=1),
        locator("test_jar_converter_curve_uni_2_3", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_0_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_1_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_2_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_3_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_0_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_1_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_2_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_3_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_4_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_0_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1), 
        locator("test_jar_converter_uni_curve_1_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_2_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_curve_3_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_uni_0", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_uni_1", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_uni_2", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
        locator("test_jar_converter_uni_uni_3", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f",
                name="approve", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



def mainNomad():
    category = "DeFiHackLabs"
    contract = '0x88a69b4e698a4b090df6cf5bd7b2d47325ad30a3'
    changeLoggingUpperBound(4)
    l1 = [
        locator("send", FUNCTION, fromAddr = "0x15fda9f60310d09fea54e3c99d1197dff5107248", funcAddress = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", \
            name="transferFrom", position=2),
    ]
    l2 = []
    l3 = [
        locator("handle", FUNCTION, fromAddr = "0x15fda9f60310d09fea54e3c99d1197dff5107248", funcAddress = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3





def mainPolyNetwork():
    category = "DeFiHackLabs"
    contract = '0x250e76987d838a75310c34bf422ea9f1ac4cc906'
    changeLoggingUpperBound(4)
    l1 = [
        locator("lock", SELFCALLVALUE),
    ]
    l2 = []
    l3 = [
        locator("unlock", FALLBACK, fromAddr = "0x250e76987d838a75310c34bf422ea9f1ac4cc906"),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



def mainPunk_1():
    category = "DeFiHackLabs"
    contract = '0x3BC6aA2D25313ad794b2D67f83f21D341cc3f5fb'
    changeLoggingUpperBound(4)
    l1 = []
    l2 = []
    l3 = [
        locator("withdrawTo", FUNCTION, fromAddr = "0x3bc6aa2d25313ad794b2d67f83f21d341cc3f5fb", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("withdrawToForge", FUNCTION, fromAddr = "0x3bc6aa2d25313ad794b2d67f83f21d341cc3f5fb", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainPunk_2():
    category = "DeFiHackLabs"
    contract = '0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D'
    changeLoggingUpperBound(4)
    l1 = []
    l2 = []
    l3 = [
        locator("withdrawTo", FUNCTION, fromAddr = "0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("withdrawToForge", FUNCTION, fromAddr = "0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3


def mainPunk_3():
    category = "DeFiHackLabs"
    contract = '0x929cb86046E421abF7e1e02dE7836742654D49d6'
    changeLoggingUpperBound(4)
    l1 = []
    l2 = []
    l3 = [
        locator("withdrawTo", FUNCTION, fromAddr = "0x929cb86046E421abF7e1e02dE7836742654D49d6", funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("withdrawToForge", FUNCTION, fromAddr = "0x929cb86046E421abF7e1e02dE7836742654D49d6", funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
    ]
    f = FilterTx()
    exploitTx = f.contract2ExploitTx(contract)
    executionList, accessList = analyzeAllTx(category, contract, l1, l2, l3)

    return category, contract, executionList, accessList, exploitTx, l1, l2, l3



def storeAllInfoInFile(benchmarkName, category, contract, executionList, accessList, exploitTx, l1, l2, l3):
    # use pickle to store the data
    with open("data/{}_executionList.pkl".format(benchmarkName), "wb") as f:
        pickle.dump(executionList, f)
    with open("data/{}_accessList.pkl".format(benchmarkName), "wb") as f: 
        pickle.dump(accessList, f)
    with open("data/{}_others.pkl".format(benchmarkName), "wb") as f:
        pickle.dump((category, contract, exploitTx, l1, l2, l3), f)
    
def loadAllInfoFromFile(benchmarkName):
    if benchmarkName == "Warp_interface2":
        print("now is the time")
    try: 
        category, contract, executionList, accessList, exploitTx, l1, l2, l3 = None, None, None, None, None, None, None, None
        # use pickle to load the data
        with open("data/{}_executionList.pkl".format(benchmarkName), "rb") as f:
            executionList = pickle.load(f)
        with open("data/{}_accessList.pkl".format(benchmarkName), "rb") as f:
            accessList = pickle.load(f)
        with open("data/{}_others.pkl".format(benchmarkName), "rb") as f:
            category, contract, exploitTx, l1, l2, l3 = pickle.load(f)

        newAccessList = []
        for ii, (tx, funcCallList) in enumerate(accessList):
            if funcCallList == [] or funcCallList == [[]]:
                continue
            if tx == exploitTx and len(accessList) > ii + 1 and accessList[ii + 1][0] != exploitTx:
                newAccessList.append((tx, funcCallList))
                break
            newAccessList.append((tx, funcCallList))
        
        return category, contract, executionList, newAccessList, exploitTx, l1, l2, l3
    except:
        return None, None, None, None, None, None, None, None




def benchmarkName2TxCount(benchmark, accesslistTable):
    for category, benchmarkName, contract, accessList, exploitTx, l1, l2, l3 in accesslistTable:
        txList = []
        print( "\"" + benchmarkName + "\": ", end = "")
        for tx, funcCallList in accessList:
            if tx not in txList:
                txList.append(tx)
            if tx == exploitTx:
                break
        print(len(txList), end = ",\n")


AllFuncs = [mainRoninNetwork, mainHarmonyBridge, mainNomad, mainPolyNetwork] + \
            [mainbZx2, mainWarp, mainWarp_interface, mainWarp_interface2, mainCheeseBank_1, mainCheeseBank_2, mainCheeseBank_3, mainInverseFi, \
                    mainCreamFi1_1, mainCreamFi1_2, mainCreamFi2_1, mainCreamFi2_2, mainCreamFi2_3, mainCreamFi2_4, \
                    mainRariCapital1, mainRariCapital2_1, mainRariCapital2_2, mainRariCapital2_3, \
                    mainRariCapital2_4, mainXCarnival] + \
            [mainHarvest1_fUSDT, mainHarvest2_fUSDC, mainValueDeFi, mainYearn1, mainYearn1_interface, mainVisorFi, \
                    mainUmbrellaNetwork, mainPickleFi] + \
            [mainEminence, mainOpyn, mainIndexFi, mainRevestFi, mainRevestFi_interface, mainDODO, mainPunk_1, mainPunk_2, \
                    mainPunk_3, mainBeanstalkFarms, mainBeanstalkFarms_interface]


def getFuncByIndex(index):
    return AllFuncs[index]

def allTransferFuncs():
    for func in AllFuncs:
        name = func.__name__[4:]
        print("\"{}\": [".format(name), end = "\n")
        l1, l2, l3 = func()
        temp = []
        temp2 = []

        print("\t[", end = "")
        for l in l1:
            if l.targetFunc in temp:
                continue
            print("\"{}\", ".format(l.targetFunc), end = "")
            temp.append(l.targetFunc)
        print("],")
        
        print("\t[", end = "")
        for l in l3:
            if l.targetFunc in temp2:
                continue
            print("\"{}\", ".format(l.targetFunc), end = "")
            temp2.append(l.targetFunc)
        print("],")

        print("],")

def allNonReadOnlyFuncs(accesslistTable):
    crawlEtherscan = CrawlEtherscan()
    for category, benchmarkName, contract, accessList, exploitTx, l1, l2, l3 in accesslistTable:
        print("====== benchmark {}: ".format(benchmarkName), end = " ")
        # if benchmarkName not in verboseBenchmarks:
        #     continue
        if contract in proxyMap:
            contract = proxyMap[contract]
        print(contract)
        # build read-only functions
        ABI = crawlEtherscan.Contract2ABI(contract)
        readOnlyFunctions = ["fallback"]
        nonReadOnlyFunctions = []
        for function in ABI:
            # if "name" in function and function["name"] == "isETH":
            #     print(function)
            if function["type"] == "function" and (function["stateMutability"] == "view" or function["stateMutability"] == "pure"):
                if function["name"] not in readOnlyFunctions:
                    readOnlyFunctions.append(function["name"])
            if function["type"] == "function" and (function["stateMutability"] != "view" and function["stateMutability"] != "pure"):
                if function["name"] not in nonReadOnlyFunctions:
                    nonReadOnlyFunctions.append(function["name"])
        # print(readOnlyFunctions)
        print(nonReadOnlyFunctions)



def reformatExecutionTable(executionTable: list):
    # refactor improper formatted entry
    newExecutionTable = []
    for category, benchmarkName, contract, executionList, exploitTx, l1, l2, l3 in executionTable:
        counter = 0
        new_executionList = []
        for ii in range(len(executionList)):
            execution = executionList[ii]
            if isinstance(execution[1], list):
                if len(execution[1]) == 1:
                    executionList[ii] = (execution[0], execution[1][0].to_dict())
                    new_executionList.append(  (execution[0], execution[1][0].to_dict() ) )
                else: # means one execution contains multiple target locations
                    executionList[ii] = [execution[0], []]
                    gasUsed = []
                    for jj in range(len(execution[1])):
                        gas = execution[1][jj].metaData['gas']
                        if gas not in gasUsed: # there is a possibility of duplicate counting
                            executionList[ii][1].append(  execution[1][jj].to_dict() )
                    if len( executionList[ii][1]) == 0 and benchmarkName != "Eminence":
                        sys.exit("invariantInfer: there is a bug")
                    elif len( executionList[ii][1]) == 1:
                        executionList[ii][1] = executionList[ii][1][0].to_dict()
                    else:
                        if counter == 0:
                            print("{} has one function call with several transfers".format(benchmarkName))
                            counter = 1
                    for jj in range(len(executionList[ii][1])):
                        new_executionList.append( (executionList[ii][0], executionList[ii][1][jj] )  )
            else:
                sys.exit("not isinstance(execution[1], list)")
        newExecutionTable.append( (category, benchmarkName, contract, new_executionList, exploitTx, l1, l2, l3) )
    return newExecutionTable





def main():
# # ## ==============================================================================
    executionTable = []
    accesslistTable = []
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    # if arg == "ReCollect":
    # AllFuncs = [mainWarp_interface2] 
    # for func in AllFuncs:
    #     category, contract, executionList, accessList, exploitTx, l1, l2, l3 = func()
    #     benchmarkName = func.__name__[4:]
    #     print("==========", benchmarkName )
    #     storeAllInfoInFile(benchmarkName, category, contract, executionList, accessList, exploitTx, l1, l2, l3)
    #     gc.collect()
    #     return
    # if arg == "ReStore":
    # totalLen = 0
    # for func in AllFuncs:
    #     benchmarkName = func.__name__[4:]
    #     print("==========", benchmarkName )
    #     # if benchmarkName != "IndexFi":
    #     #     continue
    #     category = None
    #     category, contract, executionList, accessList, exploitTx, l1, l2, l3 = loadAllInfoFromFile(benchmarkName)
    #     print("len(executionList):", len(executionList))
    #     print("len(accessList):", len(accessList))
    #     totalLen += len(accessList)
    #     executionTable.append( (category, benchmarkName, contract, executionList, exploitTx, l1, l2, l3) )
    #     accesslistTable.append( (category, benchmarkName, contract, accessList, exploitTx, l1, l2, l3) )

    # print("totalLen:", totalLen)
    # # store executionTable and accesslistTable
    # with open("data/executionTable.pkl", "wb") as f:
    #     pickle.dump(executionTable, f)
    # with open("data/accesslistTable.pkl", "wb") as f:
    #     pickle.dump(accesslistTable, f)
    # return

    
    # # read executionTable and accesslistTable
    with open("data/executionTable.pkl", "rb") as f:
        executionTable = pickle.load(f)
        executionTable = reformatExecutionTable(executionTable)

    with open("data/accesslistTable.pkl", "rb") as f:
        accesslistTable = pickle.load(f)
    
    # inferAccessControl(accesslistTable)
    # inferDataFlows(executionTable)
    # inferMoneyFlows(executionTable)
    # inferDataFlows(executionTable)
    # inferGasControl(accesslistTable)
    
    if arg == "AC":
        start = time.time()
        print("\n\n\n\n\n\n\n\n\nInvariant: access control")
        inferAccessControl(accesslistTable)
        gc.collect()

    if arg == "TL":
        print("\n\n\n\n\n\n\n\n\nInvariant: time locks")
        inferTimeLocks(accesslistTable)
        gc.collect()
        return

    if arg == "GC":
        print("\n\n\n\n\n\n\n\n\nInvariant: gas control")
        inferGasControl(accesslistTable)
        gc.collect()
        return

    if arg == "RE":
        print("Invariant: reentrancy")
        inferReentrancy(accesslistTable)
        gc.collect()
        return

    if arg == "SS":
        print("\n\n\n\n\n\n\n\n\nInvariant: special storage")
        inferSpecialStorage(accesslistTable)
        gc.collect()
        return

    if arg == "OR":
        AllBenchmarksReserved = ["bZx2", "Warp_interface", "CheeseBank_1", "CheeseBank_2", "CheeseBank_3", "InverseFi", \
                        "CreamFi2_1", "CreamFi2_2", "CreamFi2_3", "CreamFi2_4", "Harvest1_fUSDT", "Harvest2_fUSDC", \
                        "ValueDeFi"]
        print("\n\n\n\n\n\n\n\n\nInvariant: oracle range")
        inferOracleRange(AllBenchmarksReserved)
        gc.collect()
        return

    if arg == "DF":
        # # # # # # precheck(executionTable)
        print("\n\n\n\n\n\n\n\n\nInvariant: data flow")
        inferDataFlows(executionTable)
        gc.collect()
        return

    if arg == "MF":
        print("\n\n\n\n\n\n\n\n\nInvariant: money flow")
        inferMoneyFlows(executionTable) 
        gc.collect()
        return 

    # end = time.time()
    # print("time elapsed: ", end - start)



if __name__ == "__main__":
    main()

    # # category 1: bridge
    # mainHarmonyBridge()
    # mainHarmonyBridge_interface
    # mainNomad()
    # mainPolyNetwork()
    
    # # category 2: lending/borrowing
    # mainbZx2()  # also margin trading 
    # mainWarp()
    # mainWarp_interface()
    # mainCheeseBank_1()
    # mainCheeseBank_2()
    # mainCheeseBank_3()
    # mainInverseFi()
    # mainCreamFi1_1() # en-entrancy borrowing
    # mainCreamFi2_1()
    # mainCreamFi2_2()
    # mainCreamFi2_3()
    # mainCreamFi2_4()
    # mainRariCapital1()
    # mainRariCapital2_1()
    # mainRariCapital2_2()
    # mainRariCapital2_3()
    # mainRariCapital2_4()
    # mainXCarnival()

    # # category 3: yield farming
    # mainHarvest1_fUSDT()
    # mainHarvest2_fUSDC()
    # mainValueDeFi()
    # mainYearn1()
    # mainVisorFi()
    # mainUmbrellaNetwork()
    # mainPickleFi()

    # # category 4: other types
    # mainEminence()
    # mainOpyn()
    # mainIndexFi()
    # mainRevestFi()
    # mainDODO()
    # mainPunk_1()
    # mainPunk_2()
    # mainPunk_3()
    # mainBeanstalkFarms() 