import sys
import os
import gzip

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# print(SCRIPT_DIR)

from crawlPackage.crawl import Crawler
from fetchPackage.fetchTrace import fetcher
from utilsPackage.compressor import *

import multiprocessing
import time
import json



def file2Txlist(fileName: str):
    txlist = []
    with open(fileName, 'r') as f:
        for line in f:
            Tx = line.strip()
            if Tx.startswith('0x') and len(Tx) == 66:
                txlist.append(Tx)
    return txlist


def checkFileSize(logPath: str, sizeLimit = 100):
    """Given a log path, check if the file size is larger than the size limit(MB)"""
    fileSize = os.path.getsize(logPath) / 1024 / 1024
    if fileSize >= sizeLimit * 1024 * 1024:
        print("=======================================")
        print("File size >= {}MB, please check !!!", sizeLimit)
        print("=======================================")
        return
    else:
        print("File size: {}MB".format(fileSize))
        pass


def categoryContract2File(category: str, contract: str):
    # start = time.time()
    path = SCRIPT_DIR + '/{}/Txs/{}'.format(category, contract)
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    filePath = SCRIPT_DIR + '/{}/{}.txt'.format(category, contract)

    # filePath = SCRIPT_DIR + "/../constraintPackage/ReFetchedTxs/{}.pickle".format(contract.lower())
    txList = file2Txlist(filePath)
    # txList = readList(filePath)[0]
    # if contract == "0x8407dc57739bcda7aa53ca6f12f82f9d51c2f21e":
    #     txList = txList[-100000:]

    fe = fetcher()

    NumOfProcesses = 1
    processes = []
    processStats = []
    # An entry in processStats is a list of [Tx, Index, start time]
    for _ in range(NumOfProcesses):
        processStats.append(0)

    ProcessesRunning = 0

    for ii in range(len(txList)):
        # if ii < len(txList) - 1:
        #     continue
        # if ii < 400:
        #     continue
        Tx = txList[ii]
        logPath = SCRIPT_DIR + '/{}/Txs/{}/{}.json.gz'.format(category, contract, Tx)

        # # if Tx != "0x7903e4d558c81c457f96c754fc8c23bc105c46b281a9ea80d15ab1d4945d4fc2":
        if os.path.exists(logPath) and os.path.getsize(logPath) > 0:
            print("Trace exists for {}(progress: {}/{})".format(Tx, ii + 1, len(txList)))
            continue

        if Tx == "0x52a0541deff2373e1098881998b60af4175d75c410d67c86fcee850b23e61fc2" or \
            Tx == "0xca13006944e6eba2ccee0b2d96a131204491641014622ef2a3df3db3e6939062" or \
            Tx == "0xc8d138a6190459db20542a6ddec692cbf176c9825bdccd79f06d65c9c3509a86" or \
            Tx == "0xdfe08f532df2cc89707a65400e65edc9b9d108de02875b8043f845915ab884fe" or \
            Tx == "0x43921dc3d070263678d84abb262d0eedb06d38fed840d6308f228a03610c312d" or \
            Tx == "0xc651aeeaea2a25cc530dbeaecded933572af070565be911e3b624097faecd2df" or \
            Tx == "0xed7efd5bf771ae1e115fb59b9f080c2f66d74bf3c9234a89acb0e91e48181aec":
            # this tx trace is too big
            continue

        if ProcessesRunning < NumOfProcesses:
            p = multiprocessing.Process(target=fe.storeTrace, args=(category, contract, Tx, False))
            p.start()
            processes.append(p)
            processStats[ProcessesRunning] = [Tx, ii, time.time()]
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
                        logPath = SCRIPT_DIR + '/{}/Txs/{}/{}.json.gz'.format(category, contract, processStats[jj][0])
                        print("Process {} finished for {}(progress: {}/{}), takes time {} s".format(jj, processStats[jj][0], processStats[jj][1], len(txList), time.time() - processStats[jj][2]))
                        checkFileSize(logPath)
                        p = multiprocessing.Process(target=fe.storeTrace, args=(category, contract, Tx, False))
                        p.start()
                        processes[jj] = p
                        processStats[jj] = [Tx, ii, time.time()]
                        ifbreak = True
                        time.sleep(0.05)
                        break
                if ifbreak:
                    break
                # sleep 100 ms
                time.sleep(0.1)

        # print("Trace fetch started for {}(progress: {}/{})".format(Tx, ii, len(txList)))

    




    # temp = []
    # batchsize = 100 # Batch Size
    # for ii in range(len(txList)):
    #     if len(temp) == batchsize or ii == len(txList) - 1:

    #         # traces = fe.batch_getTrace(temp)
    #         # for jj in range(len(temp)):
    #         #     trace = traces[jj]
    #         #     tx = temp[jj]
    #         #     logPath = SCRIPT_DIR + '/{}/Txs/{}/{}.json.gz'.format(category, contract, tx)
    #         #     writeCompressedJson(logPath, trace)
    #         #     checkFileSize(logPath)
    #         fe.batch_storeTrace2(category=category, contract=contract, Txs=temp)   # 2 is faster
    #         temp = []
    #         print("Batch Fetching Done")
    #     Tx = txList[ii]
    #     logPath = SCRIPT_DIR + '/{}/Txs/{}/{}.json.gz'.format(category, contract, Tx)
    #     if os.path.exists(logPath) and os.path.getsize(logPath) > 0:
    #         print("Trace exists for {}(progress: {}/{})".format(Tx, ii, len(txList)))
    #         continue
    #     temp.append(Tx)
    #     print("Collecting trace for {}(progress: {}/{})".format(Tx[: 7], ii, len(txList)))
    # end = time.time()
    # print("=======================================")
    # print("Total time: {}s".format(end - start))
    # print("=======================================")


