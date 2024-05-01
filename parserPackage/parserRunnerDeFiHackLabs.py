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






def testOpyn():
    changeLoggingUpperBound(4)
    contractAddress = '0x951d51baefb72319d9fbe941e1615938d89abfe2'
    HackTx = "0x351bcbb182cb11cecb0d50d9f1bf45bd6820b71f7de5ec1ef607518865d43dc2"

    HackTx = "0xa14d0f59b67b3b5b53ce5af459c9495505aa05aa744026a7e210c33d41b19236"


    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
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
    # transferFrom ==> sellOTokens
    #              ==> uniswapBuyOToken
    #              ==> addERC20Collateral
    #              ==> _exercise(internal) ==> exercise

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
    # transfer ==> transferCollateral ==> transferFee(onlyOwner)
    #                                 ==> removeCollateral
    #                                 ==> redeemVaultBalance
    #                                 ==> liquidate
    #                                 ==> _exercise(internal) ==> exercise
    #          ==> transferUnderlying ==> removeUnderlying
    #                                 ==> redeemVaultBalance



    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testCreamFi1_1():
    changeLoggingUpperBound(8)
    contractAddress = '0x2db6c82ce72c8d7d770ba1b5f5ed0b6e075066d6'
    HackTx = "0x0016745693d68d734faa408b94cdf2d6c95f511b50f47b03909dc599c1dd9ff6"
    # HackTx = "0xc3c7793ee56db1a1715addb463698d54a20803e4391cf36b2a096dd621c08dc5"
    # HackTx = "0x4894bef0c828e2a32c8a0da85babe0bafa0a95aedfac084c98f81e9ec5c210a2"
    # HackTx = "0x0db8912ada243246d4bfa269f7f2a96dc8eae549c0cb878b7e915857e7dc3806"
    # 0xc3c7793ee56db1a1715addb463698d54a20803e4391cf36b2a096dd621c08dc5
    # 0x0db8912ada243246d4bfa269f7f2a96dc8eae549c0cb878b7e915857e7dc3806
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
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
    # doTransferIn ==> repayBorrowFresh ==> liquidateBorrowFresh   ==> liquidateBorrowInternal ==> liquidateBorrow
    #                                   ==> repayBorrowBehalfInternal  ==> repayBorrowBehalf
    #                                   ==> repayBorrowInternal ==> repayBorrow
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves

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

    # doTransferOut ==> redeemFresh ==> redeemInternal  ==> redeem
    #                               ==> redeemUnderlyingInternal  ==> redeemUnderlying
    #               ==> borrowFresh ==> borrowInternal ==> borrow
    #               ==> _reduceReservesFresh ==> _reduceReserves
    
    
    
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    # print(accessList)
    for access in accessList:
        print(access)

    # contract = contractAddress
    # tx = HackTx
    # writeDataSource(contract, tx, dataSourceMapList)
    # writeAccessList(contract, tx, accessList)
    # writeSplitedTraceTree(contract, tx, splitedTraceTree)
    # time.sleep(5)

def testCreamFi1_2():
    changeLoggingUpperBound(4)
    contractAddress = '0xd06527d5e56a3495252a528c4987003b712860ee'
    HackTx = "0x0016745693d68d734faa408b94cdf2d6c95f511b50f47b03909dc599c1dd9ff6"
    HackTx = "0xf5922ee0dd107c38285a0e593ba80027e0ee5e3618be8e7dff42fcb94b251622"
    HackTx = "0x9f2c7e92aa3c99e7f0b5098302450be4b5a219e23657a393db3ea98c9f59ab48"
    HackTx = "0x20507b57f480e4140548ff0039928dd903e6e9043d2a59f6859e79b0771e5f1b"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    l1 = [
            locator("liquidateBorrow", SELFCALLVALUE),
            locator("repayBorrowBehalf", SELFCALLVALUE),
            locator("repayBorrow", SELFCALLVALUE),
            locator("mint", SELFCALLVALUE),
            locator("_addReserves", SELFCALLVALUE)
    ]
    # doTransferIn ==> repayBorrowFresh ==> liquidateBorrowFresh   ==> liquidateBorrowInternal ==> liquidateBorrow
    #                                   ==> repayBorrowBehalfInternal  ==> repayBorrowBehalf
    #                                   ==> repayBorrowInternal ==> repayBorrow
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves

    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
            locator("_reduceReserves", FALLBACK),
            locator("redeemUnderlying", FALLBACK),
            locator("borrow", FALLBACK),
            locator("_reduceReserves", FALLBACK)
    ]

    # doTransferOut ==> redeemFresh ==> redeemInternal  ==> redeem
    #                               ==> redeemUnderlyingInternal  ==> redeemUnderlying
    #               ==> borrowFresh ==> borrowInternal ==> borrow
    #               ==> _reduceReservesFresh ==> _reduceReserves
    
    
    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    # print(accessList)
    # for traceTree in splitedTraceTree:
    #     print(traceTree)
    # contract = contractAddress
    # tx = HackTx
    # writeDataSource(contract, tx, dataSourceMapList)
    # writeAccessList(contract, tx, accessList)
    # writeSplitedTraceTree(contract, tx, splitedTraceTree)
    # time.sleep(5)



