import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from parserPackage.parser import *
from parserPackage.parserRunnerUtils import *

import pickle


def writeDataSource(contract, tx, dataSourceMapList):
    path = SCRIPT_DIR + "/../cache/" + contract + "/{}.pickle".format(tx)
    # print("write", path)
    # print(dataSourceMapList)
    with open(path, 'wb') as f:
        pickle.dump(dataSourceMapList, f)


def writeAccessList(contract, tx, accessList):
    path = SCRIPT_DIR + "/../cache/" + contract + "_Access/{}.pickle".format(tx)
    # print("write", path)
    # print(dataSourceMapList)
    with open(path, 'wb') as f:
        pickle.dump(accessList, f)


def writeSplitedTraceTree(contract, tx, splitedTraceTree):
    path = SCRIPT_DIR + "/../cache/" + contract + "_SplitedTraceTree/{}.pickle".format(tx)

    print("write to ", path)
    # print("write", path)
    # print(dataSourceMapList)
    with open(path, 'wb') as f:
        pickle.dump(splitedTraceTree, f)





def testEminence():
    changeLoggingUpperBound(4)
    # path = "./YearnHackTxFull.pickle.gz"
    # trace = readCompressedJson(path)
    # metaTraceTree = p.parseLogs(YearnContractAddress, YearnHackTx, trace)

    
    contractAddress = '0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8'
    EminenceHackTx = "0x3503253131644dd9f52802d071de74e456570374d586ddd640159cf6fb9b8ad8"

    EminenceHackTx = "0xef1a1f263e2527e5629765cb7e9ad73fbb353b998eb34afc404e636d38be77cb"
    
    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, EminenceHackTx)
    trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("buy", FUNCTION, name="transferFrom", position=2)
    ]
    # transfer ==> sell 
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("sell", FUNCTION, name="transfer", position=1) 
    ]
    # transferFrom ==> buy

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, EminenceHackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testHarvest1_fUSDT():
    p = VmtraceParser()
    changeLoggingUpperBound(6)
    contractAddress = '0x053c80ea73dc6941f518a68e2fc52ac45bde7c9c'
    HackTx = "0x0fc6d2ca064fc841bc9b1c1fad1fbb97bcea5c9a1b2b66ef837f1227e06519a6"
    # HackTx = "0x4211d3dff0c75ac4667f91e8836da3ebe5d3f8faf4cb3861037cf5afaef07cfa"
    # HackTx = "0x37f445e1df0aa320f33d21036fefba090ed591e7b6a5e64a5fc59ac87d14da65"


    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # path = "Harvest1_fUSDT.pickle.gz"  

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
            locator("deposit", FUNCTION, name="transferFrom", position=2),
            locator("depositFor", FUNCTION, name="transferFrom", position=2)
    ]
    # safeTransferFrom ==> _deposit ==> deposit
    #                               ==> depositFor

    # invest locator
    l2 = [
        locator("doHardWork", FUNCTION, name="transfer", position=1),
        locator("rebalance", FUNCTION, name="transfer", position=1)
    ]
    # transfer ==> invest ==> doHardWork(onlyControllerOrGovernance)
    #                     ==> rebalance(onlyControllerOrGovernance)

    # Withdraw locator
    l3 = [ locator("withdraw", FUNCTION, name="transfer", position=1) ]
    #  transfer ==> withdraw

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)
    print(splitedTraceTree)
    # for i in range(len(splitedTraceTree)):
    #     print(i)
    #     print(splitedTraceTree[i])
    #     print("=========================================")

    writeAccessList(contractAddress, HackTx, accessList)
    writeSplitedTraceTree(contractAddress, HackTx, splitedTraceTree)
    writeDataSource(contractAddress, HackTx, dataSourceMapList)


def testHarvest2_fUSDC():
    p = VmtraceParser()
    changeLoggingUpperBound(6)
    contractAddress = '0xf0358e8c3cd5fa238a29301d0bea3d63a17bedbe'
    HackTx = "0x35f8d2f572fceaac9288e5d462117850ef2694786992a8c3f6d02612277b0877"
#     HackTx = "0xdc184efbffc146d306541b9866b344d01a515f21c854c70033aca207745c8d5a"
    HackTx = "0x579021dd520b36f37d28d8351e905ecddd64ec5460579cf0bfca99ca4295ea0e"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # path = "Harvest1_fUSDT.pickle.gz"

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
            locator("deposit", FUNCTION, name="transferFrom", position=2),
            locator("depositFor", FUNCTION, name="transferFrom", position=2)
    ]
    # safeTransferFrom ==> _deposit ==> deposit
    #                               ==> depositFor

    # invest locator
    l2 = [
        locator("doHardWork", FUNCTION, name="transfer", position=1),
        locator("rebalance", FUNCTION, name="transfer", position=1)
    ]
    # transfer ==> invest ==> doHardWork(onlyControllerOrGovernance)
    #                     ==> rebalance(onlyControllerOrGovernance)

    # Withdraw locator
    l3 = [ locator("withdraw", FUNCTION, name="transfer", position=1) ]
    #  transfer ==> withdraw
    
    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)
    for splitedTrace in splitedTraceTree:
        print(splitedTrace)
    print(splitedTraceTree)

