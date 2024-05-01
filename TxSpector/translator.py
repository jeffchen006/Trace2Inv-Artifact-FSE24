# a general parser for vmtrace
import struct
import sys
import os
import time
import json
import gc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from parserPackage.decoder import decoder
from fetchPackage.fetchTrace import fetcher
from utilsPackage.compressor import writeCompressedJson, readCompressedJson


sys.set_int_max_str_digits(20000)


class TxSpectorTranslator:
    def __init__(self):
        self.decoder = decoder()


    def parseLogs(self, trace):
        structLogs = trace['structLogs']
        self.callReserved = {}
        # sometimes we need to rely on last return to determine this call's return value
        lastReturn = (0, 0)

        translated = ""
        ii = -1
        ii_handled = -1
        while ii < len(structLogs) - 1:
            ii += 1
            pc = structLogs[ii]["pc"]
            opcode = structLogs[ii]["op"]
            if opcode == "KECCAK256":
                opcode = "SHA3"

            if ii != 0 and ii != ii_handled:
                lastDepth = structLogs[ii-1]["depth"]
                depth = structLogs[ii]["depth"]
                if lastDepth > depth:
                    if depth in self.callReserved:
                        callResultHex = structLogs[ii]["stack"][-1]
                        callResult = int(callResultHex, 16)
                        toAdd, opcode, retOffset, retLength = self.callReserved[depth]

                        if opcode == "CALL" or opcode == "STATICCALL" or opcode == "CALLCODE" or opcode == "DELEGATECALL":
                            retValueHex = self.decoder.extractMemory(structLogs[ii]["memory"], retOffset, retLength)
                            retValue = 0
                            if retValueHex != "":
                                retValue = int(retValueHex, 16)
                            if retValue == 0 and lastReturn[0] == lastDepth and structLogs[ii-1]["op"] == "RETURN":
                                retValue = lastReturn[1]

                            toAdd = "{}{},{}\n".format(toAdd, callResult, retValue)
                            translated += toAdd
                            ii_handled = ii
                            # print("Use Reserved at pc = {}, ii = {}, lastDepth = {}, depth = {}, callResult = {}, retValue = {}".format(pc, ii, lastDepth, depth, callResult, retValue))
                            del self.callReserved[depth]
                            ii -= 1
                            continue
                        
                        elif opcode == "CREATE" or opcode == "CREATE2":
                            retValue = structLogs[ii]["stack"][-1]
                            toAdd = "{}{}\n".format(toAdd, retValue)
                            translated += toAdd
                            ii_handled = ii
                            # print("Use Reserved at pc = {}, ii = {}, lastDepth = {}, depth = {}, retValue = {}".format(pc, ii, lastDepth, depth, retValue))
                            del self.callReserved[depth]
                            ii -= 1
                            continue


                    else:
                        sys.exit("Error: depth mismatch, pc = {}, ii = {}, lastDepth = {}, depth = {}".format(pc, ii, lastDepth, depth))
            

            toAdd = "{};{};".format(pc, opcode)
            if  opcode == "ADD" or opcode == "MUL" or opcode == "SUB" or \
                opcode == "DIV" or opcode == "SDIV" or opcode == "MOD" or opcode == "SMOD" or \
                opcode == "ADDMOD" or opcode == "MULMOD" or opcode == "EXP" or opcode == "SIGNEXTEND" or \
                opcode == "LT" or opcode == "GT" or opcode == "SLT" or opcode == "SGT" or \
                opcode == "EQ" or opcode == "ISZERO" or opcode == "AND" or opcode == "OR" or \
                opcode == "XOR" or opcode == "NOT":
                pass# confirmed
            elif opcode == "BYTE":
                pass
            elif opcode == "SHL":
                pass
            elif opcode == "SHR":
                pass
            elif opcode == "SAR":
                pass
            elif opcode == "SHA3" or \
                    opcode == "ADDRESS" or opcode == "BALANCE" or opcode == "ORIGIN" or \
                    opcode == "CALLER" or opcode == "CALLVALUE" or opcode == "CALLDATALOAD" or \
                    opcode == "CALLDATASIZE" or opcode == "CODESIZE" or opcode == "GASPRICE" or opcode == "TXGASPRICE" or \
                    opcode == "EXTCODESIZE" or opcode == "RETURNDATASIZE" or opcode == "EXTCODEHASH" or \
                    opcode == "BLOCKHASH" or opcode == "COINBASE" or opcode == "TIMESTAMP" or \
                    opcode == "NUMBER" or opcode == "DIFFICULTY" or opcode == "GASLIMIT" or \
                    opcode == "CHAINID" or opcode == "SELFBALANCE" or opcode == "BASEFEE" or \
                    opcode == "MLOAD" or opcode == "SLOAD" or opcode == "PC" or \
                    opcode == "MSIZE" or opcode == "GAS":
                valueHex = structLogs[ii+1]["stack"][-1]
                value = int(valueHex, 16)
                toAdd += "{}".format(value)


            elif opcode == "CALLDATACOPY" or opcode == "CODECOPY" or opcode == "RETURNDATACOPY":
                structLog = structLogs[ii]
                nextStructLog = structLogs[ii+1]
                destOffset = structLog["stack"][-1]
                offset = structLog["stack"][-2]
                length = structLog["stack"][-3]
                destOffsetInt = int(destOffset, base = 16)
                offsetInt = int(offset, base = 16)
                lengthInt = int(length, base = 16)
                valueHex = self.decoder.extractMemory(nextStructLog["memory"], destOffset, length)
                value = 0
                if valueHex != "":
                    value = int(valueHex, 16)


                toAdd += "{}".format(value)

            elif opcode == "EXTCODECOPY":
                structLog = structLogs[ii]
                nextStructLog = structLogs[ii+1]
                address = structLog["stack"][-1]
                destOffset = structLog["stack"][-2]
                offset = structLog["stack"][-3]
                length = structLog["stack"][-4]
                destOffsetInt = int(destOffset, base = 16)
                offsetInt = int(offset, base = 16)
                lengthInt = int(length, base = 16)
                valueHex = self.decoder.extractMemory(nextStructLog["memory"], destOffset, length)
                value = 0
                if valueHex != "":
                    value = int(valueHex, 16)
                toAdd += "{}".format(value)
            
            elif opcode == "POP":
                pass# confirmed
            elif opcode == "MSTORE":
                pass # confirmed
            elif opcode == "MSTORE8":
                pass# confirmed
            elif opcode == "SSTORE":
                pass# confirmed
            elif opcode == "JUMP":
                pass# confirmed
            elif opcode == "JUMPI":
                pass# confirmed
            elif opcode == "JUMPDEST":
                pass# confirmed
            elif opcode.startswith("PUSH"): # PUSH0-PUSH32
                valueHex = structLogs[ii+1]["stack"][-1]
                value = int(valueHex, 16)
                toAdd += "{}".format(value)
            elif opcode.startswith("DUP"): # DUP1-DUP16
                pass # confirmed
            elif opcode.startswith("SWAP"):
                pass # confirmed
            elif opcode.startswith("LOG"):
                pass # confirmed

            elif opcode == "CREATE":
                structLog = structLogs[ii]
                nextStructLog = structLogs[ii+1]

                # valueHex = nextStructLog["stack"][-1]
                # offsetHex = nextStructLog["stack"][-2]
                # lengthHex = nextStructLog["stack"][-3]

                depth = structLog["depth"]
                nextDepth = nextStructLog["depth"]

                # print("Reserve create at depth {}: toAdd-{}".format(depth, toAdd))

                self.callReserved[depth] = (toAdd, opcode, None, None)
                continue

            elif opcode == "CREATE2":
                structLog = structLogs[ii]
                nextStructLog = structLogs[ii+1]

                # valueHex = nextStructLog["stack"][-1]
                # offsetHex = nextStructLog["stack"][-2]
                # lengthHex = nextStructLog["stack"][-3]

                depth = structLog["depth"]
                nextDepth = nextStructLog["depth"]

                # print("Reserve create2 at depth {}: toAdd-{}".format(depth, toAdd))

                self.callReserved[depth] = (toAdd, opcode, None, None)
                continue


            # Four call opcodes has a special type: 0,1, they need extra type
            # value_extra is used to store more arguments for call, callcode, delegatecall, staticcall
            # op.value is success flag, value_extra is the memory content.


            elif opcode == "CALL":
                structLog = structLogs[ii]
                nextStructLog = structLogs[ii+1]

                gas = structLog["stack"][-1]
                addr = structLog["stack"][-2]
                value = structLog["stack"][-3]
                argsOffset = structLog["stack"][-4]
                argsLength = structLog["stack"][-5]
                retOffset = structLog["stack"][-6]
                retLength = structLog["stack"][-7]

                depth = structLog["depth"]
                nextDepth = nextStructLog["depth"]
                # precompile
                if depth == nextDepth:
                    successValueHex = nextStructLog["stack"][-1]
                    successValue = int(successValueHex, 16)
                    retValueHex = self.decoder.extractMemory(nextStructLog["memory"], retOffset, retLength)
                    retValue = 0
                    if retValueHex != "":
                        retValue = int(retValueHex, 16)
                    toAdd += "{},{}".format(successValue, retValue)
                else:
                    # print("Reserve call at depth {}: toAdd-{}, retOffset-{}, retLength-{}".format(depth, toAdd, retOffset, retLength))
                    # if depth in self.callReserved:
                    #     print("Error: depth {} is already reserved".format(depth))
                    self.callReserved[depth] = (toAdd, opcode, retOffset, retLength)
                    continue
                    
            
            elif opcode == "CALLCODE":

                structLog = structLogs[ii]
                nextStructLog = structLogs[ii+1]

                gas = structLog["stack"][-1]
                addr = structLog["stack"][-2]
                value = structLog["stack"][-3]
                argsOffset = structLog["stack"][-4]
                argsLength = structLog["stack"][-5]
                retOffset = structLog["stack"][-6]
                retLength = structLog["stack"][-7]

                depth = structLog["depth"]
                nextDepth = nextStructLog["depth"]
                # precompile
                if depth == nextDepth:
                    successValueHex = nextStructLog["stack"][-1]
                    successValue = int(successValueHex, 16)
                    retValueHex = self.decoder.extractMemory(nextStructLog["memory"], retOffset, retLength)
                    retValue = 0
                    if retValueHex != "":
                        retValue = int(retValueHex, 16)
                    toAdd += "{},{}".format(successValue, retValue)
                else:
                    # print("Reserve call at depth {}: toAdd-{}, retOffset-{}, retLength-{}".format(depth, toAdd, retOffset, retLength))
                    # if depth in self.callReserved:
                    #     print("Error: depth {} is already reserved".format(depth))
                    self.callReserved[depth] = (toAdd, opcode, retOffset, retLength)
                    continue


            elif opcode == "STATICCALL" or opcode == "DELEGATECALL":
                structLog = structLogs[ii]
                nextStructLog = structLogs[ii+1]

                gas = structLog["stack"][-1]
                addr = structLog["stack"][-2]
                argsOffset = structLog["stack"][-3]
                argsLength = structLog["stack"][-4]
                retOffset = structLog["stack"][-5]
                retLength = structLog["stack"][-6]

                depth = structLog["depth"]
                nextDepth = nextStructLog["depth"]

                # precompile
                if depth == nextDepth:
                    successValueHex = nextStructLog["stack"][-1]
                    successValue = int(successValueHex, 16)
                    retValueHex = self.decoder.extractMemory(nextStructLog["memory"], retOffset, retLength)
                    retValue = 0
                    if retValueHex != "":
                        retValue = int(retValueHex, 16)
                    toAdd += "{},{}".format(successValue, retValue)
                else:
                    # print("Reserve call at depth {}: toAdd-{}, retOffset-{}, retLength-{}".format(depth, toAdd, retOffset, retLength))
                    # if depth in self.callReserved:
                    #     print("Error: depth {} is already reserved".format(depth))
                    self.callReserved[depth] = (toAdd, opcode, retOffset, retLength)
                    continue


            elif opcode == "STOP":
                pass # confirmed
            elif opcode == "RETURN" or opcode == "REVERT":
                offset = structLogs[ii]["stack"][-1]
                length = structLogs[ii]["stack"][-2]
                offsetInt = int(offset, 16)
                lengthInt = int(length, 16)

                valueHex = self.decoder.extractMemory(structLogs[ii]["memory"], offset, length)
                value = 0
                if valueHex != "":
                    value = int(valueHex, 16)

                toAdd += "{}".format(value)

                depth = structLogs[ii]["depth"]
                lastReturn = (depth, value)


            elif opcode == "SELFDESTRUCT":
                pass 
            else:
                sys.exit("Error: unknown opcode {}".format(opcode))
            translated += toAdd + "\n"

        return translated





