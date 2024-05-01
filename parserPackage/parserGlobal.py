# a localized version of parser.py
import struct
import sys
import os
import time
import json
from crawlPackage.crawlEtherscan import CrawlEtherscan
from crawlPackage.crawlQuicknode import CrawlQuickNode
from staticAnalyzer.analyzer import Analyzer
from parserPackage.decoder import decoder
from parserPackage.functions import *
from parserPackage.traceTree import TraceTree
from utilsPackage.compressor import writeCompressedJson, readCompressedJson

from web3 import Web3
import copy
import cProfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))



def checkmapPositionInStorageMapping(mapPosition, storageMapping, preimage):
    """Given a mapPosition and a storageMapping, check if the mapPosition is in the storageMapping"""
    # storageMapping: {0: ('Ownable._owner', 'address'), 32: ('Pausable.pauser', 'address'), 52: ('Pausable.paused', 'bool'), 64: ('Blacklistable.blacklister', 'address'), 96: ('Blacklistable.blacklisted', ('address', 'bool')), 128: ('FiatTokenV1.name', 'string'), 160: ('FiatTokenV1.symbol', 'string'), 192: ('FiatTokenV1.decimals', 'uint8'), 224: ('FiatTokenV1.currency', 'string'), 256: ('FiatTokenV1.masterMinter', 'address'), 276: ('FiatTokenV1.initialized', 'bool'), 288: ('FiatTokenV1.balances', ('address', 'uint256')), 320: ('FiatTokenV1.allowed', ('address', ('address', 'uint256'))), 352: ('FiatTokenV1.totalSupply_', 'uint256'), 384: ('FiatTokenV1.minters', ('address', 'bool')), 416: ('FiatTokenV1.minterAllowed', ('address', 'uint256')), 448: ('Rescuable._rescuer', 'address'), 480: ('EIP712Domain.DOMAIN_SEPARATOR', 'bytes32'), 512: ('GasAbstraction.TRANSFER_WITH_AUTHORIZATION_TYPEHASH', 'bytes32'), 544: ('GasAbstraction.APPROVE_WITH_AUTHORIZATION_TYPEHASH', 'bytes32'), 576: ('GasAbstraction.INCREASE_ALLOWANCE_WITH_AUTHORIZATION_TYPEHASH', 'bytes32'), 608: ('GasAbstraction.DECREASE_ALLOWANCE_WITH_AUTHORIZATION_TYPEHASH', 'bytes32'), 640: ('GasAbstraction.CANCEL_AUTHORIZATION_TYPEHASH', 'bytes32'), 672: ('GasAbstraction._authorizationStates', ('address', ('bytes32', 'GasAbstraction.AuthorizationState'))), 704: ('Permit.PERMIT_TYPEHASH', 'bytes32'), 736: ('Permit._permitNonces', ('address', 'uint256')), 768: ('FiatTokenV2._initializedV2', 'bool')}
    # preimage:  
    # {'0x882d7ed9f2a3bb94081200846cb72e20b34d0a96f26eafd7e2ec91639183323c': 
    #       ('Solc', 
    #       '0000000000000000000000000000000000000000000000000000000000000003', 
    #       '000000000000000000000000bebc44782c7db0a1a60cb6fe97d0b483032ff1c7'), 
    # '0x8caee21460e4b97ad21ef6f50ba78c06f8ace770150686bffca228a84ab684a8': 
    #       ('Solc', 
    #       '0000000000000000000000000000000000000000000000000000000000000003', 
    #       '0000000000000000000000009c211bfa6dc329c5e757a223fb72f5481d676dc1'), 
    # '0xbeff42312369bb0ffea406565ab897ad38d0d32a39e2ed7b1fcdcb8dca706a8': 
    #       ('Solc', 
    #       '000000000000000000000000000000000000000000000000000000000000000a', 
    #       '0000000000000000000000009c211bfa6dc329c5e757a223fb72f5481d676dc1'), 
    # '0xf8e05935db44fb75f76ff7f18f35b7e3d12441171b26eeafb55f7a73378f7641': 
    #       ('Solc', 
    #       '0beff42312369bb0ffea406565ab897ad38d0d32a39e2ed7b1fcdcb8dca706a8', 
    #       '000000000000000000000000bebc44782c7db0a1a60cb6fe97d0b483032ff1c7')
    # }

    pass




