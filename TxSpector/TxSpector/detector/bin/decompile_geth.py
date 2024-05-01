#!/usr/bin/env python3.6

# BSD 3-Clause License
#
# Copyright (c) 2020, The Ohio State Univerisity. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard lib imports
import argparse
import logging
import sys
from os.path import abspath, dirname, join

# Prepend .. to $PATH so the project modules can be imported below
src_path = join(dirname(abspath(__file__)), "..")
sys.path.insert(0, src_path)

# Local project imports
import src.exporter as exporter
import src.tac_efg as tac_efg
import src.settings as settings




def analyzeTx(txHash):
    import json
    result_map = {}
    with open("result_map.json", "r") as f:
        result_map = json.load(f)

    if txHash in result_map:
        return result_map[txHash]


    infile = "example/{}.txt".format(txHash)
    output_dir = "example/facts"
    efg = None
    # Build TAC EFG from input file
    try:
        logging.info("Reading from '%s'.", infile)
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


    import os
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.dirname(SCRIPT_DIR)
    path2 = os.path.dirname(path1)
    sys.path.append(path1)
    sys.path.append(path2)

    from crawlPackage.crawlEtherscan import CrawlEtherscan
    ce = CrawlEtherscan()
    sc_addr = ce.Tx2SrcAddr(txHash)
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
    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/1Reentrancy.dl"
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


    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/2UncheckedCall.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from Step3.csv
    with open("Step3.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/3FailedSend.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from FailedSendResult.csv
    with open("FailedSendResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)


    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/4TimestampDependence.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from TimestampDependenceResult.csv
    with open("TimestampDependenceResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/5UnsecuredBalance.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from Step3.csv
    with open("Step3.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)


    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/6MisuseOfOrigin.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from MisuseOriginResult.csv
    with open("MisuseOriginResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)

    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/7Suicidal.dl"
    subprocess.run(souffle_command, shell=True, check=True)
    # read contents from SuicidalResult.csv
    with open("SuicidalResult.csv", "r") as f:
        content = f.read()
        if content:
            result.append(True)
        else:
            result.append(False)


    souffle_command = "souffle -j 16  -F example/facts ./detector/rules/8Securify-Reentrancy.dl"
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
    with open("result_map.json", "r") as f:
        result_map = json.load(f)

    if txHash not in result_map:
        result_map[txHash] = result
        with open("result_map.json", "w") as f:
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
    result_map = {}
    import glob
    # txt_files = glob.glob('example/*.txt')
    # print(txt_files)
    # for txt_file in txt_files:
    #     try:
    #         txHash = txt_file.split("/")[-1].split(".")[0]
    #         print("start analyzing tx: ", txHash)
    #         result = analyzeTx(txHash)
    #         result_map[txHash] = result
    #     except Exception as e:
    #         print(e)
    #         continue



    result = analyzeTx("0x3503253131644dd9f52802d071de74e456570374d586ddd640159cf6fb9b8ad8")
    # 0xab486012f21be741c9e674ffda227e30518e8a1e37a5f1d58d0b0d41f6e76530
    # 0x3503253131644dd9f52802d071de74e456570374d586ddd640159cf6fb9b8ad8
    # 0xa858463f30a08c6f3410ed456e59277fbe62ff14225754d2bb0b4f6a75fdc8ad
    # 0xcd314668aaa9bbfebaf1a0bd2b6553d01dd58899c508d4729fa7311dc5d33ad7
    result_vec = ["1Reentrancy", "2UncheckedCall", "3FailedSend", "4TimestampDependence", "5UnsecuredBalance", "6MisuseOfOrigin", "7Suicidal", "8Securify-Reentrancy-GasDepReen", "8Securify-Reentrancy-GasConstantReen"]

    print("The following vulnerabilities are found:")
    print(result_vec)
    print(result)

    for txHash in result_map:
        print(txHash)
        print(result_map[txHash])
