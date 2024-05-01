
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





if __name__ == '__main__':
    ce = CrawlEtherscan()

    receipt = ce.Tx2SrcAddr("0x37085f336b5d3e588e37674544678f8cb0fc092a6de5d83bd647e20e5232897b")

    pprint.pprint(receipt)
