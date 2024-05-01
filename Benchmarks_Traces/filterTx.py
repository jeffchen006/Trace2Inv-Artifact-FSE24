from multiprocessing.util import is_exiting
import sys
import os
from unicodedata import category

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from crawlPackage.crawl import Crawler
import time


class FilterTx:
    def __init__(self):
        pass

    def contract2Category(self, contract: str):
        """Given a victim contract, find its category"""
        category = None
        for file in os.listdir(SCRIPT_DIR):
            d = os.path.join(SCRIPT_DIR, file)
            READMEfile = SCRIPT_DIR + '/../Benchmarks_Txs/' + file + '/README.md'

            if os.path.isdir(d) and os.path.exists(READMEfile):
                with open(READMEfile, 'r') as f:
                    for line in f:
                        hash = line.strip()
                        if hash.startswith('0x') and len(hash.strip()) == 42:
                            if hash == contract:
                                category = file
                                break
        return category

    def contract2ExploitTx(self, contract: str):
        """Given a victim contract, find the exploit Tx"""
        category = self.contract2Category(contract)
        exploitTx = self.contractCategory2ExploitTx(contract, category)
        return exploitTx

    def contractCategory2ExploitTx(self, contract: str, category: str = None):
        """Given a victim contract, find the exploit Tx"""
        if category == None:
            category = self.contract2Category(contract)
        exploitTx = None
        with open(SCRIPT_DIR + '/../Benchmarks_Txs/' + category + '/README.md', 'r') as f:
            for line in f:
                hash = line.strip()
                if hash.startswith('0x') and len(hash.strip()) == 42:
                    if hash == contract:
                        exploitTx = -1
                if hash.startswith('0x') and len(hash.strip()) == 66:
                    if exploitTx == -1:
                        exploitTx = hash
                        break
        return exploitTx

    def filterCVEAccessControl(self):
        """Delete Txs which happen after the exploit Tx"""
        contractTxPairs = []
        with open(SCRIPT_DIR + '/CVEAccessControl/README.md', 'r') as f:
            for line in f:
                hash = line.strip()
                if hash.startswith('0x') and len(hash.strip()) == 42:
                    contractTxPairs.append((hash, -1))
                if hash.startswith('0x') and len(hash.strip()) == 66:
                    for ii in range(len(contractTxPairs)):
                        index = len(contractTxPairs) - 1 - ii
                        if contractTxPairs[index][1] == -1:
                            contractTxPairs[index] = (contractTxPairs[index][0], hash)
                        else:
                            break
        for contractTxPair in contractTxPairs:
            contractAddress = contractTxPair[0]
            exploitTx = contractTxPair[1]
            print("=======================================")
            print("Filtering tx history for {}".format(contractAddress))
            print("=======================================")
            self.filterTxhistory("CVEAccessControl", contractAddress, exploitTx)

    def filterTxhistory(self, category, contractAddress, exploitTx):
        """Delete Txs which happen after the exploit Tx"""
        crawler = Crawler()

        lines = None
        with open(SCRIPT_DIR + '/' + category + '/{}.txt'.format(contractAddress), "r") as f:
            lines = f.readlines()

        findExploitTx = False
        ExploitTxBlock = -1
        with open(SCRIPT_DIR + '/' + category + '/{}.txt'.format(contractAddress), 'w') as f:
            for line in lines:
                hash = line.strip()
                if hash == exploitTx:
                    findExploitTx = True
                    ExploitTxBlock = crawler.Tx2Block(hash)
                    f.write(line)
                elif findExploitTx == False:
                    f.write(line)
                else:
                    TxBlock = crawler.Tx2Block(hash)
                    if TxBlock <= ExploitTxBlock:
                        f.write(line)
                    else:
                        break

        if findExploitTx == False:
            print("Exploit Tx not found!!!!!!!")
                


if __name__ == '__main__':
    filterTx = FilterTx()
    # filterTx.filterCVEAccessControl()

    filterTx.contract2Category("0x85ca13d8496b2d22d6518faeb524911e096dd7e0")