def main():

# progress: bZx2, creamFi2_4, Harvest2_fUSDC, Harvest1_fUSDT, creamFi1, XCarnival, 
#        RariCapital2_1, RariCapital2_2, RariCapital2_3, RariCapital2_4

#        Eminence
# doing: ,  value deFi, warp, CheeseBank_1, CheeseBank_2, CheeseBank_3, inverseFi, yearn
#        Opyn, RariCapital1, index fi, Visor Fi, Pickle Fi, DODO, Umbrella, Revest, Ronin Network
#        Beanstalk, SaddleFi, Harmony Bridge, Harmony Bridge Interface, Punk_1, Punk_2, Punk_3
#        Nomad bridge, Poly Network, 
#        
# todebug: creamFi2_1, creamFi2_2, creamFi2_3, 

# One token, yield-earning protocols:
    # category = "FlashSyn"  # Eminence
    # contract = "0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn'  # bZx2
    # contract = "0x85ca13d8496b2d22d6518faeb524911e096dd7e0"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn' # Harvest1_fUSDT
    # contract = "0x053c80ea73dc6941f518a68e2fc52ac45bde7c9c"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn' # Harvest2_fUSDC
    # contract = "0xf0358e8c3cd5fa238a29301d0bea3d63a17bedbe"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn'  # value deFi
    # contract = "0xddd7df28b1fb668b77860b473af819b03db61101"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn' # Yearn
    # # contract = "0x9c211bfa6dc329c5e757a223fb72f5481d676dc1"
    # # categoryContract2File(category, contract)
    # contract = "0xacd43e627e64355f1861cec6d3a6688b31a6f952"
    # categoryContract2File(category, contract)


# Multiple tokens, lending protocols

    # category = 'FlashSyn'  # WarpSC
    # contract = "0x6046c3Ab74e6cE761d218B9117d5c63200f4b406"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn'  # WarpControl
    # contract = "0xba539b9a5c2d412cb10e5770435f362094f9541c"
    # categoryContract2File(category, contract)

    # 0x8f1ab46cf858b02b3eae5001ad32ecbe5b56331f8816895cc3300ea185b171cf
    
    # category = 'FlashSyn'  # cheeseBank
    # contract = "0x5E181bDde2fA8af7265CB3124735E9a13779c021"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn'  # cheeseBank
    # contract = "0x4c2a8A820940003cfE4a16294B239C8C55F29695"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn'  # cheeseBank
    # contract = "0xA80e737Ded94E8D2483ec8d2E52892D9Eb94cF1f"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn'  # inverseFi
    # contract = "0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670"
    # categoryContract2File(category, contract)

    # category = 'FlashSyn'  # Yearn1
    # contract = "0x9ca85572e6a3ebf24dedd195623f188735a5179f"
    # categoryContract2File(category, contract)




