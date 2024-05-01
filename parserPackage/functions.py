import json
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utilsPackage.compressor import writeCompressedJson, readCompressedJson



def addLeadningZeroFuncSelector(funcSelector: str) -> str:
    """Given a function selector, add leading zeros to make it 5 bytes"""
    return funcSelector[0:2] + "0" * (10 - len(funcSelector)) + funcSelector[2:]

def getTrace(jsonFile: str):
    """Given a transaction hash, return the trace"""
    content = None
    with open(jsonFile, 'r') as f:
        content = json.load(f)
    return content

def getPathFromCategoryTxHash(category: str, contract: str, txHash: str):
    """Given a category, contract and txHash, return the path"""
    path = SCRIPT_DIR + '/../Benchmarks_Traces' + '/{}/Txs/{}/{}.json.gz'.format(category, contract, txHash)
    return path

def getTraceFromCategoryTxHash(category: str, contract: str, txHash: str):
    """Given a category, contract and txHash, return the trace"""
    path = SCRIPT_DIR + '/../Benchmarks_Traces' + '/{}/Txs/{}/{}.json.gz'.format(category, contract, txHash)
    trace = readCompressedJson(path)
    return trace