#     writeAccessList(contractAddress, HackTx, accessList)
#     writeSplitedTraceTree(contractAddress, HackTx, splitedTraceTree)


# title="Benchmarks_Traces/FlashSyn/Txs/
# 0x85ca13d8496b2d22d6518faeb524911e096dd7e0/
# 0x442703a4ddbd4f2b80508b44b2456e3f92cfb47d67b441380c8c1ad726ffaa15.json.gz"

def testbZx2():
    p = VmtraceParser()
    changeLoggingUpperBound(16)
    contractAddress = '0x85ca13d8496b2d22d6518faeb524911e096dd7e0'
    HackTx = "0x762881b07feb63c436dee38edd4ff1f7a74c33091e534af56c9f7d49b5ecac15"
# #     HackTx = "0x95ca6c8f951fb5ee5af02e70f972d1fcd877a731d0b42a5d80413ec7e3068cf1"
#     HackTx = "0x9ed7b3f4fbcc5fbb38c211d8949b688a4fbcafe5bdd137e0310487d0a0baadc8"
# #     HackTx = "0xd5f7c3902d3cd525ff4e89c7cffa18e090b82a7b6fcd778398e06c7519a16b21"
    HackTx = "0x762881b07feb63c436dee38edd4ff1f7a74c33091e534af56c9f7d49b5ecac15"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # path = "Harvest1_fUSDT.pickle.gz"

    # trace = readCompressedJson(path)

    # deposit locator
    l1 = [
        locator("borrowTokenFromDeposit", FUNCTION, fromAddr= "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",\
                name="transferFrom", position=2),
        locator("borrowTokenFromDeposit", SELFCALLVALUE),
        locator("mintWithEther", SELFCALLVALUE),
        locator("flashBorrowToken", SELFCALLVALUE),
        locator("mint", SELFCALLVALUE),
        locator("marginTradeFromDeposit", SELFCALLVALUE),
    ]
    # msg.value ==> mintWithEther
    #           ==> flashBorrowToken
    #           ==> borrowTokenFromDeposit
    #           ==> _mintToken (internal) ==> mint
    #           ==> _borrowTokenAndUseFinal (internal) ==> borrowTokenFromDeposit
    #                                                  ==> _borrowTokenAndUse (internal) ==> marginTradeFromDeposit
    #           ==> _verifyTransfers (internal) ==> _borrowTokenAndUseFinal (internal) ==> borrowTokenFromDeposit
    #                                                                                  ==> _borrowTokenAndUse (internal) ==> marginTradeFromDeposit



    # invest locator
    l2 = []  
    # Withdraw locator
    l3 = [
        locator("burn", FUNCTION, fromAddr= "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", \
                name="transfer", position=1),
        locator("burnToEther", FUNCTION, name="claimEther", position=1),
        locator("borrowTokenFromDeposit", FUNCTION, name="claimEther", position=1),
        locator("marginTradeFromDeposit", FUNCTION, name="claimEther", position=1),
        locator("flashBorrowToken", FUNCTION, fromAddr = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",\
                name="transfer", position=1),
    ]  # claimEther ==> burnToEther
       #            ==> _verifyTransfers ==> _borrowTokenAndUseFinal  ==> borrowTokenFromDeposit
       #                                                              ==> _borrowTokenAndUse     ==> marginTradeFromDeposit
       
       # _transfer ==> burnToEther
       #           ==> burn
       #           ==> _verifyTransfers  ==> _borrowTokenAndUseFinal  ==> borrowTokenFromDeposit
       #                                                              ==> _borrowTokenAndUse     ==> marginTradeFromDeposit

       # _transferFrom ==> _mintToken ==> _verifyTransfers(transfer to bZxVault) ==> _borrowTokenAndUseFinal  ==> borrowTokenFromDeposit
       #
    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(10)


def testWarp():
    p = VmtraceParser()
    changeLoggingUpperBound(4)
    
    contractAddress = '0x6046c3Ab74e6cE761d218B9117d5c63200f4b406'
    WarpHackTx = "0x8bb8dc5c7c830bac85fa48acad2505e9300a91c3ff239c9517d0cae33b595090"
    WarpHackTx = "0x276f354e606363898dd7578bc93e9c0c1191c1dc95f6311a451a02da18e67545"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, WarpHackTx)
    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("repayBorrow", FUNCTION, name="transferFrom", position=2),
        locator("_repayLiquidatedLoan", FUNCTION, name="transferFrom", position=2),   # onlyWarpControl
        locator("lendToWarpVault", FUNCTION, name="transferFrom", position=2)
    ]
    # safeTransferFrom ==> lendToWarpVault
    #                  ==> repayBorrow
    #                  ==> _repayLiquidatedLoan(onlyWarpControl)

    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
        locator("_borrow", FUNCTION, name="transfer", position=1),  # onlyWarpControl
        locator("redeem", FUNCTION, name="transfer", position=1)
    ]
    # safeTransfer ==> withdrawFees(onlyWarpTeam)
    #              ==> redeem
    #              ==> _borrow(onlyWarpControl)

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, WarpHackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)