# DeFi Hack Labs
    # Opyn
    # category = 'DeFiHackLabs'
    # contract = '0x951d51baefb72319d9fbe941e1615938d89abfe2'
    # categoryContract2File(category, contract)

    # Cover Protocol  Not ready yet
    # category = 'DeFiHackLabs'
    # contract = '0xe0b94a7bb45dd905c79bb1992c9879f40f1caed5'
    # categoryContract2File(category, contract)


    # RariCapital
    # category = 'DeFiHackLabs'
    # contract = '0xec260f5a7a729bb3d0c42d292de159b4cb1844a3'
    # categoryContract2File(category, contract)

    # # Cream Finance1
    # category = 'DeFiHackLabs'
    # contract = '0x2db6c82ce72c8d7d770ba1b5f5ed0b6e075066d6'
    # categoryContract2File(category, contract)

    # contract = '0xd06527d5e56a3495252a528c4987003b712860ee'
    # categoryContract2File(category, contract)

    # indexed Finance
    # category = 'DeFiHackLabs'
    # contract = '0x5bd628141c62a901e0a83e630ce5fafa95bbdee4'
    # categoryContract2File(category, contract)

    # CreamFinance2
    # category = 'DeFiHackLabs'
    # contract = '0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322'
    # categoryContract2File(category, contract)

    # contract = '0x797aab1ce7c01eb727ab980762ba88e7133d2157'
    # categoryContract2File(category, contract)

    # contract = '0xe89a6d0509faf730bd707bf868d9a2a744a363c7'
    # categoryContract2File(category, contract)

    # contract = '0x8c3b7a4320ba70f8239f83770c4015b5bc4e6f91'
    # categoryContract2File(category, contract)


    # # Visor Finance
    # category = 'DeFiHackLabs'
    # contract = '0xc9f27a50f82571c1c8423a42970613b8dbda14ef'
    # categoryContract2File(category, contract)

    # # Pickle Finance
    # category = 'DeFiHackLabs'
    # contract = '0x6847259b2B3A4c17e7c43C54409810aF48bA5210'
    # categoryContract2File(category, contract)

    # # DODO
    # category = 'DeFiHackLabs'
    # contract = '0x2bbd66fc4898242bdbd2583bbe1d76e8b8f71445'
    # categoryContract2File(category, contract)

    # # ## ====================================== 06/30/2023 =====================================================
    # # Umbrella Network 
    # category = 'DeFiHackLabs'
    # contract = '0xb3fb1d01b07a706736ca175f827e4f56021b85de'
    # categoryContract2File(category, contract)

    # # Revest Finance
    # category = 'DeFiHackLabs'
    # contract = '0xa81bd16aa6f6b25e66965a2f842e9c806c0aa11f'
    # categoryContract2File(category, contract)

    # # Ronin Network - Bridge    3081122 txs
    # category = 'DeFiHackLabs'
    # contract = '0x8407dc57739bcda7aa53ca6f12f82f9d51c2f21e'
    # categoryContract2File(category, contract)


    # BeanstalkFarms
    # category = 'DeFiHackLabs'
    # contract = '0x3a70dfa7d2262988064a2d051dd47521e43c9bdd'
    # categoryContract2File(category, contract)

    # BeanstalkFarms_interface
    # category = 'DeFiHackLabs'
    # contract = '0xc1e088fc1323b20bcbee9bd1b9fc9546db5624c5'
    # categoryContract2File(category, contract)

    # # Cover Protocol
    # category = 'DeFiHackLabs'
    # contract = "0xe0b94a7bb45dd905c79bb1992c9879f40f1caed5"
    # categoryContract2File(category, contract)

    # # Rari Capital
    # category = 'DeFiHackLabs'
    # contract = '0x26267e41ceca7c8e0f143554af707336f27fa051'
    # categoryContract2File(category, contract)

    # contract = '0xebe0d1cb6a0b8569929e062d67bfbc07608f0a47'
    # categoryContract2File(category, contract)

    # contract = '0xe097783483d1b7527152ef8b150b99b9b2700c8d'
    # categoryContract2File(category, contract)

    # contract = '0x8922c1147e141c055fddfc0ed5a119f3378c8ef8'
    # categoryContract2File(category, contract)

    # # Saddle Finance
    # category = 'DeFiHackLabs'
    # contract = '0x2069043d7556b1207a505eb459d18d908df29b55'
    # categoryContract2File(category, contract)

    # # Harmony's Horizon Bridge
    # category = 'DeFiHackLabs'
    # contract = '0xf9fb1c508ff49f78b60d3a96dea99fa5d7f3a8a6'
    # categoryContract2File(category, contract)

    # # interface
    # contract = '0x715cdda5e9ad30a0ced14940f9997ee611496de6'
    # categoryContract2File(category, contract)

    # XCarnival
    # category = 'DeFiHackLabs'
    # contract = '0x5417da20ac8157dd5c07230cfc2b226fdcfc5663'
    # categoryContract2File(category, contract)


    # # BuildFinance
    # category = 'DeFiHackLabs'
    # contract = '0x6e36556b3ee5aa28def2a8ec3dae30ec2b208739'
    # categoryContract2File(category, contract)

    # # Bacon Protocol
    # category = 'DeFiHackLabs'
    # contract = '0xb8919522331c59f5c16bdfaa6a121a6e03a91f62'
    # categoryContract2File(category, contract)

    # # Punk Protocol Punk USDT:
    # category = 'DeFiHackLabs'
    # contract = "0x1F3b04c8c96A31C7920372FFa95371C80A4bfb0D"
    # categoryContract2File(category, contract)

    # # Punk Protocol Punk USDC:
    # category = 'DeFiHackLabs'
    # contract = "0x3BC6aA2D25313ad794b2D67f83f21D341cc3f5fb"
    # categoryContract2File(category, contract)

    # # Punk Protocol Punk DAI:
    # category = 'DeFiHackLabs'
    # contract = "0x929cb86046E421abF7e1e02dE7836742654D49d6"
    # categoryContract2File(category, contract)


    # # Nomad bridge Date: Aug 1, 2022
    # category = 'DeFiHackLabs'
    # contract = "0x88a69b4e698a4b090df6cf5bd7b2d47325ad30a3"
    # categoryContract2File(category, contract)

    # # Poly Network
    # category = 'DeFiHackLabs'
    # contract = "0x250e76987d838a75310c34bf422ea9f1ac4cc906"
    # categoryContract2File(category, contract)