def testIndexedFi():
    changeLoggingUpperBound(5)
    contractAddress = '0x5bd628141c62a901e0a83e630ce5fafa95bbdee4'  # indexPool
    HackTx = "0x44aad3b853866468161735496a5d9cc961ce5aa872924c5d78673076b1cd95aa"
    HackTx = "0xd465036a50c2dd6ae6f6e66ce1b07321e8a6530b899c1e9d58d02c6158a7554a"
    HackTx = "0xa7ce9fb03a6427f048eae0642f58de96b17599ac86a875345a830aec74403860"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
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
    # transferFrom ==> _pullUnderlying ==> initialize (OnlyOwner)
    #                                  ==> joinPool 
    #                                  ==> joinswapExternAmountIn
    #                                  ==> joinswapPoolAmountOut
    #                                  ==> swapExactAmountIn
    #                                  ==> swapExactAmountOut

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
    # transfer ==> _pushUnderlying ==> exitPool
    #                              ==> exitswapPoolAmountIn
    #                              ==> exitswapExternAmountOut
    #                              ==> gulp
    #                              ==> swapExactAmountIn
    #                              ==> swapExactAmountOut
    #                              ==> _unbind ==> _decreaseDenorm ==> exitswapPoolAmountIn (dup)
    #                                                              ==> exitswapExternAmountOut (dup)
    #                                                              ==> swapExactAmountIn (dup)
    #                                                              ==> swapExactAmountOut (dup)

    
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testCreamFi2_1():  # crUSDC Token
    changeLoggingUpperBound(10)
    contractAddress = '0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322'
    HackTx = "0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92"
    HackTx = "0x75684209d453e842d0535a3e5759347f807495c85329c59bc0fbd495fffe030b"
    HackTx = "0x62a54bd1b8fddebffe2df0899e17481cf716ae2a1c6cdcec9d106d143b13b652"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

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
    # doTransferIn ==> repayBorrowFresh ==> liquidateBorrowFresh   ==> liquidateBorrowInternal ==> liquidateBorrow
    #                                   ==> repayBorrowBehalfInternal  ==> repayBorrowBehalf
    #                                   ==> repayBorrowInternal ==> repayBorrow
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves

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

    # doTransferOut ==> redeemFresh ==> redeemInternal  ==> redeem
    #                               ==> redeemUnderlyingInternal  ==> redeemUnderlying
    #               ==> borrowFresh ==> borrowInternal ==> borrow
    #               ==> _reduceReservesFresh ==> _reduceReserves

    
    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    # printdataSourceMapList(dataSourceMapList)
    # print(accessList)
    # for traceTree in splitedTraceTree:
    #     print(traceTree)
    
    # contract = contractAddress
    # tx = HackTx
    # writeDataSource(contract, tx, dataSourceMapList)
    # writeAccessList(contract, tx, accessList)
    # writeSplitedTraceTree(contract, tx, splitedTraceTree)
    # time.sleep(5)


def testCreamFi2_2():  # crUSDT Token
    changeLoggingUpperBound(10)
    contractAddress = '0x797aab1ce7c01eb727ab980762ba88e7133d2157'
    HackTx = "0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

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
    # doTransferIn ==> repayBorrowFresh ==> liquidateBorrowFresh   ==> liquidateBorrowInternal ==> liquidateBorrow
    #                                   ==> repayBorrowBehalfInternal  ==> repayBorrowBehalf
    #                                   ==> repayBorrowInternal ==> repayBorrow
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves

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

    # doTransferOut ==> redeemFresh ==> redeemInternal  ==> redeem
    #                               ==> redeemUnderlyingInternal  ==> redeemUnderlying
    #               ==> borrowFresh ==> borrowInternal ==> borrow
    #               ==> _reduceReservesFresh ==> _reduceReserves

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(5)


def testCreamFi2_3():  # crUNI Token
    changeLoggingUpperBound(10)
    contractAddress = '0xe89a6d0509faf730bd707bf868d9a2a744a363c7'
    HackTx = "0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92"
    # HackTx = "0xdf6067bf5cf848a481c87e14ec8d00e18f34ab85c35717984e7860acd14556cb"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

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
    # doTransferIn ==> repayBorrowFresh ==> liquidateBorrowFresh   ==> liquidateBorrowInternal ==> liquidateBorrow
    #                                   ==> repayBorrowBehalfInternal  ==> repayBorrowBehalf
    #                                   ==> repayBorrowInternal ==> repayBorrow
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves

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

    # doTransferOut ==> redeemFresh ==> redeemInternal  ==> redeem
    #                               ==> redeemUnderlyingInternal  ==> redeemUnderlying
    #               ==> borrowFresh ==> borrowInternal ==> borrow
    #               ==> _reduceReservesFresh ==> _reduceReserves

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(5)