def testWarp_interface():
    p = VmtraceParser()
    changeLoggingUpperBound(4)
    contractAddress = '0xba539b9a5c2d412cb10e5770435f362094f9541c'
    HackTx = "0x8bb8dc5c7c830bac85fa48acad2505e9300a91c3ff239c9517d0cae33b595090"
    HackTx = "0xa53c987280acb1cd58b901e24078b16fd17cf44cddc0211cfab14f12ac3567b4"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)

    # deposit locator
    l1 = []

    # invest locator
    l2 = []

    # Withdraw locator
    l3 = []

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)





def testCheeseBank_1(): # USDC
    p = VmtraceParser()
    changeLoggingUpperBound(4)
    contractAddress = '0x5E181bDde2fA8af7265CB3124735E9a13779c021'
    HackTx = "0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    
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
    # doTransferIn ==> _becomeImplementation ==> _becomeImplementation(Only Admin)
    #                                        ==> _setImplementation(Only Admin)
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> repayBorrowFresh ==> repayBorrowInternal  ==> repayBorrow
    #                                   ==> repayBorrowBehalfInternal ==> repayBorrowBehalf
    #                                   ==> liquidateBorrowFresh ==> liquidateBorrowInternal ==> liquidateBorrow
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves 
    #              
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
    # transfer ==> doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                                            ==> redeemUnderlyingInternal ==> redeemUnderlying
    #                            ==> borrowFresh ==> borrowInternal ==> borrow
    #                            ==> _reduceReservesFresh ==> _reduceReserves

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testCheeseBank_2():  # USDT
    p = VmtraceParser()
    changeLoggingUpperBound(4)
    
    contractAddress = '0x4c2a8A820940003cfE4a16294B239C8C55F29695'
    HackTx = "0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    
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
    # doTransferIn ==> _becomeImplementation ==> _becomeImplementation(Only Admin)
    #                                        ==> _setImplementation(Only Admin)
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> repayBorrowFresh ==> repayBorrowInternal  ==> repayBorrow
    #                                   ==> repayBorrowBehalfInternal ==> repayBorrowBehalf
    #                                   ==> liquidateBorrowFresh ==> liquidateBorrowInternal ==> liquidateBorrow
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves 
    #              
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
    # transfer ==> doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                                            ==> redeemUnderlyingInternal ==> redeemUnderlying
    #                            ==> borrowFresh ==> borrowInternal ==> borrow
    #                            ==> _reduceReservesFresh ==> _reduceReserves


    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testCheeseBank_3(): # DAI
    p = VmtraceParser()
    changeLoggingUpperBound(4)
    
    contractAddress = '0xA80e737Ded94E8D2483ec8d2E52892D9Eb94cF1f'
    HackTx = "0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc"
    # 0x02a54ffebfbea9584796fcc0592e926bc5adc9b18aa453688ed8e30cbacf10bd
    # 

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    
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
    # doTransferIn ==> _becomeImplementation ==> _becomeImplementation(Only Admin)
    #                                        ==> _setImplementation(Only Admin)
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> repayBorrowFresh ==> repayBorrowInternal  ==> repayBorrow
    #                                   ==> repayBorrowBehalfInternal ==> repayBorrowBehalf
    #                                   ==> liquidateBorrowFresh ==> liquidateBorrowInternal ==> liquidateBorrow
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves 
    #              
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
    # transfer ==> doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                                            ==> redeemUnderlyingInternal ==> redeemUnderlying
    #                            ==> borrowFresh ==> borrowInternal ==> borrow
    #                            ==> _reduceReservesFresh ==> _reduceReserves

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testValueDeFi():  # yield earning
    p = VmtraceParser()
    changeLoggingUpperBound(4)
    contractAddress = '0xddd7df28b1fb668b77860b473af819b03db61101'
    HackTx = "0x46a03488247425f845e444b9c10b52ba3c14927c687d38287c0faddc7471150a"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # path = "Harvest1_fUSDT.pickle.gz"

    # trace = readCompressedJson(path)

    # deposit locator # originally hacker deposited DAI, but ValueDeFi converted it to CRV
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
    # CRV transfer => _deposit ==> depositFor  ==> deposit
    #                          ==> depositAllFor ==> depositAll

    # invest locator
    l2 = []


    # Withdraw locator
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
    ]
    # safeTransfer ==> earn(external) ==> _deposit ==> depositFor(external) ==> deposit
    #                                              ==> depositAllFor(external) ==> depositAll
    #              ==> convert_nonbased_want
    #              ==> earnExtra(only governance)
    #              ==> harvest 
    #              ==> claimInsurance(only controller or governance)
    #              ==> governanceRecoverUnsupported(only governance)
    #              ==> withdrawFor(external) ==> withdraw(external)

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testYearn1():  # 
    p = VmtraceParser()
    changeLoggingUpperBound(4)
    # 0x9c211bfa6dc329c5e757a223fb72f5481d676dc1
    contractAddress = '0x9c211bfa6dc329c5e757a223fb72f5481d676dc1'
    HackTx = "0xf6022012b73770e7e2177129e648980a82aab555f9ac88b8a9cda3ec44b30779"
    HackTx = "0x35803833a3c9f838a6e75f0d68691d8f0284d448cfd8b00715b31e667b440eac"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = []

    # invest locator
    l2 = []

    # Withdraw locator
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
    # safeTransfer ==> withdraw
    #              ==> withdrawAll
    #              ==> migrate
    #              ==> forceW
    #              ==> drip ==> forceD
    #                       ==> forceW
    #                       ==> rebalance(public) ==> deposit
    #                                             ==> withdraw
    
    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)


