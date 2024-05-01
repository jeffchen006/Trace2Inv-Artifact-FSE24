import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from parserPackage.parser import *


def printdataSourceMapList(dataSourceMapList):
    for item in dataSourceMapList:
        if isinstance(item, dataSource):
            print(item)
        elif isinstance(item, list):
            for i in item:
                print(i)




def printdataSourceMapListAll(dataSourceMapList):
    for item in dataSourceMapList:
        if isinstance(item, dataSource):
            print(item.to_dict())
        elif isinstance(item, list):
            printdataSourceMapListAll(item)
            # for i in item:
            #     print(i)