class VmtraceParser:
    def __init__(self):
        self.analyzer = Analyzer()
        self.crawlQuickNode = CrawlQuickNode()
        self.indent = 0
        self.logging = 0
        self.loggingUpper = 3
        ##### They four should be one struct
        self.msgSenderStack = None
        self.contractAddressStack = None
        self.isDelegateCallStack = None
        #####
        self.contractAddress = None
        self.decoder = decoder()
        self.printAll = False
        self.printMessageStack = self.printAll or False

    def printStack(self):
        if self.printMessageStack:
            print("========msgSenderStack", self.msgSenderStack)
            print("==contractAddressStack", self.contractAddressStack)
            print("===isDelegateCallStack", self.isDelegateCallStack)


    def getMsgSender(self, isDelegate: bool = False):
        if len(self.msgSenderStack) != len(self.isDelegateCallStack):
            sys.exit("Error: len(msgSenderStack) != len(isDelegateCallStack)")
        if len(self.msgSenderStack) != len(self.contractAddressStack):
            sys.exit("Error: len(msgSenderStack) != len(contractAddressStack)")

        if isDelegate:
            return self.msgSenderStack[-1]
        elif not self.isDelegateCallStack[-1]:
            return self.contractAddressStack[-1]
        else:
            for jj in range(len(self.isDelegateCallStack) - 1, -1, -1):
                if not self.isDelegateCallStack[jj]:
                    return self.contractAddressStack[jj]
        

    def parseLogsGzip(self, category, contractAddress: str, txHash: str):
        trace = getTraceFromCategoryTxHash(category, contractAddress, txHash)
        # with open("temp.json", "w") as f:
        #     json.dump(trace, f, indent = 2)

        return self.parseLogs(contractAddress.lower(), txHash, trace)

    def parseLogsJson(self, contractAddress: str, txHash: str, jsonFile):
        """Given a json file, parse the trace and return logs"""
        trace = getTrace(jsonFile)
        return self.parseLogs(contractAddress.lower(), txHash, trace)

    def printIndentContent(self, *values: object):
        """Given an indent and a content, print the content with the indent"""
        for _ in range(self.indent - 1):
            print("\t", end = '')
        print(*values)

    def printIndentContentLogging(self, *values: object):
        """Given an indent and a content, print the content with the indent"""
        if self.printAll:
            for _ in range(self.indent - 1):
                print("\t", end = '')
            print(*values)

        if not self.printAll and self.logging > 0 and self.indent <= 2:
            if self.contractAddress not in self.contractAddressStack:
                sys.exit("Error! contractAddress not in contractAddressStack")

            for _ in range(self.indent - 1):
                print("\t", end = '')
            print(*values)

    def setupGlobalState(self, txHash: str):
        details = self.crawlQuickNode.Tx2Details(txHash)
        fromAddress = details["from"].lower()
        status = details["status"]

        toAddress = details["to"]
        interactContract = details["contractAddress"]
        
        # global states of a transaction
        origin = fromAddress
        msgSenderStack = [fromAddress]
        contractAddressStack = None
        isDelegateCallStack = None
        if toAddress != None:
            contractAddressStack = [toAddress.lower()]
            isDelegateCallStack = [False]
        elif interactContract != None:
            contractAddressStack = [interactContract.lower()]
            isDelegateCallStack = [False]
        else:
            sys.exit("Error: both toAddress and interactContract are None")

        self.msgSenderStack = msgSenderStack
        self.contractAddressStack = contractAddressStack
        self.isDelegateCallStack = isDelegateCallStack
        
        return status, origin

    def decrementLogging(self):
        if self.logging > 0:
            self.logging -= 1

    def incrementLogging(self, addr: str):
        if self.logging > 0:
            self.logging += 1
        elif addr == self.contractAddress.lower():
            if self.logging != 0:
                sys.exit("Error: logging != 0")
            self.logging += 1

    def parseLogs(self, contractAddress: str, txHash: str, trace: dict, functions2protect: list = None):
        """Given a trace, return a list of logs restricted to <contractAddress>"""
        """These logs should be ready to feed into an invariant checker"""

        self.contractAddress = contractAddress.lower()
        contractAddress = self.contractAddress

        # storage layout of THE contract
        storageMapping = self.analyzer.contract2storageMapping(contractAddress)
        storageMappingMap = {contractAddress: storageMapping} # We also need some other contracts 
        
        funcSigMap = self.analyzer.contract2funcSigMap(contractAddress)
        funcSigMapMap = {contractAddress: funcSigMap}

        for function in functions2protect:
            isIn = False
            for funcSig in funcSigMap:
                if function == funcSigMap[funcSig][0]:
                    isIn = True
                    break
            if not isIn:
                sys.exit("Error: function not in funcSigMap")


        self.calldataStack = [{"calldata":"", "preimage":{}}] # calldata of the function, a stack
        # eg. {
        #     "calldata": "0x12345678",
        #     "calldatasize": "0x12345678",
        # }

        funcSelector = "" # function selector of the function, a temp
        self.funcSelectorStack = [""] # function selector, a stack


        # self.calldataStack
        # self.funcSelectorStack
        # self.msgSenderStack
        # self.contractAddressStack
        # self.isDelegateCallStack


        status, origin = self.setupGlobalState(txHash)

        # print("Tx Origin = ", origin)


        metaData = {"txHash": txHash, "status": status, "origin": origin}
        if status == 0:
            return metaData

        metaTraceTree = TraceTree(metaData) # function calls represent what we really care

        # Basically, it records a list of function calls to the <contractAddress>
        
        # eg. functionLog = {
        #   "type": "call", or "constructor", or "fallback"
        #   "from": "0x12345678",
        #   "tx.origin": "0x12345678",
        #   "msg.sender": "0x12345678",
        #   "functionSelector": "0x12345678",
        #   children: [
        #      sload 
        #      calldataread
        #      sload
        #      sstore
        #      functionLog
        #      functionLog
        #      sload
        #   ]
        # 
        # }
        
        if status == 0:
            sys.exit("Error: transaction reverted(cannot handle temporarily)")

        self.logging = 0  # 0: not logging, >=1: logging

        structLogs = trace['structLogs']

        ii = -1

        while ii < len(structLogs) - 1:
            ii += 1
            self.indent = structLogs[ii]["depth"]
            # if ii+1 < len(structLogs):
                # gas1 = structLogs[ii]["gas"]
                # gas2 = structLogs[ii+1]["gas"]
                # if gas2 > gas1:
                #     print("=========gas increases")



            # A log should start from CALL/STATICCALL/DELEGATECALL/CREATE/CREATE2/
            # end with RETURN/STOP/REVERT/SELFDESTRUCT
            if ii + 1 < len(structLogs) and \
                (structLogs[ii]["op"] == "CREATE" or structLogs[ii]["op"] == "CREATE2"):
                opcode = structLogs[ii]["op"]
                value = structLogs[ii]["stack"][-1]
                offset = structLogs[ii]["stack"][-2]
                size = structLogs[ii]["stack"][-3]
                if structLogs[ii]["op"] == "CREATE2":
                    salt = structLogs[ii]["stack"][-4]
                depth = structLogs[ii]["depth"]
                addr = None
                for jj in range(ii + 1, len(structLogs)):
                    if structLogs[jj]["depth"] == depth:
                        addr = structLogs[jj]["stack"][-1]
                        break
                
                self.incrementLogging(addr)

                msgSender = self.getMsgSender()
                self.msgSenderStack.append(msgSender)
                self.funcSelectorStack.append(funcSelector)
                funcSelector = "constructor"


                infoDict = {"type": opcode.lower(), "structLogsStart": ii,  "addr": addr, "msg.sender": msgSender}
                newTraceTree =  TraceTree(infoDict)
                
                if addr == contractAddress and self.logging == 1:
                    # means we are calling a function inside the target contract
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)
                elif self.logging > 1:
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)


                # print(self.funcSelectorStack)

                self.calldataStack.append({"calldata":"", "preimage":{}})  # preimage is a map from key to keccak(key)
                self.contractAddressStack.append(addr)
                self.isDelegateCallStack.append(False)
                

                self.printIndentContentLogging(opcode, "value = ", value,  "address = ", addr)
                self.printIndentContentLogging("msg.sender = ", msgSender, "({} does change msg.sender)".format(opcode))
                self.printIndentContentLogging("Currently Entering into a contract", addr)
                
                if self.logging > 0:
                    if contractAddress not in self.contractAddressStack:
                        sys.exit("Error: contractAddress not in self.contractAddressStack")
                    if addr not in funcSigMapMap: # and not self.analyzer.isVyper(addr):
                        funcSigMapMap[addr] = self.analyzer.contract2funcSigMap(addr)
                    if addr not in storageMappingMap: # and not self.analyzer.isVyper(addr):
                        storageMappingMap[addr] = self.analyzer.contract2storageMapping(addr)
                        
            # Call a function inside another contract
            elif structLogs[ii]["op"] == "CALL" and "error" not in structLogs[ii]:
                gas = Web3.toInt(hexstr = structLogs[ii]["stack"][-1])
                addr = structLogs[ii]["stack"][-2]
                if len(addr) > 42:
                    addr = '0x' + addr[-40:]
                value = structLogs[ii]["stack"][-3]
                argsOffset = structLogs[ii]["stack"][-4]
                argsLength = structLogs[ii]["stack"][-5]
                retOffset = structLogs[ii]["stack"][-6]
                retLength = structLogs[ii]["stack"][-7]

                if addr == "0x1" or addr == "0x2" or addr == "0x3" or addr == "0x4":
                    # 0x1 represents: ECREC
                    # 0x2 represents: SHA256
                    # 0x3 represents: RIP160
                    # 0x4 represents: IDENTITY
                    continue

                if structLogs[ii]["depth"] == structLogs[ii + 1]["depth"]:
                    # looks like a fallback function
                    # In rare rare cases, "CALL" opcode does not increase the depth
                    # which means we should not change stacks
                    self.printIndentContentLogging("call(gas = {}, addr = {}, value = {}, argsOffset = {}, argsLength = {})".format(gas, addr, value, argsOffset, argsLength))
                    self.printIndentContentLogging("call does not increase depth")
                    continue

                self.incrementLogging(addr)
                msgSender = self.getMsgSender()
                self.msgSenderStack.append(msgSender)
                self.funcSelectorStack.append(funcSelector)
                funcSelector = ""

                # print(self.funcSelectorStack)

                infoDict = {"type": "call", "structLogsStart": ii, "gas": gas, "addr": addr, "msg.value": value, "msg.sender": msgSender, "retOffset": retOffset, "retLength": retLength}
                newTraceTree =  TraceTree(infoDict)
                
                if addr == contractAddress and self.logging == 1:
                    # means we are calling a function inside the target contract
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)
                elif self.logging > 1:
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)

                self.calldataStack.append({"calldata":"", "preimage":{}})
                
                self.contractAddressStack.append(addr)
                self.isDelegateCallStack.append(False)

                self.printIndentContentLogging("call(gas = {}, addr = {}, value = {}, argsOffset = {}, argsLength = {})".format(gas, addr, value, argsOffset, argsLength))
                self.printIndentContentLogging("msg.sender = ", msgSender, "(Call does change msg.sender)")
                self.printIndentContentLogging("Currently Entering into a contract", addr)

                # print("self.msgSenderStack = ", self.msgSenderStack)

                if self.logging > 0:
                    if contractAddress not in self.contractAddressStack:
                        sys.exit("Error: contractAddress not in self.contractAddressStack")
                    if addr not in funcSigMapMap: # and not self.analyzer.isVyper(addr):
                        funcSigMapMap[addr] = self.analyzer.contract2funcSigMap(addr)
                    if addr not in storageMappingMap: # and not self.analyzer.isVyper(addr):
                        storageMappingMap[addr] = self.analyzer.contract2storageMapping(addr)
   
            # Call a function inside another contract
            elif structLogs[ii]["op"] == "CALLCODE" and "error" not in structLogs[ii]:
                gas = Web3.toInt(hexstr = structLogs[ii]["stack"][-1])
                addr = structLogs[ii]["stack"][-2]
                if len(addr) > 42:
                    addr = '0x' + addr[-40:]
                value = structLogs[ii]["stack"][-3]
                argsOffset = structLogs[ii]["stack"][-4]
                argsLength = structLogs[ii]["stack"][-5]
                retOffset = structLogs[ii]["stack"][-6]
                retLength = structLogs[ii]["stack"][-7]

                if addr == "0x1" or addr == "0x2" or addr == "0x3" or addr == "0x4":
                    # 0x1 represents: ECREC
                    # 0x2 represents: SHA256
                    # 0x3 represents: RIP160
                    # 0x4 represents: IDENTITY
                    continue

                self.incrementLogging(addr)


                msgSender = self.getMsgSender()
                self.msgSenderStack.append(msgSender)
                self.funcSelectorStack.append(funcSelector)
                funcSelector = ""

                # print(self.funcSelectorStack)
                
                infoDict = {"type": "callcode", "structLogsStart": ii, "gas": gas, "addr": addr, "msg.value": value, "msg.sender": msgSender, "retOffset": retOffset, "retLength": retLength}
                newTraceTree =  TraceTree(infoDict)
                
                if addr == contractAddress and self.logging == 1:
                    # means we are calling a function inside the target contract
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)
                elif self.logging > 1:
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)

                self.calldataStack.append({"calldata":"", "preimage":{}})
                
                
                self.contractAddressStack.append(addr)
                self.isDelegateCallStack.append(True)


                self.printIndentContentLogging("callcode(gas = {}, addr = {}, value = {}, argsOffset = {}, argsLength = {})".format(gas, addr, value, argsOffset, argsLength))
                self.printIndentContentLogging("msg.sender = ", msgSender, "(Callcode does change msg.sender)")
                self.printIndentContentLogging("Currently Entering into a contract", addr)

                # print("self.msgSenderStack = ", self.msgSenderStack)

                if self.logging > 0:
                    if contractAddress not in self.contractAddressStack:
                        sys.exit("Error: contractAddress not in self.contractAddressStack")
                    if addr not in funcSigMapMap: # and not self.analyzer.isVyper(addr):
                        funcSigMapMap[addr] = self.analyzer.contract2funcSigMap(addr)
                    if addr not in storageMappingMap: # and not self.analyzer.isVyper(addr):
                        storageMappingMap[addr] = self.analyzer.contract2storageMapping(addr)

            # calls a method in another contract with state changes disallowed
            elif structLogs[ii]["op"] == "STATICCALL" and "error" not in structLogs[ii]:
                gas = Web3.toInt(hexstr = structLogs[ii]["stack"][-1])
                addr = structLogs[ii]["stack"][-2]
                if len(addr) > 42:
                    addr = '0x' + addr[-40:]
                argsOffset = structLogs[ii]["stack"][-3]
                argsLength = structLogs[ii]["stack"][-4]
                retOffset = structLogs[ii]["stack"][-5]
                retLength = structLogs[ii]["stack"][-6]
                
                if addr == "0x1" or addr == "0x2" or addr == "0x3" or addr == "0x4":
                    # 0x1 represents: ECREC
                    # 0x2 represents: SHA256
                    # 0x3 represents: RIP160
                    # 0x4 represents: IDENTITY
                    continue

                self.incrementLogging(addr)

                msgSender = self.getMsgSender()
                self.msgSenderStack.append(msgSender)
                self.funcSelectorStack.append(funcSelector)
                funcSelector = ""

                # print(self.funcSelectorStack)


                infoDict = {"type": "staticcall", "structLogsStart": ii, "gas": gas, "addr": addr, "msg.sender": msgSender, "retOffset": retOffset, "retLength": retLength}
                newTraceTree =  TraceTree(infoDict)
                
                if addr == contractAddress and self.logging == 1:
                    # means we are calling a function inside the target contract
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)
                elif self.logging > 1:
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)


                self.calldataStack.append({"calldata":"", "preimage":{}})
                
                self.contractAddressStack.append(addr)
                self.isDelegateCallStack.append(False)

                self.printIndentContentLogging("staticcall(gas = {}, addr = {}, argsOffset = {}, argsLength = {})".format(gas, addr, argsOffset, argsLength))
                self.printIndentContentLogging("msg.sender = ", msgSender, "(Staticcall does change msg.sender)") 
                self.printIndentContentLogging("Currently Entering into a contract", addr)

                # print("self.msgSenderStack = ", self.msgSenderStack)

                if self.logging > 0:
                    if contractAddress not in self.contractAddressStack:
                        sys.exit("Error: contractAddress not in self.contractAddressStack")
                    if addr not in funcSigMapMap: # and not self.analyzer.isVyper(addr):
                        funcSigMapMap[addr] = self.analyzer.contract2funcSigMap(addr)
                    if addr not in storageMappingMap: # and not self.analyzer.isVyper(addr):
                        storageMappingMap[addr] = self.analyzer.contract2storageMapping(addr)

            #  calls a method in another contract, using the storage of the current contract
            elif structLogs[ii]["op"] == "DELEGATECALL" and "error" not in structLogs[ii]:
                gas = Web3.toInt(hexstr = structLogs[ii]["stack"][-1])
                addr = structLogs[ii]["stack"][-2]
                if len(addr) > 42:
                    addr = '0x' + addr[-40:]
                argsOffset = structLogs[ii]["stack"][-3]
                argsLength = structLogs[ii]["stack"][-4]
                retOffset = structLogs[ii]["stack"][-5]
                retLength = structLogs[ii]["stack"][-6]


                if addr == "0x1" or addr == "0x2" or addr == "0x3" or addr == "0x4":
                    # 0x1 represents: ECREC
                    # 0x2 represents: SHA256
                    # 0x3 represents: RIP160
                    # 0x4 represents: IDENTITY
                    continue

                self.incrementLogging(addr)

                msgSender = self.getMsgSender(isDelegate=True)
                self.msgSenderStack.append(msgSender)
                self.funcSelectorStack.append(funcSelector)
                funcSelector = ""
                # print(self.funcSelectorStack)


                infoDict = {"type": "delegatecall", "structLogsStart": ii,  "gas": gas, "addr": addr, "msg.sender": msgSender, "retOffset": retOffset, "retLength": retLength}
                newTraceTree =  TraceTree(infoDict)
                
                if addr == contractAddress and self.logging == 1:
                    # means we are calling a function inside the target contract
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)
                elif self.logging > 1:
                    metaTraceTree.addInternalCall(newTraceTree, self.logging)

                self.calldataStack.append({"calldata":"", "preimage":{}})
                
                self.contractAddressStack.append(addr)
                self.isDelegateCallStack.append(True)

                self.printIndentContentLogging("delegatecall(gas = {}, addr = {}, argsOffset = {}, argsLength = {})".format(gas, addr, argsOffset, argsLength))
                self.printIndentContentLogging("msg.sender = ", msgSender, "(delegate call does not change msg.sender)")
                self.printIndentContentLogging("Currently Entering into a contract", addr)

                # print("self.msgSenderStack = ", self.msgSenderStack)

                if self.logging > 0:
                    if contractAddress not in self.contractAddressStack:
                        sys.exit("Error: contractAddress not in self.contractAddressStack")
                    if addr not in funcSigMapMap: # and not self.analyzer.isVyper(addr):
                        funcSigMapMap[addr] = self.analyzer.contract2funcSigMap(addr)
                    if addr not in storageMappingMap: # and not self.analyzer.isVyper(addr):
                        storageMappingMap[addr] = self.analyzer.contract2storageMapping(addr)

            # check if matches the pattern of RETURN
            if structLogs[ii]["op"] == "RETURN":
                # self.printIndentContent("Function Returns with something(RETURN)")
                self.printIndentContentLogging("Currently Leaving from a contract(RETURN)", self.contractAddressStack[-1])
                calldata = self.calldataStack[-1]["calldata"]
                self.printIndentContentLogging("callData = ", calldata)

                if self.logging > 0:    
                    offset = structLogs[ii]["stack"][-1]
                    length = structLogs[ii]["stack"][-2]
                    self.printIndentContentLogging("Function Returns memory[{}:{}+{}]".format(offset, offset, length))
                    # self.printIndentContentLogging("memory = ",  structLogs[ii]["memory"])
                    currentContract = self.contractAddressStack[-1]

                    

                    # print("currentContract", currentContract)
                    # print("funcSelector", funcSelector)
                    # print("funcSigMapMap[currentContract]", funcSigMapMap[currentContract])

                    types = None
                    decoded = None
                    if funcSelector != "":
                        types = funcSigMapMap[currentContract][funcSelector][2]
                        decoded = self.decoder.decodeReturn(types, structLogs[ii]["memory"], offset, length)
                    else:
                        types = "None(Fallabck Function)"
                        decoded = "None(Fallabck Function)"
                    
                    
                    
                    self.printIndentContentLogging("Decoded return value types = ", types)
                    self.printIndentContentLogging("Decoded return value = ", decoded)

                    Info = {"structLogsEnd": ii, "returnValue": decoded, "returnType": types}

                    # print("types:", types)
                    # print("calldata:", calldata)
                    # print("currentContract:", currentContract)
                    # print("funcSelector:", funcSelector)
                    # print("funcSigMapMap:", funcSigMapMap[currentContract][funcSelector])

                    types = None
                    decoded = None
                    if funcSelector != "":
                        types = funcSigMapMap[currentContract][funcSelector][1]
                        decoded = self.decoder.decodeSimpleABI(types, calldata[8:]) # remove the first 4 bytes, which is the function selector
                    else:
                        types = "None(Fallabck Function)"
                        decoded = "None(Fallabck Function)"

                    self.printIndentContentLogging("Decoded calldata types = ", types)
                    self.printIndentContentLogging("Decoded calldata = ", decoded)

                    Info.update({"calldataValue": decoded, "calldataType": types})
                    Info.update({"returnType": "RETURN", "function": funcSigMapMap[currentContract][funcSelector][0]})

                    metaTraceTree.updateInfo(Info, self.logging)


                funcSelector = self.funcSelectorStack.pop()
                self.contractAddressStack.pop()
                self.msgSenderStack.pop()
                self.isDelegateCallStack.pop()
                self.calldataStack.pop()
                
                self.decrementLogging()

            elif structLogs[ii]["op"] == "STOP":
                # self.printIndentContent("Function Returns with nothing(STOP)")
                self.printIndentContentLogging("Currently Leaving from a contract(STOP)", self.contractAddressStack[-1])
                calldata = self.calldataStack[-1]["calldata"]
                self.printIndentContentLogging("callData = ", calldata)
                    

                if self.logging > 0:
                    currentContract = self.contractAddressStack[-1]
                    if not self.analyzer.isVyper(currentContract):
                        types = funcSigMapMap[currentContract][funcSelector][1]
                        if len(types)!=0:
                            # print("types:", types)
                            # print("calldata:", calldata)
                            # print("calldataStack:", self.calldataStack)
                            decoded = self.decoder.decodeSimpleABI(types, calldata[8:]) # remove the first 4 bytes, which is the function selector
                            self.printIndentContentLogging("Decoded calldata types = ", types)
                            self.printIndentContentLogging("Decoded calldata = ", decoded)
                    else:
                        # self.printIndentContentLogging("Currently does not support Vyper ")
                        types = funcSigMapMap[currentContract][funcSelector][1]
                        if len(types)!=0:
                            # print("types:", types)
                            # print("calldata:", calldata)
                            # print("calldataStack:", self.calldataStack)
                            decoded = self.decoder.decodeSimpleABI(types, calldata[8:]) # remove the first 4 bytes, which is the function selector
                            self.printIndentContentLogging("Decoded calldata types = ", types)
                            self.printIndentContentLogging("Decoded calldata = ", decoded)
                    
                    Info = {"function": funcSigMapMap[currentContract][funcSelector][0], "returnType": "STOP", "structLogsEnd": ii}
                    Info.update({"calldataValue": decoded, "calldataType": types})
                    metaTraceTree.updateInfo(Info, self.logging)
                
                funcSelector = self.funcSelectorStack.pop()
                self.contractAddressStack.pop()
                self.msgSenderStack.pop()
                self.isDelegateCallStack.pop()
                self.calldataStack.pop()


                self.decrementLogging()

            elif structLogs[ii]["op"] == "REVERT":
                # self.printIndentContent("Function Returns with nothing(REVERT)")
                self.printIndentContentLogging("Currently Leaving from a contract(REVERT)", self.contractAddressStack[-1])
                calldata = self.calldataStack[-1]["calldata"]
                self.printIndentContentLogging("callData = ", calldata)


                if self.logging > 0:    
                    currentContract = self.contractAddressStack[-1]
                    types = None
                    decoded = None
                    if funcSelector != "":
                        types = funcSigMapMap[currentContract][funcSelector][1]
                        decoded = self.decoder.decodeSimpleABI(types, calldata[8:]) # remove the first 4 bytes, which is the function selector
                    else:
                        types = "None(Fallabck Function)"
                        decoded = "None(Fallabck Function)"
                    self.printIndentContentLogging("Decoded calldata types = ", types)
                    self.printIndentContentLogging("Decoded calldata = ", decoded)

                    Info = {"function": funcSigMapMap[currentContract][funcSelector][0], "returnType": "REVERT", "structLogsEnd": ii}
                    Info.update({"calldataValue": decoded, "calldataType": types})
                    metaTraceTree.updateInfo(Info, self.logging)


                funcSelector = self.funcSelectorStack.pop()
                self.contractAddressStack.pop()
                self.msgSenderStack.pop()
                self.isDelegateCallStack.pop()
                self.calldataStack.pop()
                
                self.decrementLogging()

            elif structLogs[ii]["op"] == "SELFDESTRUCT":
                # self.printIndentContent("Function Returns with nothing(SELFDESTRUCT)")
                self.printIndentContentLogging("Currently Leaving from a contract(SELFDESTRUCT)", self.contractAddressStack[-1])
                calldata = self.calldataStack[-1]["calldata"]
                self.printIndentContentLogging("callData = ", calldata)

                if self.logging > 0:
                    metaTraceTree.updateInfo({"function": funcSigMapMap[currentContract][funcSelector][0], "returnType": "SELFDESTRUCT", "structLogsEnd": ii}, self.logging)

                if self.logging > 0:    
                    currentContract = self.contractAddressStack[-1]
                    if not self.analyzer.isVyper(currentContract):
                        types = funcSigMapMap[currentContract][funcSelector][1]
                        decoded = self.decoder.decodeSimpleABI(types, calldata[8:]) # remove the first 4 bytes, which is the function selector
                        self.printIndentContentLogging("Decoded calldata types = ", types)
                        self.printIndentContentLogging("Decoded calldata = ", decoded)
                    else:
                        # self.printIndentContentLogging("Currently does not support Vyper ")
                        types = funcSigMapMap[currentContract][funcSelector][1]
                        decoded = self.decoder.decodeSimpleABI(types, calldata[8:]) # remove the first 4 bytes, which is the function selector
                        self.printIndentContentLogging("Decoded calldata types = ", types)
                        self.printIndentContentLogging("Decoded calldata = ", decoded)

                    Info = {"function": funcSigMapMap[currentContract][funcSelector][0], "returnType": "SELFDESTRUCT", "structLogsEnd": ii}
                    Info.update({"calldataValue": decoded, "calldataType": types})
                    metaTraceTree.updateInfo(Info, self.logging)


                funcSelector = self.funcSelectorStack.pop()
                self.contractAddressStack.pop()
                self.msgSenderStack.pop()
                self.isDelegateCallStack.pop()
                self.calldataStack.pop()


                self.decrementLogging()

            elif structLogs[ii + 1]["depth"] < structLogs[ii]["depth"] \
                and structLogs[ii]["op"] != "STOP" and structLogs[ii]["op"] != "RETURN" \
                and structLogs[ii]["op"] != "REVERT" and structLogs[ii]["op"] != "INVALID" \
                and structLogs[ii]["op"] != "SELFDESTRUCT":

                # print("gas=", structLogs[ii]["gas"])
                # print(structLogs[ii])
                # print(structLogs[ii + 1])

                # self.printIndentContent("Function Returns with nothing(GASLESS)")
                self.printIndentContentLogging("Currently Leaving from a contract(GASLESS)", self.contractAddressStack[-1])
                calldata = self.calldataStack[-1]["calldata"]
                self.printIndentContentLogging("callData = ", calldata)


                if self.logging > 0:    
                    currentContract = self.contractAddressStack[-1]
                    types = None
                    decoded = None
                    if funcSelector != "":
                        types = funcSigMapMap[currentContract][funcSelector][1]
                        decoded = self.decoder.decodeSimpleABI(types, calldata[8:]) # remove the first 4 bytes, which is the function selector
                    else:
                        types = "None(Fallabck Function)"
                        decoded = "None(Fallabck Function)"
                    self.printIndentContentLogging("Decoded calldata types = ", types)
                    self.printIndentContentLogging("Decoded calldata = ", decoded)

                    Info = {"function": funcSigMapMap[currentContract][funcSelector][0], "returnType": "GASLESS", "structLogsEnd": ii}
                    Info.update({"calldataValue": decoded, "calldataType": types})
                    metaTraceTree.updateInfo(Info, self.logging)


                funcSelector = self.funcSelectorStack.pop()
                self.contractAddressStack.pop()
                self.msgSenderStack.pop()
                self.isDelegateCallStack.pop()
                self.calldataStack.pop()
                
                self.decrementLogging()

            elif "error" in structLogs[ii]:
                sys.exit("Parser: \'error\' in structLogs, but not handled by gasless send")
                

            # # self.logging == 1 means we just called a function inside the contract
            # # self
            # if self.logging > 4:
            #      continue
            




            if structLogs[ii]["op"] == "SHA3": # or structLogs[ii]["op"] == "":
                # keccak256(key) = hashValue
                
                offset = structLogs[ii]["stack"][-1]
                length = structLogs[ii]["stack"][-2]
                key = self.decoder.extractMemory(structLogs[ii]["memory"], offset, length)
                hashValue = structLogs[ii+1]["stack"][-1]

                # remove 0x from hashValue and add padding 0s
                hashValue = hashValue[2:]
                hashValue = "0" * (64 - len(hashValue)) + hashValue
                hashValue = "0x" + hashValue

                if len(key) == 128:
                    # mapping
                    if self.logging > 0:
                        currentContract = self.contractAddressStack[-1]
                        if currentContract not in storageMappingMap:
                            sys.exit("Error! currentContract not in storageMappingMap")
                        if self.analyzer.isVyper(currentContract):
                            mapPositionHex = key[0:64]
                            self.calldataStack[-1]["preimage"][hashValue] = ("Vyper", mapPositionHex, key[64:])
                            # print("mapping storage position of Vyper = ", mapPositionHex)
                        else:
                            mapPositionHex = key[64:]
                            self.calldataStack[-1]["preimage"][hashValue] = ("Solc", mapPositionHex, key[:64])
                            # print("mapping storage position of Solidity = ", mapPositionHex)
                        
                        # convert mapping storage position to storage slot
                        mapPosition = int(mapPositionHex, 16) * 32 # 32 bytes per slot
                        if mapPosition not in storageMappingMap[currentContract] \
                            and "0x" + mapPositionHex not in self.calldataStack[-1]["preimage"]:
                            sys.exit("Error! mapPosition {} not in storageMappingMap".format(mapPositionHex) + " and not in preimage")


                elif len(key) == 64:
                    # dynamic array
                    # slot = arraySlot + keccak256(key)
                    self.printIndentContentLogging("SHA3[mem[{0}: {0} + {1}]] for dynamic array".format(offset, length))
                    self.printIndentContentLogging("SHA3({0}) = {1}".format(key, hashValue))

                    if self.logging > 0:
                        currentContract = self.contractAddressStack[-1]
                        if self.analyzer.isVyper(currentContract):
                            self.calldataStack[-1]["preimage"][hashValue] = ("Vyper", key)
                        else:
                            self.calldataStack[-1]["preimage"][hashValue] = ("Solc", key)

                        if currentContract not in storageMappingMap:
                            sys.exit("Error! currentContract not in storageMappingMap")


            elif structLogs[ii]["op"] == "KECCAK256":
                sys.exit("Error! KECCAK256 is not supported")

            # check if msg.value == 0 if the function is non-payable
            if ii + 7 < len(structLogs) and \
                structLogs[ii]["op"] == "PUSH1" and \
                structLogs[ii + 1]["op"] == "PUSH1" and \
                structLogs[ii + 2]["op"] == "MSTORE" and \
                structLogs[ii + 3]["op"] == "CALLVALUE" and \
                structLogs[ii + 4]["op"] == "DUP1" and \
                structLogs[ii + 5]["op"] == "ISZERO" and \
                structLogs[ii + 6]["op"] == "PUSH2" and \
                structLogs[ii + 7]["op"] == "JUMPI":

                ii = ii + 7
                continue


            # truncate the calldata size to get function selector
            if ii + 3 < len(structLogs) and \
                structLogs[ii]["op"] == "PUSH1" and \
                structLogs[ii + 1]["op"] == "CALLDATALOAD" and \
                structLogs[ii + 2]["op"] == "PUSH1" and \
                structLogs[ii + 3]["op"] == "SHR" and \
                len(structLogs[ii + 3]["stack"]) >= 1 and \
                structLogs[ii + 3]["stack"][-1] == "0xe0":

                ii = ii + 3
                continue

                
            # function selector comparison succeeds for Solidity
            if ii + 4 < len(structLogs) and \
                structLogs[ii]["op"] == "DUP1" and \
                structLogs[ii + 1]["op"] == "PUSH4" and \
                structLogs[ii + 2]["op"] == "EQ" and \
                structLogs[ii + 3]["op"] == "PUSH2" and \
                structLogs[ii + 4]["op"] == "JUMPI" and \
                structLogs[ii + 4]["stack"][-2] == "0x1" and \
                structLogs[ii + 5]["op"] == "JUMPDEST": # comparison succeeds

                funcSelector = structLogs[ii + 2]["stack"][-1]
                funcSelector = addLeadningZeroFuncSelector(funcSelector)

                self.printIndentContentLogging("Enter into function ", funcSelector)

                if self.logging > 0:
                    # print("self.logging", self.logging)
                    funcSigMap = funcSigMapMap[self.contractAddressStack[-1]]
                    # print("contract key, ", self.contractAddressStack[-1])
                    # print("funcSigMapMap keys", funcSigMapMap.keys())
                    self.printIndentContentLogging("Function name:", funcSigMap[funcSelector][0], " ||  Function Signature:", funcSigMap[funcSelector][1], funcSigMap[funcSelector][2])


            # function selector comparison succeeds for Vyper
            if ii + 4 < len(structLogs) and \
                structLogs[ii]["op"] == "PUSH4" and \
                structLogs[ii + 1]["op"] == "PUSH1" and \
                structLogs[ii + 2]["op"] == "MLOAD" and \
                structLogs[ii + 3]["op"] == "EQ" and \
                structLogs[ii + 4]["op"] == "ISZERO" and \
                structLogs[ii + 4]["stack"][-1] == "0x1" and \
                structLogs[ii + 5]["op"] == "PUSH2" and \
                structLogs[ii + 6]["op"] == "JUMPI": # comparison succeeds

                funcSelector = structLogs[ii + 3]["stack"][-1]
                funcSelector = addLeadningZeroFuncSelector(funcSelector)
                self.printIndentContentLogging("Enter into function ", funcSelector)

                if self.logging > 0:
                    # print("self.logging", self.logging)
                    funcSigMap = funcSigMapMap[self.contractAddressStack[-1]]
                    # print("contract key, ", self.contractAddressStack[-1])
                    # print("funcSigMapMap keys", funcSigMapMap.keys())
                    self.printIndentContentLogging("Function name:", funcSigMap[funcSelector][0], " ||  Function Signature:", funcSigMap[funcSelector][1], funcSigMap[funcSelector][2])

            # print sload
            if structLogs[ii]["op"] == "SLOAD":
                key = structLogs[ii]["stack"][-1]
                value = structLogs[ii + 1]["stack"][-1]
                # self.printIndentContentLogging("sload[{}] -> {}".format(key, value))

                # interpret the key
                # find answer from two places: 
                # 1. Preimage: self.calldataStack[-1]["preimage"]
                # eg. {hashValue: ("Vyper", mapPositionHex, key[64:])}
                # 2  StorageMapping: storageMappingMap[currentContract]
                # eg. "96": [
                #     "balanceOf",
                #     [
                #         "address",
                #         "uint256"
                #     ]
                # ]
                # 3. Transaction Variables:
                # eg. msg.sender, msg.value, tx.origin, gas, ...   No one will use gas as key to a map, right? ;)
                # should take a look at https://github.com/banteg/storage-layout to better understand the storage layout

                # goal: In the end, it should be in the form of 
                # Start from sth in storage Mapping, then calculate a function f(paras, msg.sender, msg.value, tx.origin) and get the index. 
                # Then, we can get the answer from the preimage. 

                # This is not trivial...

                # eg. sload[0xf7bb5e32e7dcc1b54124ab032e8d3728ddffa8e6f9fe66385a3ffce8c5cdc823] -> 0x0
                # several possibilities:
                # 1. key is in StorageMapping. Easiest case. 
                # 2. key is from nested mapping: a nested SHA3 call. Trace back preimage
                # 3. key is from nested dynamic array: trace how it is calculated.
                # 4. Most complicated case: key is calculated using paras. Symbolic execution is needed.
                

            # print sstore
            elif structLogs[ii]["op"] == "SSTORE":
                key = structLogs[ii]["stack"][-1]
                # value = structLogs[ii]["stack"][-2]
                # self.printIndentContentLogging("sstore[{}] = {}".format(key, value))

            # print calldatasize
            elif structLogs[ii]["op"] == "CALLDATASIZE":
                size = structLogs[ii + 1]["stack"][-1]
                self.printIndentContentLogging("msg.data.size -> {} bytes".format(size))
                if "calldatasize" not in self.calldataStack[-1]:
                    # if size == "0x24":
                    #     pass
                        # print("now it's the time")
                        # print(self.calldataStack)
                        # print("len:", len(self.calldataStack))
                        # print("len:", len(self.msgSenderStack))
                        # print("len:", len(self.isDelegateCallStack))
                        # print("len:", len(self.contractAddressStack))
                        # print("len:", len(self.funcSelectorStack))
                    self.calldataStack[-1]["calldatasize"] = size
                    

                elif self.calldataStack[-1]["calldatasize"] != size and self.calldataStack[-1]["calldatasize"] != -1:
                    print("self.calldataStack:")
                    for calldata in self.calldataStack:
                        print("calldatasize:", calldata["calldatasize"])
                    print("self.msgSenderStack:")
                    for msgSender in self.msgSenderStack:
                        print("msgSender:", msgSender)
                    print("self.isDelegateCallStack:", self.isDelegateCallStack)
                    print("self.contractAddressStack:")
                    for contractAddress in self.contractAddressStack:
                        print("contractAddress:", contractAddress)
                    print("self.funcSelectorStack:", self.funcSelectorStack)
                    print("len:", len(self.calldataStack))
                    print("len:", len(self.msgSenderStack))
                    print("len:", len(self.isDelegateCallStack))
                    print("len:", len(self.contractAddressStack))
                    print("len:", len(self.funcSelectorStack))
                    sys.exit("Error: calldatasize is changed, size = {} but self.calldataStack[-1][\"calldatasize\"] = {}".format(size, self.calldataStack[-1]["calldatasize"]))

            # print calldatacopy
            elif structLogs[ii]["op"] == "CALLDATACOPY":
                destOffset = structLogs[ii]["stack"][-1]
                offset = structLogs[ii]["stack"][-2]
                length = structLogs[ii]["stack"][-3]
                self.printIndentContentLogging("CALLDATACOPY: memory[{0}:{0}+{2}] = msg.data[{1}:{1}+{2}]".format(destOffset, offset, length))
                
            # print calldataload
            elif structLogs[ii]["op"] == "CALLDATALOAD":
                index = structLogs[ii]["stack"][-1]
                value = structLogs[ii + 1]["stack"][-1]
                
                # print("calldata[{}] -> {}".format(index, value))
                # self.printIndentContentLogging("calldata[{}] -> {}".format(index, value))
                

                oldCalldata = self.calldataStack[-1]["calldata"]
                calldataSizeInt = -1
                if "calldatasize" in self.calldataStack[-1]:
                    calldataSize = self.calldataStack[-1]["calldatasize"]
                    calldataSizeInt = int(calldataSize, 16)
                newCalldata = self.decoder.getCalldataHex(oldCalldata, calldataSizeInt, index, value)

                self.calldataStack[-1]["calldata"] = newCalldata
                
                
                # print("Old method: ", self.calldataStack[-1]["calldata"])
                # print("calldataSize", calldataSize)
                # print("New method: ", newCalldata)

                self.printIndentContentLogging("calldata[{}] -> {}".format(index, value))

            # print origin
            elif structLogs[ii]["op"] == "ORIGIN":
                origin = structLogs[ii + 1]["stack"][-1]
                self.printIndentContentLogging("origin -> {}".format(origin))
            
            # print caller
            elif structLogs[ii]["op"] == "CALLER":
                caller = structLogs[ii + 1]["stack"][-1]
                # remove 0x prefix, add zero paddings and then add 0x prefix back
                
                caller = "0x" + caller[2:].zfill(40)

                msgSender = self.msgSenderStack[-1]
                msgSender = "0x" + msgSender[2:].zfill(40)

                self.printIndentContentLogging("caller -> {}".format(caller))
                if caller != msgSender:
                    if len(self.msgSenderStack) != 1:
                        print("CALLER opcode returns {}, but msg.sender stack[-1] is {}".format(caller, self.msgSenderStack[-1]))
                        
                        print("len:", len(self.calldataStack))
                        print("len:", len(self.msgSenderStack))
                        print("len:", len(self.isDelegateCallStack))
                        print("len:", len(self.contractAddressStack))
                        print("len:", len(self.funcSelectorStack))

                        print("msgSenderStack: ", self.msgSenderStack)
                        print("contractAddressStack: ", self.contractAddressStack)
                        print("isDelegateCallStack: ", self.isDelegateCallStack)

                        sys.exit("Error! msg.sender is different from CALLER inside a Tx")

            # print callvalue
            elif structLogs[ii]["op"] == "CALLVALUE":
                callvalue = structLogs[ii + 1]["stack"][-1]
                self.printIndentContentLogging("callvalue -> {}".format(callvalue))

            # print selfbalance
            elif structLogs[ii]["op"] == "SELFBALANCE":
                selfbalance = structLogs[ii + 1]["stack"][-1]
                self.printIndentContentLogging("selfbalance -> {}".format(selfbalance))
            
            # print balance
            elif structLogs[ii]["op"] == "BALANCE":
                addr = structLogs[ii]["stack"][-1]
                balance = structLogs[ii + 1]["stack"][-1]
                self.printIndentContentLogging("balance[{}] -> {}".format(addr, balance))
            
            # print timestamp
            elif structLogs[ii]["op"] == "TIMESTAMP":
                timestamp = structLogs[ii + 1]["stack"][-1]
                self.printIndentContentLogging("timestamp -> {}".format(timestamp))

            # Test INVALID opcode
            elif structLogs[ii]["op"] == "INVALID":
                sys.exit("Error! INVALID opcode is detected")
        


        
        # print("msgSenderStack: ", self.msgSenderStack)
        # print("contractAddressStack: ", self.contractAddressStack)
        # print("isDelegateCallStack: ", self.isDelegateCallStack)


        if len(self.msgSenderStack) != 0 or len(self.contractAddressStack) != 0 \
            or len(self.isDelegateCallStack) != 0:
            print("msgSenderStack: ", self.msgSenderStack)
            print("contractAddressStack: ", self.contractAddressStack)
            print("isDelegateCallStack: ", self.isDelegateCallStack)
            sys.exit("Error! msgSenderStack, contractAddressStack, isDelegateCallStack should be empty at the end of a Tx")
        
        metaTraceTree.cleanStaticCall()
        metaTraceTree.hideUnnecessaryInfo()

        return metaTraceTree