def testCreamFi2_4():
    changeLoggingUpperBound(10)
    contractAddress = '0x8c3b7a4320ba70f8239f83770c4015b5bc4e6f91'
    HackTx = "0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92"
    # HackTx = "0x1652b3cc52f95d6163934ac3c9c100b8ed6f0b35a0668e40ec56b49b549db753"
    # HackTx = "0x8b9c2d427136f0d34f2b1515572c8b5e458c296401b5065550eddb64fd6a40d7"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

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
    # doTransferIn ==> repayBorrowFresh ==> liquidateBorrowFresh   ==> liquidateBorrowInternal ==> liquidateBorrow
    #                                   ==> repayBorrowBehalfInternal  ==> repayBorrowBehalf
    #                                   ==> repayBorrowInternal ==> repayBorrow
    #              ==> mintFresh ==> mintInternal ==> mint
    #              ==> _addReservesFresh ==> _addReservesInternal ==> _addReserves

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

    # doTransferOut ==> redeemFresh ==> redeemInternal  ==> redeem
    #                               ==> redeemUnderlyingInternal  ==> redeemUnderlying
    #               ==> borrowFresh ==> borrowInternal ==> borrow
    #               ==> _reduceReservesFresh ==> _reduceReserves

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(5)



def testRariCapital1():
    changeLoggingUpperBound(4)
    contractAddress = '0xec260f5a7a729bb3d0c42d292de159b4cb1844a3'
    HackTx = "0x171072422efb5cd461546bfe986017d9b5aa427ff1c07ebe8acc064b13a7b7be"
    HackTx = "0xdd3a395b71babb361a3487852913ca1807b31751c21d154830fc68cdb85f03b7"
    HackTx = "0x171072422efb5cd461546bfe986017d9b5aa427ff1c07ebe8acc064b13a7b7be"
    # 0x9f7d9b952d310580a47b381e0493508a67170135f983bc8632a16fe994ebb25a
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)

    # deposit locator
    l1 = [
        locator("deposit", SELFCALLVALUE),
        locator("depositTo", SELFCALLVALUE),
        locator("exchangeAndDeposit", SELFCALLVALUE),
        locator("withdrawAndExchange", SELFCALLVALUE),
    ]
    # msg.value ==> marketSell0xOrdersFillOrKill (onlyRebalancer)
    #           ==> fallback 
    #           _depositTo ==> deposit
    #                      ==> depositTo
    #           ==> exchangeAndDeposit
    #           ==> withdrawAndExchange

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
    # call.value ==> withdrawToManager (onlyManager)
    #            ==> marketSell0xOrdersFillOrKill (onlyRebalancer)
    #            ==> _withdrawFrom ==> withdraw
    #                              ==> withdrawFrom
    #            ==> withdrawFees (onlyRebalancer) 
    #            ==> withdrawAndExchange
    #            ==> sendValue (internal)
    #            ==> _depositTo ==> deposit
    #                           ==> depositTo


    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)
    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(5)


def testVisorFi():
    changeLoggingUpperBound(10)
    contractAddress = '0xc9f27a50f82571c1c8423a42970613b8dbda14ef'
    HackTx = ""
    HackTx = "0x6eabef1bf310a1361041d97897c192581cd9870f6a39040cd24d7de2335b4546"
    # HackTx = "0x630f07599fc8c68017fc1ed77810b4f3a16c63524f34b0c2ed0f7a763dd531ea"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
            locator("deposit", FUNCTION, funcAddress = "0xf938424f7210f31df2aee3011291b658f872e91e", \
                name="transferFrom", position=2), 
    ]
    # safeTransferFrom ==> deposit
    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
            locator("withdraw", FUNCTION, funcAddress = "0xf938424f7210f31df2aee3011291b658f872e91e", \
                name="transfer", position=1), 
    ]
    # safeTransfer ==> withdraw
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testUmbrellaNetwork():
    changeLoggingUpperBound(4)
    contractAddress = '0xb3fb1d01b07a706736ca175f827e4f56021b85de'
    HackTx = "0x33479bcfbc792aa0f8103ab0d7a3784788b5b0e1467c81ffbed1b7682660b4fa"


    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("stake", FUNCTION, funcAddress = "0xb1bbeea2da2905e6b0a30203aef55c399c53d042", \
            name="transferFrom", position=2),
    ]
    # transferFrom ==> _stake ==> stake

    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
        locator("rescueToken", FUNCTION, funcAddress = "0xb1bbeea2da2905e6b0a30203aef55c399c53d042", \
            name="transfer", position=1),
        locator("withdraw", FUNCTION, funcAddress = "0xb1bbeea2da2905e6b0a30203aef55c399c53d042", \
            name="transfer", position=1),
    ]
    # transfer ==> rescueToken 
    #          ==> _withdraw ==> withdraw

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

# use a variable to track balance
def testRevestFi():
    changeLoggingUpperBound(10)
    contractAddress = '0xa81bd16aa6f6b25e66965a2f842e9c806c0aa11f'
    HackTx = "0xe0b0c2672b760bef4e2851e91c69c8c0ad135c6987bbf1f43f5846d89e691428"

    # 0x56de8bc61346321d4f2211e3ac3c0a7f00db9b76 Rena tokens

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawToken", FUNCTION, funcAddress = "0x56de8bc61346321d4f2211e3ac3c0a7f00db9b76", \
            name="transfer", position=1),
    ]
    # safeTransfer ==> withdrawToken(onlyRevestController)(msg.sender/contract)
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)