def solve1benchmark(exploitTx, use_cache = True):

    fe = fetcher()

    # path = SCRIPT_DIR + '/../TxSpectorHelper/cache2/{}.json'.format(exploitTx)
    # if not (use_cache and os.path.exists(path)):
    #     result_dict = fe.getTrace(exploitTx, FullTrace=False)
    #     with open(path, 'w') as f:
    #         json.dump(result_dict, f, indent = 2)
        

    path = SCRIPT_DIR + '/../TxSpectorHelper/cache/{}.json.gz'.format(exploitTx)
    if not (use_cache and os.path.exists(path)):
        result_dict = fe.getTrace(exploitTx, FullTrace=False)
        # with open(path, 'w') as f:
        #     json.dump(result_dict, f, indent = 2)
        writeCompressedJson(path, result_dict)
            
    # print(path)
    # kk = None
    # with open(path, 'r') as f:
    #     kk = json.load(f)
    kk = readCompressedJson(path)
    translated = TxSpectorTranslator().parseLogs(kk)
    path = SCRIPT_DIR + '/../TxSpectorHelper/translated/{}.txt'.format(exploitTx)
    with open("{}.txt".format(exploitTx), "w") as f:
        f.write(translated)

    gc.collect()



if __name__ == "__main__":
    # # given a trace file, translate it to the 3-address format required by the TxSpector
    # HackTx = "0x37085f336b5d3e588e37674544678f8cb0fc092a6de5d83bd647e20e5232897b"
    # txspectorExample = None
    # # read from TxSpectorExample.json
    # with open("TxSpectorExample.json", "r") as f:
    #     txspectorExample = json.load(f)
    # # print(txspectorExample)
    # translated = TxSpectorTranslator().parseLogs(txspectorExample)
    # with open("TxSpectorExampleTranslated.txt", "w") as f:
    #     f.write(translated)

    # Eminence
    exploitTx = "0x3503253131644dd9f52802d071de74e456570374d586ddd640159cf6fb9b8ad8"
    solve1benchmark(exploitTx)

    # # Harvest1_fUSDT
    # exploitTx = "0x0fc6d2ca064fc841bc9b1c1fad1fbb97bcea5c9a1b2b66ef837f1227e06519a6"
    # solve1benchmark(exploitTx)

    # # Harvest2_fUSDC
    # exploitTx = "0x35f8d2f572fceaac9288e5d462117850ef2694786992a8c3f6d02612277b0877"
    # solve1benchmark(exploitTx)

    # # bZx2
    # exploitTx = "0x762881b07feb63c436dee38edd4ff1f7a74c33091e534af56c9f7d49b5ecac15"
    # solve1benchmark(exploitTx)

    # # Warp
    # exploitTx = '0x8bb8dc5c7c830bac85fa48acad2505e9300a91c3ff239c9517d0cae33b595090'
    # solve1benchmark(exploitTx)

    # # CheeseBank_1
    # exploitTx = '0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc'
    # solve1benchmark(exploitTx)

    # # ValueDeFi
    # exploitTx = "0x46a03488247425f845e444b9c10b52ba3c14927c687d38287c0faddc7471150a"
    # solve1benchmark(exploitTx)
    # # InverseFi
    # exploitTx = '0x600373f67521324c8068cfd025f121a0843d57ec813411661b07edc5ff781842'
    # solve1benchmark(exploitTx)
    # # Yearn1
    # exploitTx = '0x59faab5a1911618064f1ffa1e4649d85c99cfd9f0d64dcebbc1af7d7630da98b'
    # solve1benchmark(exploitTx)

    # # Opyn
    # exploitTx = '0xa858463f30a08c6f3410ed456e59277fbe62ff14225754d2bb0b4f6a75fdc8ad'
    # solve1benchmark(exploitTx)
    # # CreamFi1_1
    # exploitTx = '0x0016745693d68d734faa408b94cdf2d6c95f511b50f47b03909dc599c1dd9ff6'
    # solve1benchmark(exploitTx)

    # # IndexFi
    # exploitTx = '0x44aad3b853866468161735496a5d9cc961ce5aa872924c5d78673076b1cd95aa'
    # solve1benchmark(exploitTx)

    # # CreamFi2_1
    # exploitTx = '0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92'
    # solve1benchmark(exploitTx)

    # # RariCapital1
    # exploitTx = '0x4764dc6ff19a64fc1b0e57e735661f64d97bc1c44e026317be8765358d0a7392'
    # solve1benchmark(exploitTx)
    # # VisorFi
    # exploitTx = '0x6eabef1bf310a1361041d97897c192581cd9870f6a39040cd24d7de2335b4546'
    # solve1benchmark(exploitTx)
    # # UmbrellaNetwork
    # exploitTx = '0x33479bcfbc792aa0f8103ab0d7a3784788b5b0e1467c81ffbed1b7682660b4fa'
    # solve1benchmark(exploitTx)
    # # RevestFi
    # exploitTx = '0xe0b0c2672b760bef4e2851e91c69c8c0ad135c6987bbf1f43f5846d89e691428'
    # solve1benchmark(exploitTx)

    # # RoninNetwork
    # exploitTx = '0xc28fad5e8d5e0ce6a2eaf67b6687be5d58113e16be590824d6cfa1a94467d0b7'
    # solve1benchmark(exploitTx)
    # # BeanstalkFarms
    # exploitTx = '0xcd314668aaa9bbfebaf1a0bd2b6553d01dd58899c508d4729fa7311dc5d33ad7'
    # solve1benchmark(exploitTx)

    # # HarmonyBridge
    # exploitTx = '0x27981c7289c372e601c9475e5b5466310be18ed10b59d1ac840145f6e7804c97'
    # solve1benchmark(exploitTx)
    # # XCarnival
    # exploitTx = '0x51cbfd46f21afb44da4fa971f220bd28a14530e1d5da5009cfbdfee012e57e35'
    # solve1benchmark(exploitTx)
    # # RariCapital2_1
    # exploitTx = '0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530'
    # solve1benchmark(exploitTx)

    # # DODO
    # exploitTx = '0x395675b56370a9f5fe8b32badfa80043f5291443bd6c8273900476880fb5221e'
    # solve1benchmark(exploitTx)
    # # PickleFi
    # exploitTx = '0xe72d4e7ba9b5af0cf2a8cfb1e30fd9f388df0ab3da79790be842bfbed11087b0'
    # solve1benchmark(exploitTx)

    # # Nomad
    # exploitTx = '0x61497a1a8a8659a06358e130ea590e1eed8956edbd99dbb2048cfb46850a8f17'
    # solve1benchmark(exploitTx)

    # # PolyNetwork
    # exploitTx = '0xad7a2c70c958fcd3effbf374d0acf3774a9257577625ae4c838e24b0de17602a'
    # solve1benchmark(exploitTx)

    # Punk_1
    # exploitTx = '0x597d11c05563611cb4ad4ed4c57ca53bbe3b7d3fefc37d1ef0724ad58904742b'
    # solve1benchmark(exploitTx)