def main():
    
    contractAddress = '0x5ade7aE8660293F2ebfcEfaba91d141d72d221e8'
    EminenceHackTx = "0x3503253131644dd9f52802d071de74e456570374d586ddd640159cf6fb9b8ad8"

    p = VmtraceParser()

    # jsonFile = SCRIPT_DIR + "/EMNHackFullTrace.json"
    # functionLogs = p.parseLogsJson(contractAddress, EminenceHackTx, jsonFile)
    # print(functionLogs)



    YearnContractAddress = "0xACd43E627e64355f1861cEC6d3a6688B31a6F952"
    YearnHackTx = "0xf6022012b73770e7e2177129e648980a82aab555f9ac88b8a9cda3ec44b30779"
    functions2protect = ["withdraw", "withdrawAll"]

    BuggyTx = "0xe5707912f018d7eb4e7dfda94281847a50192d914bd8c3f69c9c64c8486fc168"

    path = "./YearnHackTxFull.pickle.gz"
    trace = readCompressedJson(path)
    functionLogs = p.parseLogs(YearnContractAddress, YearnHackTx, trace, functions2protect)

    print(functionLogs)

    # jsonfile = functionLogs.to_json()
    # import pprint
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(jsonfile)



    # category = "FlashSyn"

    # problemTx = "0x7eedef5ef5babb778aa847f749fb222eaf68c8be7bbd2faae4bb77b9b24ef623"

    # print(p.parseLogsGzip(category, contractAddress, problemTx))








if __name__ == "__main__":


    # cProfile.run('main()', sort='cumtime')
    main()