# use a variable to track balance
def testRevestFi_interface():
    changeLoggingUpperBound(12)
    contractAddress = '0x2320a28f52334d62622cc2eafa15de55f9987ed9'
    HackTx = "0xe0b0c2672b760bef4e2851e91c69c8c0ad135c6987bbf1f43f5846d89e691428"
    HackTx = "0x2b69dbedb675fefb9d0f4a4d6b6d7e86cbf08ef9425cb7cea833c1606e6df725"
    HackTx = "0xa15a12edc9b5a2ec6bc6e95e7a4aa700759fe0fc5289f166dc3ffc262169a753"
    HackTx = "0xe0b0c2672b760bef4e2851e91c69c8c0ad135c6987bbf1f43f5846d89e691428"
    # 0x56de8bc61346321d4f2211e3ac3c0a7f00db9b76 Rena tokens

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = []
    # safeTransfer ==> withdrawToken(onlyRevestController)(msg.sender/contract)
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)



def testRoninNetwork(): # contains a bug but not related to the analysis
    changeLoggingUpperBound(4)
    contractAddress = '0x8407dc57739bcda7aa53ca6f12f82f9d51c2f21e'
    HackTx = "0xc28fad5e8d5e0ce6a2eaf67b6687be5d58113e16be590824d6cfa1a94467d0b7"
    # HackTx = "0x071fa6473569424e04f3208f3f53afd7da647d718c7aecf56baca9c1a52c5746"
    HackTx = "0x736ab4727985415fafb9c7eb3bd5f58b49a1e4c57bfedf05a6586993adf0fb92"


    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("deposit", SELFCALLVALUE), 
        locator("depositEthFor", SELFCALLVALUE),
    ]
    # msg.value ==> deposit
    #           ==> depositEthFor
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawERC20For", FALLBACK), 
        locator("withdrawTokenFor", FALLBACK),
        locator("withdrawERC20", FALLBACK),
    ]
    # transfer ==> _withdrawETHFor ==> withdrawERC20For (public) ==> withdrawTokenFor 
    #                                                                   ==> withdrawERC20
    #          ==> withdraw

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

# dataFlowInfer: error: temp=

# 302651704963099550405042 != lastBlockBalance[1]=
# 302654054963099550405042


