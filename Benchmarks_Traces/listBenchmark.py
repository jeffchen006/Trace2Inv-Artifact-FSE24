import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Benchmarks_Traces.filterTx import FilterTx
import random
 
def listBenchmarks():
    rootdir = SCRIPT_DIR
    benchmarkCategories = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d) and file != "__pycache__":
            benchmarkCategories.append(file)
            
    for benchmarkCategory in benchmarkCategories:
        print("=======================================")
        print("Category: {}".format(benchmarkCategory))
        print("=======================================")
        benchmarkCategoryDir = os.path.join(rootdir, benchmarkCategory)
        for file in os.listdir(benchmarkCategoryDir):
            if file.endswith(".txt"):
                lines_in_file = open(os.path.join(benchmarkCategoryDir, file), 'r').readlines()
                number_of_lines = len(lines_in_file)
                print(file[:-4], number_of_lines)

# take first element for sort
def takeFirst(elem):
    return elem[0]


def listTxDetails(contract: str, category: str = None):
    """Given a victim contract, (and a category), list all the Tx details"""
    ft = FilterTx()
    if category == None:
        category = ft.contract2Category(contract)
    exploitTx = ft.contractCategory2ExploitTx(contract, category)

    rootdir = SCRIPT_DIR
    benchmarkCategoryDir = os.path.join(rootdir, category) + "/Txs/" + contract
    txDetails = []

    if os.path.isdir(benchmarkCategoryDir):
        for file in os.listdir(benchmarkCategoryDir):
            print(file)
            if file.endswith(".json"):
                file_stats = os.stat(benchmarkCategoryDir + "/" + file)
                txDetails.append((file_stats.st_size, file[:-5]))

    txDetails.sort(key=takeFirst)
    for txDetail in txDetails:
        if txDetail[1] == exploitTx:
            print(txDetail[0], "\t", txDetail[1], "Exploit Tx!")
        else:
            print(txDetail[0], "\t", txDetail[1])





def main():
    listBenchmarks()

    # listTxDetails("0xACd43E627e64355f1861cEC6d3a6688B31a6F952")
#                                                               exploit Tx rank in size
# Eminence        0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8    1
# bZx1            0xb0200B0677dD825bb32B93d055eBb9dc3521db9D    1
# bZx2            0x77f973FCaF871459aa58cd81881Ce453759281bC    1
# CheeseBank      0x5E181bDde2fA8af7265CB3124735E9a13779c021
#                 0x4c2a8A820940003cfE4a16294B239C8C55F29695
#                 0xA80e737Ded94E8D2483ec8d2E52892D9Eb94cF1f    1
# Harvest1_fUSDT   0x053c80eA73Dc6941F518a68E2FC52Ac45BDE7c9C
# Harvest2_fUSDC   0xf0358e8c3CD5Fa238a29301d0bEa3D63A17bEdBE
# InverseFi       0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670
# ValueDeFi       0x55BF8304C78Ba6fe47fd251F37d7beb485f86d26    1
# Warp            0xBa539B9a5C2d412Cb10e5770435f362094f9541c    1
# Yearn           0xACd43E627e64355f1861cEC6d3a6688B31a6F952




if __name__ == '__main__':
    main()