# ========================== user interface ==========================
    # category = 'DeFiHackLabs'
    # contract = "0xec260f5a7a729bb3d0c42d292de159b4cb1844a3"
    # categoryContract2File(category, contract)


    # category = 'DeFiHackLabs'
    # contract = "0x2320a28f52334d62622cc2eafa15de55f9987ed9"
    # categoryContract2File(category, contract)


    # category = 'DeFiHackLabs'
    # contract = "0xc1e088fc1323b20bcbee9bd1b9fc9546db5624c5"
    # categoryContract2File(category, contract)


    # category = 'DeFiHackLabs'
    # contract = "0x715cdda5e9ad30a0ced14940f9997ee611496de6"
    # categoryContract2File(category, contract)


    # category = 'DeFiHackLabs'
    # contract = "0x051ebd717311350f1684f89335bed4abd083a2b6"
    # categoryContract2File(category, contract)



# After FSE submission:
    category = 'FlashSyn'
    contract = "0x13db1cb418573f4c3a2ea36486f0e421bc0d2427"
    categoryContract2File(category, contract)




# No source code for the border contracts. Give up:

    # category = 'FlashSyn'  # bZx1
    # contract = "0xb0200B0677dD825bb32B93d055eBb9dc3521db9D"
    # categoryContract2File(category, contract)

#  dropped

    # # Jan 19, 2022 Multichain Permit Attack  AnySwap  
    # category = 'DeFiHackLabs'
    # contract = "0x6b7a87899490EcE95443e979cA9485CBE7E71522"
    # categoryContract2File(category, contract)

if __name__ == "__main__":
    main()
