import sys
import os
import gzip

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# print(SCRIPT_DIR)

from crawlPackage.crawl import Crawler
from crawlPackage.crawlEtherscan import CrawlEtherscan
from fetchPackage.fetchTrace import fetcher
from parserPackage.parser import VmtraceParser
from utilsPackage.compressor import writeCompressedJson, readCompressedJson
from Benchmarks_Traces.Txlist2Trace import file2Txlist
import time
import json
import multiprocessing
from utilsPackage.compressor import *


def categoryContract2txlist(category: str, contract: str) -> list:
    filePath = SCRIPT_DIR + '/{}/{}.txt'.format(category, contract)
    txList = file2Txlist(filePath)
    return txList

def categoryContract2Paths(category: str, contract: str) -> list:
    filePath = SCRIPT_DIR + '/{}/{}.txt'.format(category, contract)
    txList = file2Txlist(filePath)
    pathList = []
    for txHash in txList:
        path = SCRIPT_DIR + '/{}/Txs/{}/{}.json.gz'.format(category, contract, txHash)
        pathList.append(path)
    return txList, pathList






def Path2Logs(txHash: str, category: str, contract: str) -> list:
    path = SCRIPT_DIR + '/{}/Txs/{}/{}.json.gz'.format(category, contract, txHash)
    trace = readCompressedJson(path)
    parser = VmtraceParser()
    logs = parser.parseLogs(contract, txHash, trace)
    return logs


tempLogPath = SCRIPT_DIR + '/temp2/'

def cookOneTx(txHash: str, category: str, contract: str):
    logPath = tempLogPath + '{}.json'.format(txHash)
    logs = Path2Logs(txHash, category, contract)

    with open(logPath, 'w') as f:
        json.dump(logs, f)


def runOneProcess(category: str, contract: str):
    txList = categoryContract2txlist(category, contract)
    start = False

    for ii in range(len(txList)):
        txHash = txList[ii]

        # check if temp.txt size is bigger than 2MB
        # if so, delete temp.txt and create a new one
        

        print("Now works on Tx number: {}".format(ii))


        print("Now works on Tx: {}".format(txHash))
        parser = VmtraceParser()
        path = SCRIPT_DIR + '/{}/Txs/{}/{}.json.gz'.format(category, contract, txHash)
        trace = readCompressedJson(path)
        logs = parser.parseLogs(contract, txHash, trace)






def run(category: str, contract: str):
    txList = categoryContract2txlist(category, contract)
    NumOfProcesses = 10
    processes = []
    ProcessesRunning = 0
    # cookOneTx(txList[59], category, contract)
    executeTxList = txList
    for ii in range(len(executeTxList)):
        txHash = executeTxList[ii]
        logPath = tempLogPath + '{}.json'.format(txHash)
        if os.path.exists(logPath):
            print("Log exists for Tx: {}(progress: {}/{})".format(txHash[:10], ii + 1, len(executeTxList)))
            continue

        if ProcessesRunning < NumOfProcesses:
            p = multiprocessing.Process(target=cookOneTx, args=(txHash, category, contract))
            p.start()
            processes.append(p)
            ProcessesRunning += 1
            time.sleep(0.01)
            if ProcessesRunning == NumOfProcesses:
                print("From now on, all processes are running")
        else:
            # spinning wait
            ifbreak = False
            while True:
                for jj in range(NumOfProcesses):
                    if not processes[jj].is_alive():
                        processes[jj].join()
                        print("Process {} finished for {}(progress: {}/{})".format(jj, txHash[:10], ii + 1, len(executeTxList)))
                        p = multiprocessing.Process(target=cookOneTx, args=(txHash, category, contract))
                        p.start()
                        processes[jj] = p
                        ifbreak = True
                        time.sleep(0.01)
                        break
                if ifbreak:
                    break
                # sleep 100 ms
    print("All processes finished")