def testBeanstalkFarms(): # 3Crv # invest is related to multi-token exchange, eg. giving 3Crv, 
                                   # get DAI, USDC, USDT
                                   # fixed: let's stick to one token
    changeLoggingUpperBound(4)
    contractAddress = '0x3a70dfa7d2262988064a2d051dd47521e43c9bdd'
    # contractAddress = "0x5f890841f657d90e081babdb532a05996af79fe6"
    HackTx = "0xcd314668aaa9bbfebaf1a0bd2b6553d01dd58899c508d4729fa7311dc5d33ad7"
    HackTx = "0xd3a684c354de5633a202351e7891e4f9b022089f2dbc066e07f171cf70246a0f"
    HackTx = "0x30fd944ddd5a68a9ab05048a243b852daf5f707e0448696b172cea89e757f4e5"  # buggy
    HackTx = "0x1b0e6c078d37ed1a6c8577757227a89cf5809295429e595bd5d633c21030e579"
    
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("exchange", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transferFrom", position=2),
        locator("exchange_underlying", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transferFrom", position=2),
        locator("add_liquidity", FUNCTION, funcAddress = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490", \
            name="transferFrom", position=2),
    ]
    # transferFrom ==> exchange
    #              ==> exchange_underlying
    #              ==> add_liquidity
    l2 = []
    # Curve(base_pool).add_liquidity ==> exchange_underlying   
    # Curve(base_pool).exchange ==> exchange_underlying
    # Curve(base_pool).remove_liquidity_one_coin ==> exchange_underlying

    # Withdraw locator
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
    # transfer ==> exchange
    #          ==> exchange_underlying
    #          ==> remove_liquidity
    #          ==> remove_liquidity_imbalance
    #          ==> remove_liquidity_one_coin
    #          ==> withdraw_admin_fees

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapListAll(dataSourceMapList)
    print(accessList)



def testBeanstalkFarms_interface(): 
    changeLoggingUpperBound(6)
    contractAddress = '0xc1e088fc1323b20bcbee9bd1b9fc9546db5624c5'
    HackTx = "0xcd314668aaa9bbfebaf1a0bd2b6553d01dd58899c508d4729fa7311dc5d33ad7"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = []

    l2 = []
    # Withdraw locator
    l3 = []

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapListAll(dataSourceMapList)
    print(accessList)



def testRariCapital2_1(): # fETH
    changeLoggingUpperBound(10)
    contractAddress = '0x26267e41ceca7c8e0f143554af707336f27fa051'
    HackTx = "0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530"
    HackTx = "0x899567ecf4125f9a69f31d9c8bd5f1855c1d3ee1e4617f072b4edfcf227dff2b"
    HackTx = "0xb69c0b3cbcbad4608048202836c3e73b1d211383ac05e41ef58f868ebd5d3328"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("mint", SELFCALLVALUE ),
        locator("repayBorrow", SELFCALLVALUE),
        locator("repayBorrowBehalf",SELFCALLVALUE ),
        locator("liquidateBorrow", SELFCALLVALUE),
        locator("fallback", SELFCALLVALUE),
        locator("repayBehalfExplicit", SELFCALLVALUE),
    ]
    # msg.value ==> mint 
    #           ==> repayBorrow
    #           ==> repayBorrowBehalf
    #           ==> liquidateBorrow
    #           ==> fallback
    #           ==> repayBehalfExplicit
    # doTransferIn ==> mintFresh ==> mintInternal ==> mint
    #                                             ==> fallback
    #              ==> repayBorrowFresh ==> repayBorrowInternal ==> repayBorrow
    #                                   ==> repayBorrowBehalfInternal ==> repayBorrowBehalf
    #                                   ==> liquidateBorrowFresh ==> liquidateBorrowInternal ==> liquidateBorrow

    # invest locator
    l2 = []

    # Withdraw locator
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
    # transfer ==> doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                                            ==> redeemUnderlyingInternal ==> redeemUnderlying
    #                            ==> borrowFresh ==> borrowInternal ==> borrow
    #                            ==> _reduceReservesFresh ==> _reduceReserves(external)
    #                            ==> _withdrawFuseFeesFresh ==> _withdrawFuseFees
    #                            ==> _withdrawAdminFeesFresh ==> _withdrawAdminFees
    #          ==> repayBehalfExplicit(external) ==> repayBehalf

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    for access in accessList:
        if "name" not in access:
            print(access)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(5)



def testRariCapital2_2(): 
    changeLoggingUpperBound(10)
    
    
    contractAddress = '0xebe0d1cb6a0b8569929e062d67bfbc07608f0a47'
    HackTx = "0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530"
    HackTx = "0xb30e6f9c94e215fbaadb272eb92f23c41f86b3fbc824d773da09427aff48eadb"
    HackTx = "0x21bf31ed1088145a196190cc4a442dae08792530a57e2eb08dadf1aa9056c38e"
    
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # Deposit locator
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
    # doTransferIn ==> mintFresh ==> mintInternal ==> mint
    #              ==> repayBorrowFresh ==> repayBorrowInternal ==> repayBorrow
    #                                   ==> repayBorrowBehalfInternal ==> repayBorrowBehalf
    #                                   ==> liquidateBorrowFresh ==> liquidateBorrowInternal ==> liquidateBorrow

    # invest locator
    l2 = []

    # withdraw locator
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
    #  doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                                ==> redeemUnderlyingInternal ==> redeemUnderlying
    #                ==> borrowFresh ==> borrowInternal ==> borrow
    #                ==> _reduceReservesFresh ==> _reduceReserves
    #                ==> _withdrawFuseFeesFresh ==> _withdrawFuseFees
    #                ==> _withdrawAdminFeesFresh ==> _withdrawAdminFees


    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    for access in accessList:
        if "name" not in access:
            print(access)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(5)

def testRariCapital2_3():
    changeLoggingUpperBound(10)
    contractAddress = '0xe097783483d1b7527152ef8b150b99b9b2700c8d'
    HackTx = "0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530"


    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
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
    # doTransferIn ==> mintFresh ==> mintInternal ==> mint
    #              ==> repayBorrowFresh ==> repayBorrowInternal ==> repayBorrow
    #                                   ==> repayBorrowBehalfInternal ==> repayBorrowBehalf
    #                                   ==> liquidateBorrowFresh ==> liquidateBorrowInternal ==> liquidateBorrow
    # invest locator
    l2 = []

    # Withdraw locator
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
    #  doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                                ==> redeemUnderlyingInternal ==> redeemUnderlying
    #                ==> borrowFresh ==> borrowInternal ==> borrow
    #                ==> _reduceReservesFresh ==> _reduceReserves
    #                ==> _withdrawFuseFeesFresh ==> _withdrawFuseFees
    #                ==> _withdrawAdminFeesFresh ==> _withdrawAdminFees

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testRariCapital2_4(): # frax  # TODO
    changeLoggingUpperBound(10)
    contractAddress = '0x8922c1147e141c055fddfc0ed5a119f3378c8ef8'
    HackTx = "0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530"

    HackTx = "0x4843f7e6bbdd6026713a35686bcaa0feb0723615b67d9f178e0484562cc482ea"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
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

    # invest locator
    l2 = []

    # Withdraw locator
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
    #  doTransferOut ==> redeemFresh ==> redeemInternal ==> redeem
    #                                ==> redeemUnderlyingInternal ==> redeemUnderlying
    #                ==> borrowFresh ==> borrowInternal ==> borrow
    #                ==> _reduceReservesFresh ==> _reduceReserves
    #                ==> _withdrawFuseFeesFresh ==> _withdrawFuseFees
    #                ==> _withdrawAdminFeesFresh ==> _withdrawAdminFees


    dataSourceMapList, accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)