# ================================================================================================================================================


    # # Warp_interface
    # exploitTx = '0x8bb8dc5c7c830bac85fa48acad2505e9300a91c3ff239c9517d0cae33b595090'
    # solve1benchmark(exploitTx)

    # # Warp_interface2
    # exploitTx = '0x8bb8dc5c7c830bac85fa48acad2505e9300a91c3ff239c9517d0cae33b595090'
    # solve1benchmark(exploitTx)


    # # CheeseBank_2
    # exploitTx = '0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc'
    # solve1benchmark(exploitTx)
    # # CheeseBank_3
    # exploitTx = '0x600a869aa3a259158310a233b815ff67ca41eab8961a49918c2031297a02f1cc'
    # solve1benchmark(exploitTx)


    # # Yearn1_interface
    # exploitTx = '0x59faab5a1911618064f1ffa1e4649d85c99cfd9f0d64dcebbc1af7d7630da98b'
    # solve1benchmark(exploitTx)



    # # CreamFi1_2
    # exploitTx = '0x0016745693d68d734faa408b94cdf2d6c95f511b50f47b03909dc599c1dd9ff6'
    # solve1benchmark(exploitTx)


    # # CreamFi2_2
    # exploitTx = '0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92'
    # solve1benchmark(exploitTx)
    # # CreamFi2_3
    # exploitTx = '0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92'
    # solve1benchmark(exploitTx)
    # # CreamFi2_4
    # exploitTx = '0x0fe2542079644e107cbf13690eb9c2c65963ccb79089ff96bfaf8dced2331c92'
    # solve1benchmark(exploitTx)



    # # RevestFi_interface
    # exploitTx = '0xe0b0c2672b760bef4e2851e91c69c8c0ad135c6987bbf1f43f5846d89e691428'
    # solve1benchmark(exploitTx)

    # # BeanstalkFarms_interface
    # exploitTx = '0xcd314668aaa9bbfebaf1a0bd2b6553d01dd58899c508d4729fa7311dc5d33ad7'
    # solve1benchmark(exploitTx)

    # # RariCapital2_2
    # exploitTx = '0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530'
    # solve1benchmark(exploitTx)
    # # RariCapital2_3
    # exploitTx = '0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530'
    # solve1benchmark(exploitTx)
    # # RariCapital2_4
    # exploitTx = '0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530'
    # solve1benchmark(exploitTx)

    # # Punk_2
    # exploitTx = '0x597d11c05563611cb4ad4ed4c57ca53bbe3b7d3fefc37d1ef0724ad58904742b'
    # solve1benchmark(exploitTx)


    # # Punk_3
    # exploitTx = '0x597d11c05563611cb4ad4ed4c57ca53bbe3b7d3fefc37d1ef0724ad58904742b'
    # solve1benchmark(exploitTx)












