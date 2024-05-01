# Standard lib imports
import argparse
import logging
import sys
import os
from os.path import abspath, dirname, join

# Prepend .. to $PATH so the project modules can be imported below
src_path = join(dirname(abspath(__file__)), "..")
sys.path.insert(0, src_path)

# Local project imports
import src.exporter as exporter
import src.tac_efg as tac_efg
import src.settings as settings

dir_name = dirname(abspath(__file__))
TxSpector_dir = join(dir_name, "..", "..")
result_map_file = join(TxSpector_dir, "new_result_map.json")
# result_map_file = "/home/zhiychen/Documents/TxGuard/TxSpector/TxSpector/new_result_map.json"





def analyzeTx(txHash, infile, sc_addr):
    import json
    result_map = {}
    with open(result_map_file, "r") as f:
        result_map = json.load(f)
    if txHash in result_map:
        return result_map[txHash]


    # infile = "example/{}.txt".format(txHash)
    output_dir = join(TxSpector_dir, "example/facts")
    # output_dir = "/home/zhiychen/Documents/TxGuard/TxSpector/TxSpector/example/facts"
    efg = None
    # Build TAC EFG from input file
    try:
        lines = None
        with open(infile, 'r') as f:
            lines = f.readlines()
        efg = tac_efg.TACGraph.from_opcode(lines)
        logging.info("Initial EFG generation completed.")

    # Catch a Control-C and exit with UNIX failure status 1
    except KeyboardInterrupt:
        logging.critical("\nInterrupted by user")
        sys.exit(1)


    opcodes = [
        'CREATE', 'BALANCE', 'CALLER', 'CALLVALUE', 'STOP', \
        'RETURN', 'REVERT', 'ORIGIN', 'CALLDATALOAD', 'EQ', \
        'TIMESTAMP', 'NUMBER', 'DIFFICULTY', 'COINBASE', 'BLOCKHASH', \
        'GASLIMIT', 'EXTCODESIZE', 'SELFDESTRUCT', 'JUMPI', 'JUMP', \
        'JUMPDEST', 'SSTORE', 'SLOAD', 'CALL', 'DELEGATE', 'CALLCODE', 'STATICCALL'
    ]
    exporter.EFGTsvExporter(efg).export(output_dir=output_dir,
                                        out_opcodes=opcodes)


    # sc_addr = ce.Tx2SrcAddr(txHash)
    # store sc_addr in output_dir/.facts

    with open("{}/sc_addr.facts".format(output_dir), "w") as f:
        if txHash == "0xcd314668aaa9bbfebaf1a0bd2b6553d01dd58899c508d4729fa7311dc5d33ad7":
            f.write("0x728ad672409da288ca5b9aa85d1a55b803ba97d7\n")
        elif txHash == "0x3503253131644dd9f52802d071de74e456570374d586ddd640159cf6fb9b8ad8":
            f.write("0xe38684752ebe4c333c921800a8109bc97cd6fa3d\n")
        else:
            f.write(sc_addr)
            if not sc_addr.startswith("0x"):
                sys.exit(1)
            f.write("\n")

    result = []

    factsFolder = join(TxSpector_dir, "example/facts")
    # factsFolder = "/home/zhiychen/Documents/TxGuard/TxSpector/TxSpector/example/facts"

    detectorRuleFolder = join(TxSpector_dir, "detector/rules")
    # detectorRuleFolder = "/home/zhiychen/Documents/TxGuard/TxSpector/TxSpector/detector/rules"

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/1Reentrancy.dl"
    # run souffle command at root directory
    import subprocess
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from ReenResult.csv
    with open("ReenResult.csv", "r") as f:
        content = f.read()
        # if content is not empty, print yes
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/2UncheckedCall.dl"

    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from Step3.csv
    with open("Step3.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/3FailedSend.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from FailedSendResult.csv
    with open("FailedSendResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/4TimestampDependence.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from TimestampDependenceResult.csv
    with open("TimestampDependenceResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/5UnsecuredBalance.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from Step3.csv
    with open("Step3.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/6MisuseOfOrigin.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from MisuseOriginResult.csv
    with open("MisuseOriginResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/7Suicidal.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from SuicidalResult.csv
    with open("SuicidalResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = f"souffle -j 4  -F {factsFolder} {detectorRuleFolder}/8Securify-Reentrancy.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from GasDepReen.csv and GasConstantReen.csv
    with open("GasDepReen.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    with open("GasConstantReen.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    # load the file result_map.json which is a dictionary
    import json
    result_map = {}
    with open(result_map_file, "r") as f:
        result_map = json.load(f)

    if txHash not in result_map:
        result_map[txHash] = result
        with open(result_map_file, "w") as f:
            json.dump(result_map, f)


    # remove all .csv files
    os.remove("ReenResult.csv")
    os.remove("Step1.csv")
    os.remove("Step2.csv")
    os.remove("FailedSendResult.csv")
    os.remove("TimestampDependenceResult.csv")
    os.remove("Step3.csv")
    os.remove("MisuseOriginResult.csv")
    os.remove("SuicidalResult.csv")
    os.remove("GasDepReen.csv")
    os.remove("GasConstantReen.csv")
    os.remove("Situation1.csv")

    return result







if __name__ == "__main__":
    # read three command line arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument("txHash", help="transaction hash")
    # parser.add_argument("infile", help="input file")
    # parser.add_argument("sc_addr", help="contract address")
    # args = parser.parse_args()
    # txHash = args.txHash
    # infile = args.infile
    # sc_addr = args.sc_addr
    # result = analyzeTx(txHash, infile, sc_addr)
    # print(result)
    pass

    txHash = "0x6816996502df50d6c8b3ce59b782b232c86b3348da673b713360dd48a335bd36"
    infile = join(TxSpector_dir, "translated.txt")
    sc_addr = "0x77f973FCaF871459aa58cd81881Ce453759281bC"
    result = analyzeTx(txHash, infile, sc_addr)
    print(result)