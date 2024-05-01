from textwrap import indent
from web3 import Web3
import requests
import json
import toml
import sys
import pprint
import pickle
import time
import os
import random
settings = toml.load("settings.toml")

def save_object(obj, filename):
    try:
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        path = None
        if filename.startswith("0x"):
            path = SCRIPT_DIR + "/cache/" + "{}/{}.pickle".format(filename[0:3], filename)
        else:
            path = SCRIPT_DIR + "/cache/" + "{}.pickle".format(filename)
        with open(path, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
 

def load_object(filename):
    try:
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        path = None
        if filename.startswith("0x"):
            path = SCRIPT_DIR + "/cache/" + "{}/{}.pickle".format(filename[0:3], filename)
        else:
            path = SCRIPT_DIR + "/cache/" + "{}.pickle".format(filename)
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        return None


class CrawlEtherscan:
    def __init__(self):
        self.etherscanAPIkeys = settings["settings"]["EtherScanApiKeys"]
        self.counter = random.randint(0, len(self.etherscanAPIkeys))
        self.cacheDeployTx = None
        self.ABIMap = {}
        self.VerifyMap = {}
    
    def getEtherScanAPIkey(self):
        self.counter += 1
        numOfAPIkeys = len(self.etherscanAPIkeys)
        return self.etherscanAPIkeys[self.counter % numOfAPIkeys]


    def Contract2Sourcecode(self, contractAddress: str) -> str:
        """Given a contract address, return the source code"""
        contractAddress = contractAddress.lower()
        filename = "{}_sourcecode".format(contractAddress)
        receiptJson = load_object(filename)
        if receiptJson is not None and not isinstance(receiptJson, str):
            return receiptJson
        GETrequest = 'https://api.etherscan.io/api?module=contract'\
            '&action=getsourcecode'\
            '&address={}'\
            '&apikey={}'.format(contractAddress, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()
        receiptJson = response["result"]
        save_object(receiptJson, filename)
        return receiptJson

    def Contract2ABI(self, contractAddress: str) -> str:
        """Given a contract address, return the ABI"""
        if contractAddress in self.ABIMap:
            return self.ABIMap[contractAddress]
        GETrequest = 'https://api.etherscan.io/api?module=contract'\
            '&action=getabi'\
            '&address={}'\
            '&apikey={}'.format(contractAddress, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()

        if response['result'] == 'Contract source code not verified':
            self.ABIMap[contractAddress] = {}
            return {}
        result = json.loads(response['result'])
        self.ABIMap[contractAddress] = result
        return result
    
    def isVerified(self, contractAddress: str) -> bool:
        """Given a contract address, return if the contract is verified"""
        if contractAddress in self.VerifyMap:
            return self.VerifyMap[contractAddress]
        
        GETrequest = 'https://api.etherscan.io/api?module=contract'\
            '&action=getabi'\
            '&address={}'\
            '&apikey={}'.format(contractAddress, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()
        status = response['status']
        if status == '1':
            self.VerifyMap[contractAddress] = True
            return True
        else:
            self.VerifyMap[contractAddress] = False
            return False

    def Contract2funcSelectors(self, contractAddress: str) -> list:
        """Given a contract address, return a list of function selectors"""
        functionSigMap = self.Contract2funcSigMap(contractAddress)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(functionSigMap)
        # delete constructor
        del functionSigMap["constructor"]
        return list(functionSigMap.keys())

    def Contract2funcSigMap(self, contractAddress, abi = None):
        """Given a contract address, return a map of function signature hash to
        function name"""
        if abi is None:
            abi = self.Contract2ABI(contractAddress)
        functionSigMap = {}
        for function in abi:
            # print(function)
            if function['type'] == 'constructor':
                functionSigMap["constructor"] = ("constructor", [])
                for input in function['inputs']:
                    functionSigMap["constructor"][1].append(input['type'])
                # constructor does not return any value
            if function['type'] == 'function':
                functionSign = function['name'] + '('
                if len(function['inputs']) == 0:
                    functionSign += ')'
                else:
                    for input in function['inputs']:
                        functionSign += input['type'] + ','
                    functionSign = functionSign[:-1] + ')'
                functionSelector = Web3.keccak(text=functionSign).hex()[0:10]
                functionSigMap[functionSelector] = (function['name'], [], [])
                for input in function['inputs']:
                    functionSigMap[functionSelector][1].append(input['type'])
                for output in function['outputs']:
                    functionSigMap[functionSelector][2].append(output['type'])
        return functionSigMap

    def Contract2Bytecode(self, contractAddress: str) -> str:
        """Given a contract address, return the bytecode"""
        GETrequest = 'https://api.etherscan.io/api?module=proxy'\
            '&action=eth_getCode'\
            '&address={}'\
            '&tag=latest'\
            '&apikey={}'.format(contractAddress, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()
        return response['result']

    def Contract2DeployTx(self, contractAddress: str):
        """Given a contract address, return the deploy Tx hash"""
        if self.cacheDeployTx is None:
            self.cacheDeployTx = load_object("cacheDeployTx")
            if self.cacheDeployTx is None:
                self.cacheDeployTx = {}

        if self.cacheDeployTx is not None and contractAddress in self.cacheDeployTx:
            return self.cacheDeployTx[contractAddress]

        GETrequest = 'https://api.etherscan.io/api?module=contract'\
            '&action=getcontractcreation'\
            '&contractaddresses={}'\
            '&apikey={}'.format(contractAddress, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()
        
        if response['status'] == '0' and response['message'] == 'No data found':
            self.cacheDeployTx[contractAddress] = None
            save_object(self.cacheDeployTx, "cacheDeployTx")
            return None
        elif response['status'] == '0' and response['message'] == 'NOTOK' and response['result'] == "Max rate limit reached":
            time.sleep(1)
            return self.Contract2DeployTx(contractAddress)
        else:
            # print(response)
            self.cacheDeployTx[contractAddress] = response['result'][0]['txHash']
            save_object(self.cacheDeployTx, "cacheDeployTx")
            return response['result'][0]['txHash']

    def Tx2Block(self, Tx: str) -> int:
        """Given a Tx hash, return the block number"""
        GETrequest = 'https://api.etherscan.io/api'\
            '?module=transaction'\
            '&action=gettxreceiptstatus'\
            '&txhash={}'\
            '&apikey={}'.format(Tx, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()
        return int(response['result']['blockNumber'])

    def Tx2Receipt(self, Tx: str) -> dict:
        """Given a Tx hash, return the receipt"""
        filename = "{}_Receipt".format(Tx)
        receiptJson = load_object(filename)
        if receiptJson is not None and receiptJson != "Max rate limit reached" :
            return receiptJson
        GETrequest = 'https://api.etherscan.io/api'\
            '?module=proxy'\
            '&action=eth_getTransactionReceipt'\
            '&txhash={}'\
            '&apikey={}'.format(Tx, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()
        # print(response)
        receiptJson = response["result"]
        save_object(receiptJson, filename)
        return receiptJson

    def Tx2SrcAddr(self, Tx: str) -> str:
        receipt = self.Tx2Receipt(Tx)
        return receipt["to"]

    def Tx2Details(self, Tx: str) -> dict:
        receipt = self.Tx2Receipt(Tx)

        if isinstance(receipt, str):
            # print(receipt)
            receipt = json.loads(receipt)

        fromAddress = receipt['from'] 
        toAddress = receipt['to']
        contractAddress = receipt['contractAddress']
        status = receipt['status']
        # status: 0 => failed, 1 => success
        # to: Address of the receiver or null in a contract creation transaction.
        ret = {"contractAddress": contractAddress, "from": fromAddress, "to": toAddress, "status": status}
        return ret

    def Tx2Block(self, Tx: str) -> int:
        """Given a Tx hash, return the block number"""
        receipt = self.Tx2Receipt(Tx)
        blockNumber = receipt['blockNumber'] 
        if isinstance(blockNumber, str):  # it might be a hex string
            blockNumber = int(blockNumber, 16) # convert hex to int
        return blockNumber

    def Contract2DeployBlock(self, contractAddress: str) -> int:
        """Given a contract address, return the deploy block number"""
        deployTx = self.Contract2DeployTx(contractAddress)
        return self.getTxBlock(deployTx)

    def BlockIndex2Tx(self, block: int, blockIndex: int) -> str:
        """Given a block number and a block index, return the tx hash"""
        block_hex = hex(block)
        block_index = hex(blockIndex)
        GETrequest = 'https://api.etherscan.io/api?module=proxy'\
            '&action=eth_getTransactionByBlockNumberAndIndex'\
            '&tag={}'\
            '&index={}'\
            '&apikey={}'.format(block_hex, block_index, self.getEtherScanAPIkey())
        response = requests.get(GETrequest).json()
        # print(response['result']['hash'])
        return response['result']['hash']

    


def main():
    ce = CrawlEtherscan()
    # # test getDeployTx
    contractAddress = '0x5ade7ae8660293f2ebfcefaba91d141d72d221e8' # Eminence Victim Contract
    # deployTx = ce.Contract2DeployTx(contractAddress)
    # print(deployTx)

    # # test BlockIndex2Tx
    # Tx = ce.BlockIndex2Tx(12911679, 3)
    # print(Tx)

    # # test Contract2Bytecode
    # bytecode = ce.Contract2Bytecode(contractAddress)
    # print(bytecode)

    # # test Tx2Details
    # Tx = "0x911c32767fabb090813d9661803d508e05a4edef562704679cb351f65b81ada1"
    # details = ce.Tx2Details(Tx)
    # print(details)

    # test Contract2ABI
    ABI = ce.Contract2ABI(contractAddress)
    print(json.dumps(ABI, indent=4))

    # # test Contract2funcSigMap
    # functionSigMap = ce.Contract2funcSigMap(contractAddress)
    # print(functionSigMap)

    # test Contract2funcSelectors
    # Yearn attack
    # contractAddress = "0xacd43e627e64355f1861cec6d3a6688b31a6f952"

    # funcSelectors = ce.Contract2funcSelectors(contractAddress)
    # print(funcSelectors)

    # test Contract2BscInternalTxs
    # endBlock = 34041500
    # address = "0x4e332D616b5bA1eDFd87c899E534D996c336a2FC"
    # # Txs = ce.Contract2BscInternalTxs(address, endBlock)
    # Txs = ce.Contract2FtmTxs(address, endBlock)
    # for Tx in Txs:
    #     print (Tx)
    # print(len(Txs))

    # from crawlPhalcon import CrawlPhalcon
    # cp = CrawlPhalcon(chainID = 2)

    # for Tx in Txs:
    #     msg  = cp.Tx2Msg2(Tx)

    #     if "get_dy" in msg or "calc_token_amount" in msg or \
    #         "calc_withdraw_one_coin" in msg or "lp_price" in msg or \
    #         "get_virtual_price" in msg or "price_oracle" in msg or \
    #         "balances" in msg or "xcp_profit" in msg or "xcp_profit_a" in msg or \
    #         "virtual_price" in msg:
            
    #         print(Tx)

    # get_dy

    # calc_token_amount

    # calc_withdraw_one_coin

    # lp_price

    # get_virtual_price

    # price_oracle

    # balances 

    # xcp_profit

    # xcp_profit_a

    # virtual_price

        


## Assume Guassian Distribution 

## logritmic Gaussian





if __name__ == '__main__':
    main()