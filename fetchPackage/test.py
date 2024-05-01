from web3 import Web3, HTTPProvider
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import toml
settings = toml.load("settings.toml")
from fetchPackage.StackCarpenter import stackCarpener
import json


# GAS opcode returns "gas" in structLogs


# SimpleDAItransferTx = "0xeeb70054c1a08dd366570184d2da9457b08a620e2ffbbf5954bed5d8ec630943"
# gas limit: 90000
# SimpleDAItransferTx2 = "0x164839b9cbf25f6050df6abc61b823baae736eef9af03fac60a9a0c87c642b63"
# gas limit: 69436
# SimpleDAItransferTx3 = "0xd63b4308a9dafc426f468e568ab52d1c4738de0e66b5acbc3947709d15265227"
# gas limit: 51842

print(90000 - 68320)
print(69436 - 47792)
print(51842 - 30198)


for filename in ["DAItransferfulltrace.json", "DAItransferfulltrace2.json", "DAItransferfulltrace3.json"]:
    
    print("==============", filename, "==================")
    filePath = SCRIPT_DIR + "/" + filename

    logs = json.load(open(filePath, "r"))

    gasConsumed = 0
    for structLog in logs["structLogs"]:
        gasConsumed += structLog["gasCost"]

    print("start gas:", logs["structLogs"][0]["gas"])
    print("gasConsumed:", gasConsumed)
    print("end gas:", logs["structLogs"][-1]["gas"])
    print("Gas Usage by Txn:", logs["gas"])
    print("Gas Usage by Txn - gasConsumed:", logs["gas"] - gasConsumed)