def testSaddleFi(): #DAI
    changeLoggingUpperBound(5)
    contractAddress = '0x2069043d7556b1207a505eb459d18d908df29b55'
    HackTx = "0x2b023d65485c4bb68d781960c2196588d03b871dc9eb1c054f596b7ca6f7da56"

    HackTx = "0x8e0b0a555f2edc487ab775a4e328a09315ba5b8133ffe7f2c4e9d19a89d4c04d"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("swap", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
        locator("addLiquidity", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transferFrom", position=2),
    ]
    # safeTransferFrom ==> swap
    #              ==> addLiquidity
    
    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
        locator("swap", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("removeLiquidity", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("removeLiquidityOneToken", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("removeLiquidityImbalance", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("withdrawAdminFees", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
    ]
    # safeTransfer ==> swap
    #              ==> removeLiquidity
    #              ==> removeLiquidityOneToken
    #              ==> removeLiquidityImbalance
    #              ==> withdrawAdminFees
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testHarmonyBridge():
    changeLoggingUpperBound(4)
    contractAddress = '0xf9fb1c508ff49f78b60d3a96dea99fa5d7f3a8a6'
    HackTx = "0x27981c7289c372e601c9475e5b5466310be18ed10b59d1ac840145f6e7804c97"

    HackTx = "0x70d06084ea03835cc3f51ad0899bde3cd5398ea169e6a58fb965ba7c57178320"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("lockEth", SELFCALLVALUE),
    ]
    # msg.value ==> lockEth
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("unlockEth", FALLBACK),
    ]
    # transfer ==> unlockEth
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)


# def testHarmonyBridge_interface():
#     changeLoggingUpperBound(4)
#     contractAddress = '0x715cdda5e9ad30a0ced14940f9997ee611496de6'
#     HackTx = "0x27981c7289c372e601c9475e5b5466310be18ed10b59d1ac840145f6e7804c97"

#     path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

#     # trace = readCompressedJson(path)
    
#     # deposit locator
#     l1 = [
#         locator("fallback", SELFCALLVALUE),
#     ]
#     # msg.value ==> lockEth
#     # invest locator
#     l2 = []
#     # Withdraw locator
#     l3 = []
#     # transfer ==> unlockEth
#     dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
#     printdataSourceMapList(dataSourceMapList)
#     print(accessList)



def testXCarnival():
    changeLoggingUpperBound(6)
    contractAddress = '0x5417da20ac8157dd5c07230cfc2b226fdcfc5663'
    HackTx = "0x51cbfd46f21afb44da4fa971f220bd28a14530e1d5da5009cfbdfee012e57e35"
    HackTx = "0xc9fd29b9df597763b97a1ca9c97e1a9ea72aa9c485628ba79427639dc8b7aa6e"
    HackTx = "0x1919b4af8e4599d48a60b580df9f8adc0f3803b1f45b422aaba07116a1a2bb9f"
    HackTx = "0x40c355960f415efb2daa761dabe274e9a919485c65f1ac3f41ea52be4555449b"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = [
        locator("fallback", SELFCALLVALUE),
        locator("mint", SELFCALLVALUE),
        locator("repayBorrow", SELFCALLVALUE),
        locator("repayBorrowAndClaim", SELFCALLVALUE),
        locator("liquidateBorrow", SELFCALLVALUE),
    ]
    # msg.value ==> doTransferIn ==> mintInternal ==> receive()
    #                                                 ==> mint
    #                            ==> repayBorrowInternal ==> repayBorrow
    #                                                    ==> repayBorrowAndClaimInternal ==> repayBorrowAndClaim
    #                                                    ==> liquidateBorrowInternal ==> liquidateBorrow
    #           ==> mintInternal ==> receive()
    #                            ==> mint


    # invest locator
    l2 = []

    # Withdraw locator
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
    # doTransferOut ==> redeemInternal ==> redeem
    #                                  ==> redeemUnderlying
    #               ==> borrowInternal ==> borrow
    #               ==> reduceReserves
    # doTransferIn ==> mintInternal ==> receive()
    #                               ==> mint
    #              ==> repayBorrowInternal ==> repayBorrow
    #                                      ==> repayBorrowAndClaimInternal ==> repayBorrowAndClaim
    #                                      ==> liquidateBorrowInternal ==> liquidateBorrow
    # sendValue ==> None
    # functionCallWithValue ==> functionCall ==> None
    # _functionCallWithValue ==> functionCall ==> None

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    for access in accessList:
        if "name" not in access:
            print(access)

    contract = contractAddress
    tx = HackTx
    writeDataSource(contract, tx, dataSourceMapList)
    writeAccessList(contract, tx, accessList)
    writeSplitedTraceTree(contract, tx, splitedTraceTree)
    time.sleep(5)



def testPickleFi(): 
    changeLoggingUpperBound(4)
    contractAddress = '0x6847259b2B3A4c17e7c43C54409810aF48bA5210'
    HackTx = "0xe72d4e7ba9b5af0cf2a8cfb1e30fd9f388df0ab3da79790be842bfbed11087b0"


    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
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
    # transferFrom ==> swapExactJarForJar
    #              ==> deposit ==> depositAll
    #                          ==> _distributePerformanceFeesAndDeposit ==> harvest
    #                          ==> leverageUntil
    #              ==> convertWETHPair
    #              ==> stake
    #              ==> convert

    # invest locator
    l2 = []

    # Withdraw locator
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
        locator("test_jar_converter_curve_uni_2_3", FUNCTION, funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
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
    # transfer ==> earn(public) ==> yearn
    #          ==> inCaseTokensGetStuck
    #          ==> yearn
    #          ==> swapExactJarForJar
    #          ==> convert
    #          ==> harvest
    #          ==> withdraw
    #          ==> claimRewards
    #          ==> test_staking

    # approve ==> _test_curve_curve ==> test_jar_converter_curve_curve_0
    #                               ==> test_jar_converter_curve_curve_1
    #                               ==> test_jar_converter_curve_curve_2
    #                               ==> test_jar_converter_curve_curve_3
    #                               ==> test_jar_converter_curve_curve_4
    #         ==> _test_curve_uni_swap ==> test_jar_converter_curve_uni_0_0
    #                                  ==> test_jar_converter_curve_uni_0_1
    #                                  ==> test_jar_converter_curve_uni_0_2
    #                                  ==> test_jar_converter_curve_uni_0_3
    #                                  ==> test_jar_converter_curve_uni_1_0
    #                                  ==> test_jar_converter_curve_uni_1_1
    #                                  ==> test_jar_converter_curve_uni_1_2
    #                                  ==> test_jar_converter_curve_uni_1_3
    #                                  ==> test_jar_converter_curve_uni_2_3

    #         ==>  _test_uni_curve_swap ==> test_jar_converter_uni_curve_0_0
    #                                  ==> test_jar_converter_uni_curve_1_0
    #                                  ==> test_jar_converter_uni_curve_2_0
    #                                  ==> test_jar_converter_uni_curve_3_0
    #                                  ==> test_jar_converter_uni_curve_0_1
    #                                  ==> test_jar_converter_uni_curve_1_1
    #                                  ==> test_jar_converter_uni_curve_2_1
    #                                  ==> test_jar_converter_uni_curve_3_1
    #                                  ==> test_jar_converter_uni_curve_4_1
    #                                  ==> test_jar_converter_uni_curve_0_2
    #                                  ==> test_jar_converter_uni_curve_1_2
    #                                  ==> test_jar_converter_uni_curve_2_2
    #                                  ==> test_jar_converter_uni_curve_3_2

    #         ==> _test_uni_uni ==> test_jar_converter_uni_uni_0
    #                          ==> test_jar_converter_uni_uni_1
    #                          ==> test_jar_converter_uni_uni_2
    #                          ==> test_jar_converter_uni_uni_3


    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testDODO(): # todo
    changeLoggingUpperBound(6)
    contractAddress = '0x051ebd717311350f1684f89335bed4abd083a2b6'
    HackTx = "0x395675b56370a9f5fe8b32badfa80043f5291443bd6c8273900476880fb5221e"
    # HackTx = "0x30f34f373294df77e5009c9555d2f5802179b269c941c59dab7b952a16d53c6d"
    # HackTx = "0x8bd252077927128d96793badb806c5a6a0e9c62bdca35fd5dc7707446fc8aec7"

    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)

    # trace = readCompressedJson(path)
    
    # deposit locator
    l1 = []
    # balanceOf() ==> buyShares

    # invest locator
    l2 = []

    # Withdraw locator
    l3 = [
        locator("sellQuote", FUNCTION, fromAddr = "0x2bbd66fc4898242bdbd2583bbe1d76e8b8f71445", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("flashLoan", FUNCTION, fromAddr = "0x2bbd66fc4898242bdbd2583bbe1d76e8b8f71445", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("sellShares", FUNCTION, fromAddr = "0x2bbd66fc4898242bdbd2583bbe1d76e8b8f71445", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
    ]
    # _transferBaseOut ==> sellQuote
    #                  ==> flashLoan
    #                  ==> sellShares

    # _transferQuoteOut ==> sellBase
    #                   ==> flashLoan
    #                   ==> sellShares
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)


def testNomad(): # wbtc
    changeLoggingUpperBound(4)
    contractAddress = '0x88a69b4e698a4b090df6cf5bd7b2d47325ad30a3'
    # implementation: 0x15fda9f60310d09fea54e3c99d1197dff5107248
    HackTx = "0xa5fe9d044e4f3e5aa5bc4c0709333cd2190cba0f4e7f16bcf73f49f83e4a5460"
    HackTx = "0xed0552ce892bd0b12c24c4a4025340287a41e07c5747ffc6f998f15a62552132"
    HackTx = "0xf1ae97f1e0eba570a4e978235ca156dd626cf2ab674a8456294ad9b369bdc3a7"
    HackTx = "0xd95176fbf31792c42f91587249d43ad47a204be35567ebb9ed7b7d5bd3056593"
    HackTx = "0x3778aecf153e3437d5b3942780ce0f5848d1dc1dfc4581adf8d0c6512e16e275"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = [
        locator("send", FUNCTION, fromAddr = "0x15fda9f60310d09fea54e3c99d1197dff5107248", funcAddress = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", \
            name="transferFrom", position=2),
    ]
    # safeTransferFrom ==> send
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("handle", FUNCTION, fromAddr = "0x15fda9f60310d09fea54e3c99d1197dff5107248", funcAddress = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", \
            name="transfer", position=1),
    ]
    # safeTransfer ==> _handleTransfer ==> handle
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)


def testPolyNetwork(): #  Ether
    changeLoggingUpperBound(4)
    contractAddress = '0x250e76987d838a75310c34bf422ea9f1ac4cc906'
    HackTx = "0xad7a2c70c958fcd3effbf374d0acf3774a9257577625ae4c838e24b0de17602a"
    HackTx = "0x9cb1b4376e99eb3e7af7f465e3cf5b53788c969801407bffad2ff5ab0a45be3b"
    HackTx = "0xd89fbddee2e3971d0e25ad9907987b8994e4e37edcd53f687f1a0490b1b65297"
    HackTx = "0x911c32767fabb090813d9661803d508e05a4edef562704679cb351f65b81ada1"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = [
        locator("lock", SELFCALLVALUE),
    ]
    # msg.value ==> _transferToContract ==> lock
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("unlock", FALLBACK, fromAddr = "0x250e76987d838a75310c34bf422ea9f1ac4cc906"),
    ]
    # transfer ==> _transferFromContract ==> unlock
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testPunk_1(): # Punk USDC Initialize
    changeLoggingUpperBound(4)
    contractAddress = '0x3BC6aA2D25313ad794b2D67f83f21D341cc3f5fb'
    HackTx = "0x597d11c05563611cb4ad4ed4c57ca53bbe3b7d3fefc37d1ef0724ad58904742b"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawTo", FUNCTION, fromAddr = "0x3bc6aa2d25313ad794b2d67f83f21d341cc3f5fb", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
        locator("withdrawToForge", FUNCTION, fromAddr = "0x3bc6aa2d25313ad794b2d67f83f21d341cc3f5fb", funcAddress = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", \
            name="transfer", position=1),
    ]
    #  safeTransfer ==> withdrawTo ==> withdrawToForge

    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testPunk_2(): # Punk USDT
    changeLoggingUpperBound(4)
    contractAddress = '0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D'
    HackTx = "0x597d11c05563611cb4ad4ed4c57ca53bbe3b7d3fefc37d1ef0724ad58904742b"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawTo", FUNCTION, fromAddr = "0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
        locator("withdrawToForge", FUNCTION, fromAddr = "0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D", funcAddress = "0xdac17f958d2ee523a2206206994597c13d831ec7", \
            name="transfer", position=1),
    ]
    #  safeTransfer ==> withdrawTo ==> withdrawToForge
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)

def testPunk_3(): # Punk DAI
    changeLoggingUpperBound(4)
    contractAddress = '0x929cb86046E421abF7e1e02dE7836742654D49d6'
    HackTx = "0x597d11c05563611cb4ad4ed4c57ca53bbe3b7d3fefc37d1ef0724ad58904742b"
    path = SCRIPT_DIR + "/../Benchmarks_Traces/DeFiHackLabs/Txs/{}/{}.json.gz".format(contractAddress, HackTx)
    # trace = readCompressedJson(path)
    # deposit locator
    l1 = []
    # invest locator
    l2 = []
    # Withdraw locator
    l3 = [
        locator("withdrawTo", FUNCTION, fromAddr = "0x929cb86046E421abF7e1e02dE7836742654D49d6", funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
        locator("withdrawToForge", FUNCTION, fromAddr = "0x929cb86046E421abF7e1e02dE7836742654D49d6", funcAddress = "0x6b175474e89094c44da98b954eedeac495271d0f", \
            name="transfer", position=1),
    ]
    #  safeTransfer ==> withdrawTo ==> withdrawToForge
    dataSourceMapList , accessList, splitedTraceTree = analyzeOneTx(contractAddress, HackTx, path, l1, l2, l3)
    printdataSourceMapList(dataSourceMapList)
    print(accessList)







def runAllCases():
    testOpyn()
    testCreamFi1_1()
    testCreamFi1_2()
    testIndexedFi()
    testCreamFi2_1()
    testCreamFi2_2()
    testCreamFi2_3()
    testCreamFi2_4()
    testRariCapital1()
    testVisorFi()
    testUmbrellaNetwork()
    testRevestFi()
    testRoninNetwork()
    testBeanstalkFarms()
    testRariCapital2_1()
    testRariCapital2_2()
    testRariCapital2_3()
    testRariCapital2_4()
    testSaddleFi()
    testHarmonyBridge()
    testXCarnival()
    testPickleFi()
    testDODO()
    testNomad()
    testPolyNetwork()
    testPunk_1()
    testPunk_2()
    testPunk_3()


if __name__ == "__main__":
    # runAllCases()

    # testIndexedFi()

    # testOpyn()

    # testVisorFi()

    # testCreamFi1_2()

    # testPunk_1()

    # testPunk_2()

    # testPunk_3()

    testDODO()