def main():
    # category = "FlashSyn"
    # contract = "0xACd43E627e64355f1861cEC6d3a6688B31a6F952"
    # txList = categoryContract2txlist(category, contract)
    # run(category, contract)


    category = "FlashSyn"
    contract = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    txList = categoryContract2txlist(category, contract)
    # run(category, contract)

    datas = []
    hasValue = 0
    sstore = 0
    for txHash in txList:
        logPath = tempLogPath + '{}.json'.format(txHash)
        if os.path.exists(logPath) and os.path.getsize(logPath) > 0:
            data = json.load(open(logPath))
            hasSstore = False
            for ii in range(len(data)):
                for jj in range(len(data[ii])):
                    if data[ii][jj] == 'sstore':
                        hasSstore = True
                if hasSstore:
                    break
            if hasSstore:
                datas.append((txHash, data))
                sstore += 1
            # print(data)
            if data != [] and data != [[]]:
                hasValue += 1
                # print(txHash)
    # print(hasValue)
    # print(sstore)

    for data in datas:
        for ii in range(len(data[1])):
            for jj in range(len(data[1][ii])):
                if data[1][ii][jj] == '0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6':
                    data[1][ii][jj] = 'DAI'
                elif data[1][ii][jj] == '0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf7':
                    data[1][ii][jj] = 'USDC'
                elif data[1][ii][jj] == '0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf8':
                    data[1][ii][jj] = 'USDT'
    
    for data in datas:
        sloadDAI = "---------"
        sstoreDAI = "---------"
        sloadUSDC = "---------"
        sstoreUSDC = "---------"
        sloadUSDT = "---------"
        sstoreUSDT = "---------"
        for ii in range(len(data[1])):
            if data[1][ii][0] == 'sstore' and data[1][ii][1] == 'DAI':
                sstoreDAI = int(data[1][ii][2] / 10 ** 18)
            elif data[1][ii][0] == 'sload' and data[1][ii][1] == 'DAI':
                sloadDAI = int(data[1][ii][2] / 10 ** 18)
            elif data[1][ii][0] == 'sstore' and data[1][ii][1] == 'USDC':
                sstoreUSDC = int(data[1][ii][2] / 10 ** 6)
            elif data[1][ii][0] == 'sload' and data[1][ii][1] == 'USDC':
                sloadUSDC = int(data[1][ii][2] / 10 ** 6)
            elif data[1][ii][0] == 'sstore' and data[1][ii][1] == 'USDT':
                sstoreUSDT = int(data[1][ii][2] / 10 ** 6)
            elif data[1][ii][0] == 'sload' and data[1][ii][1] == 'USDT':
                sloadUSDT = int(data[1][ii][2] / 10 ** 6)
        print(data[0][:10],  sloadDAI, sstoreDAI, sloadUSDC, sstoreUSDC, sloadUSDT, sstoreUSDT)


    # Txs = []
    # with open(SCRIPT_DIR + '/record.txt') as f:
    #     for line in f:
    #         Txs.append(line.strip())
    
    # stats = []
    # for Tx in Txs:
    #     logPath = tempLogPath + '{}.json'.format(Tx)
    #     if os.path.exists(logPath) and os.path.getsize(logPath) > 0:
    #         data = json.load(open(logPath))
    #         # print(data)
    #         if data != [] and data != [[]]:
    #             for i in range(len(data)):
    #                 for j in range(len(data[i])):
    #                     if data[i][j] == "0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6":
    #                         data[i][j] = "DAI"
    #                     elif data[i][j] == "0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf7":
    #                         data[i][j] = "USDC"
    #                     elif data[i][j] == "0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf8":
    #                         data[i][j] = "USDT"
    #                     if isinstance(data[i][j], list) and len(data[i][j]) == 1:
    #                         data[i][j] = data[i][j][0]
    #             for i in range(len(data)):
    #                 stats.append((Tx, data[i]))

    # import pprint
    # # pprint.pprint(stats)
    
    # new_stats = []
    # for ii in range(len(stats)):
    #     if stats[ii][1][0] == 'sload' and stats[ii][1][1] == 'DAI' \
    #         and stats[ii][1][9] == 'sstore' and stats[ii][1][10] == 'DAI':
    #         new_stats.append((stats[ii][0], (stats[ii][1][2] // 10 ** 18, stats[ii][1][11] // 10 ** 18)))

    # etherScan = CrawlEtherscan()
    # for ii in range(len(new_stats)):
    #     TxHash = new_stats[ii][0]
    #     BlockNumber = etherScan.Tx2Block(TxHash)
    #     if ii != 0:
    #         print(BlockNumber, new_stats[ii][0][:10], new_stats[ii][1][0], new_stats[ii][1][1], new_stats[ii][1][1] - new_stats[ii][1][0], new_stats[ii][1][0] - new_stats[ii-1][1][1], sep='\t')
    # # print("In total, ", hasValue, " txs have value")
    # # DAI,
    # # USDC, 
    # # USDT

    


        
if __name__ == '__main__':
    category = "FlashSyn"
    contract = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    runOneProcess(category, contract)