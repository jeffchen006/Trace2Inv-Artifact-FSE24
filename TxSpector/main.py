import json
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from TxSpector.translator import *
from crawlPackage.crawlEtherscan import CrawlEtherscan
import subprocess
import signal
import time

FAILED = -1
SUCCESS = 0

print(SCRIPT_DIR)
# /home/zhiychen/Documents/TxGuard/TxSpector


def translate(category, interface, testTx):
    # step 3: translate one transaction
    trace_path = f'{SCRIPT_DIR}/../Benchmarks_Traces/{category}/Txs/{interface}/{testTx}.json.gz'
    kk = readCompressedJson(trace_path)    

    translated = None
    try:
        translated = TxSpectorTranslator().parseLogs(kk)
    except Exception as e:
        fe = fetcher()
        result_dict = fe.getTrace(testTx, FullTrace=False)
        writeCompressedJson(trace_path, result_dict)
        try:
            translated = TxSpectorTranslator().parseLogs(result_dict)
        except Exception as e:
            print(e)
            print("Failed to translate the transaction")
            error_file = f'{SCRIPT_DIR}/failedTranslate.txt'
            with open(error_file, 'a') as f:
                f.write(f'{category} {interface} {testTx}\n')
                return FAILED
    

    # store translated in a file
    infile = f'{SCRIPT_DIR}/translated.txt'
    with open(infile, 'w') as f:
        # write the translated transaction to the file
        f.write(translated)
    return SUCCESS



def executeTxSpector(category, interface, testTx):

    infile = f'{SCRIPT_DIR}/translated.txt'

    # step 4: execute the command
    ce = CrawlEtherscan()
    sc_addr = ce.Tx2SrcAddr(testTx)

    # execute the following command
    # /usr/bin/python3 /home/zhiychen/Documents/TxGuard/TxSpector/TxSpector/detector/bin/new_decompile_geth.py testTx infile sc_addr
    command = f'/usr/bin/python3 {SCRIPT_DIR}/TxSpector/detector/bin/new_decompile_geth.py {testTx} {infile} {sc_addr}'
    print(command)

    # execute the command and read its output
    error = None
    output = None
    timeout = 60
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        output, error = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        # First, try to terminate gracefully
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        try:
            output, error = process.communicate(timeout=10)  # Give it a few seconds to terminate
        except subprocess.TimeoutExpired:
            # If it still hasn't terminated, force kill
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            output, error = process.communicate()
        print("Timeout after {} seconds".format(timeout))

        timeout_file = f'{SCRIPT_DIR}/failedTimeOut.json'
        timeout_map = None
        with open(timeout_file, "r") as f:
            timeout_map = json.load(f)
        if testTx not in timeout_map:
            timeout_map[testTx] = 1
            with open(timeout_file, "w") as f:
                json.dump(timeout_map, f)
        return FAILED

    print("output:", output)
    # print(output)
    # print(error)
    if "False" not in str(output):
        print("TxSpector failed to execute the command")
        print(error)
        error_file = f'{SCRIPT_DIR}/failedTxSpector.txt'
        with open(error_file, 'a') as f:
            f.write(f'{category} {interface} {testTx}\n')
        return FAILED
        
    return SUCCESS




def runAll():
    # step 1: read transactions
    # get all json files under /home/zhiychen/Documents/TxGuard/TxSpector/Trace2Inv-Benchmarks/benchmarks
    import glob
    benchmark_path = f'{SCRIPT_DIR}/Trace2Inv-Benchmarks/benchmarks/*.json'
    # print(benchmark_path)
    json_files = glob.glob(benchmark_path)

    # step 2: analyze all transactions
    for benchmark in [ json_files[1] ]:
        category = ""
        benchmarkName = ""
        exploitTx = ""
        interface = ""
        implementation = ""
        testingSet = []
        testTx = 0

        result_map_file = f"{SCRIPT_DIR}/TxSpector/new_result_map.json"
        import json
        result_map = {}
        with open(result_map_file, "r") as f:
            result_map = json.load(f)
        
        timeout_file = f'{SCRIPT_DIR}/failedTimeOut.json'
        timeout_map = {}
        with open(timeout_file, "r") as f:
            timeout_map = json.load(f)

        with open(benchmark, "r") as f:
            json_read = json.load(f)
            category = json_read['category']
            benchmarkName = json_read['benchmarkName']
            exploitTx = json_read['exploitTx']
            interface = json_read['interface']
            implementation = json_read['implementation']
            testingSet = json_read['testingSet']

            for ii, testTx in enumerate(testingSet):
                print("now processing: {}/{}".format(ii, len(testingSet)), testTx)
                if testTx in result_map:
                    print("Already processed")
                    continue
                
                if testTx in timeout_map:
                    print("Timeout in previous run")
                    continue

                if testTx == exploitTx:
                    continue

                status = translate(category, interface, testTx)
                if status == FAILED:
                    continue
                
                status = executeTxSpector(category, interface, testTx)
                if status == FAILED:
                    continue



def runone():
    category = "FlashSyn"
    interface = "0x85ca13d8496b2d22d6518faeb524911e096dd7e0"
    testTx = "0x6816996502df50d6c8b3ce59b782b232c86b3348da673b713360dd48a335bd36"
    translate(category, interface, testTx)
    status = executeTxSpector(category, interface, testTx)
    print(status)



if __name__ == "__main__":

    # runAll()
    runone()