def testYearn_interface():  # 
    p = VmtraceParser()
    changeLoggingUpperBound(5)
    # 0x9c211bfa6dc329c5e757a223fb72f5481d676dc1
    contractAddress = '0xacd43e627e64355f1861cec6d3a6688b31a6f952'
    HackTx = "0xf6022012b73770e7e2177129e648980a82aab555f9ac88b8a9cda3ec44b30779"
    HackTx = "0xc8bf69ef3a5e418c74b5099af883edee8cdf9b3bf47ae0d5fa7fe4c7c011af63"  # mint CHI tokens
    HackTx = "0x7ae864faf81979eba3bffa7a2a72f4ded858694ced79c63d613020d064bc06f4"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = [
        locator("deposit", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transferFrom", position=2),
        locator("depositAll", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
                name="transferFrom", position=2),

    ]
    # transferFrom ==> deposit ==> depositAll

    # invest locator
    l2 = []

    # Withdraw locator
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
    # safeTransfer ==> earn
    #              ==> harvest
    #              ==> withdraw ==> withdrawAll

    
    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    # 11267
    printdataSourceMapList(dataSourceMapList)
    print(accessList)



def testInverseFi(): # 
    p = VmtraceParser()
    changeLoggingUpperBound(6)
    contractAddress = '0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670'
    HackTx = "0x958236266991bc3fe3b77feaacea120f172c0708ad01c7a715b255f218f9313c"
    HackTx = "0x368d447ecdc3b55da99673f46bb01af1a6910d49fa088a5705e821449d833af4"
    HackTx = "0x524e2bde2adc3f659063bbd9ff04155ee83bcd76a0a0783929e4b80f7ae52f78"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/FlashSyn/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    
    # deposit locator
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
    # doTransferIn ==> mintFresh ==> mintInternal ==> mint
    #              ==> repayBorrowFresh ==> repayBorrowInternal ==> repayBorrow
    #                                   ==> repayBorrowBehalfInternal ==> repayBorrowBehalf
    #                                   ==> liquidateBorrowFresh ==> liquidateBorrowInternal ==> liquidateBorrow
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves

    # invest locator
    l2 = [
    ]

    # Withdraw locator
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
    # doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                               ==> redeemUnderlyingInternal ==> redeemUnderlying
    #               ==> borrowFresh ==> borrowInternal ==> borrow
    #               ==> _reduceReservesFresh ==> _reduceReserves

    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(10)



def runAllCases():
    testEminence()
    testHarvest1_fUSDT()
    testHarvest2_fUSDC()

    testbZx2()
    testWarp()
    testCheeseBank_1()
    testCheeseBank_2()
    testCheeseBank_3()
    testValueDeFi()
    testYearn1()
    testInverseFi()


if __name__ == "__main__":
#     runAllCases()
    testInverseFi()
#     testValueDeFi()
#     testbZx2()
#     testYearn1()
#     testYearn_interface()
#     testInverseFi()
#     testEminence()
#     testYearn_interface()
#     testbZx2()
#     testInverseFi()
#     testValueDeFi()
#     testHarvest2_fUSDC()



