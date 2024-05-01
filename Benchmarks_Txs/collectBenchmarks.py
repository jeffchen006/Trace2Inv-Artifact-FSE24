import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from crawlPackage.crawl import Crawler
import time


def collectBlockSecBlogs():
    count = 0
    contractEndblockPairs = []
    crawler = Crawler()
    with open(SCRIPT_DIR + '/MediumBlocksec/README.md', 'r') as f:
        pair = (None, None)
        for line in f:
            hash = line.strip()
            if hash.startswith('0x') and len(hash.strip()) == 42:
                pair = (hash, -1)
            if hash.startswith('0x') and len(hash.strip()) == 66:
                endBlock = crawler.Tx2Block(hash)
                count += 1
                pair = (pair[0], endBlock)
                contractEndblockPairs.append(pair)
            if hash == "None":
                pair = (None, None)
        print("In total {} contracts".format(count))

    print(contractEndblockPairs)
    for ii in range(len(contractEndblockPairs)):
        contractAddress = contractEndblockPairs[ii][0]
        endBlock = contractEndblockPairs[ii][1]
        print("=======================================")
        print("Collecting tx history for {}".format(contractAddress))
        print("=======================================")
        writeTxhistory(contractAddress, endBlock, 'MediumBlocksec')



def collectDeFiHackLabsVictim():
    count = 0
    contractEndblockPairs = []
    crawler = Crawler()
    with open(SCRIPT_DIR + '/DeFiHackLabs/README.md', 'r') as f:
        for line in f:
            hash = line.strip()
            if hash.startswith('0x') and len(hash.strip()) == 42:
                contractEndblockPairs.append((hash, -1))
                count += 1
            if hash.startswith('0x') and len(hash.strip()) == 66:
                endBlock = crawler.Tx2Block(hash)
                for ii in range(len(contractEndblockPairs)):
                    index = len(contractEndblockPairs) - 1 - ii
                    if contractEndblockPairs[index][1] == -1:
                        contractEndblockPairs[index] = (contractEndblockPairs[index][0], endBlock)
                    else:
                        break
        print("In total {} contracts".format(count))
    # print(contractEndblockPairs)
    for ii in range(len(contractEndblockPairs)):
        contractAddress = contractEndblockPairs[ii][0]
        endBlock = contractEndblockPairs[ii][1]
        if contractAddress.lower() != "0x88a69b4e698a4b090df6cf5bd7b2d47325ad30a3".lower():
            continue
        print("=======================================")
        print("Collecting tx history for {}".format(contractAddress))
        print("=======================================")
        writeTxhistory(contractAddress, endBlock, 'DeFiHackLabs')

# 0xec260f5a7a729bb3d0c42d292de159b4cb1844a3
# 0x2320a28f52334d62622cc2eafa15de55f9987ed9
# 0xc1e088fc1323b20bcbee9bd1b9fc9546db5624c5
# 0x715cdda5e9ad30a0ced14940f9997ee611496de6
# 0x051ebd717311350f1684f89335bed4abd083a2b6

def collectFlashLoanVictim():
    count = 0
    contractEndblockPairs = []
    crawler = Crawler()
    with open(SCRIPT_DIR + '/FlashSyn/README.md', 'r') as f:
        for line in f:
            hash = line.strip()
            if hash.startswith('0x') and len(hash.strip()) == 42:
                contractEndblockPairs.append((hash, -1))
                count += 1
            if hash.startswith('0x') and len(hash.strip()) == 66:
                endBlock = crawler.Tx2Block(hash)
                for ii in range(len(contractEndblockPairs)):
                    index = len(contractEndblockPairs) - 1 - ii
                    if contractEndblockPairs[index][1] == -1:
                        contractEndblockPairs[index] = (contractEndblockPairs[index][0], endBlock)
                    else:
                        break
        print("In total {} contracts".format(count))
    # print(contractEndblockPairs)
    for ii in range(len(contractEndblockPairs)):
        contractAddress = contractEndblockPairs[ii][0]
        endBlock = contractEndblockPairs[ii][1]
        if contractAddress.lower() != "0x13db1cb418573f4c3a2ea36486f0e421bc0d2427".lower():
            continue
        print("=======================================")
        print("Collecting tx history for {}".format(contractAddress))
        print("=======================================")
        writeTxhistory(contractAddress, endBlock, 'FlashSyn')


def collectCVEAccessControl():
    count = 0
    contractAddresses = []
    with open(SCRIPT_DIR + '/CVEAccessControl/README.md', 'r') as f:
        for line in f:
            contractAddress = line.strip()
            if contractAddress.startswith('0x') and len(contractAddress) == 42:
                contractAddresses.append(contractAddress)
                count += 1
        print("In total {} contracts".format(count))
    
    for ii in range(len(contractAddresses)):
        contractAddress = contractAddresses[ii]
        print("=======================================")
        print("Collecting tx history for {}".format(contractAddress))
        print("=======================================")
        writeTxhistory(contractAddress)


def writeTxhistory(contractAddress: str, endBlock: int = -1, folderName: str = 'CVEAccessControl'):
    crawler = Crawler()
    start = time.time()
    filePath = SCRIPT_DIR + '/../Benchmarks_Traces/{}/{}.txt'.format(folderName, contractAddress)
    print(filePath)
    txHashes = None
    if endBlock == -1:
        txHashes = crawler.Contract2TxHistory(contractAddress)
    else:
        txHashes = crawler.Contract2TxHistory(contractAddress, endBlock)
    end_time = time.time() - start

    with open(filePath, 'w') as f:
        for txHash in txHashes:
            f.write(txHash + '\n')
        f.write("In total, it takes {} seconds".format(end_time))
        sizeLimit = 100 # MB
        if os.path.getsize(filePath) >= sizeLimit * 1024 * 1024:
            print("=======================================")
            print("File size >= {}MB, please check !!!", sizeLimit)
            print("=======================================")
            return


if __name__ == '__main__':
    # collectCVEAccessControl()
    # collectFlashLoanVictim()
    # collectBlockSecBlogs()
    # collectDeFiHackLabsVictim()

    collectFlashLoanVictim()