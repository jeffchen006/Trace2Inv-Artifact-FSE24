# read all json files under benchmarks/ folder

import os
import json
import sys
import re
import csv

# read all json files under benchmarks/ folder
path = 'benchmarks/'
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))

array = []
array2 = []
array3 = []

interface_implementations = []

used_hack_contract_cases = dict()
used_hack_contract_names = dict()


count = 0
count2 = 0
for f in files:
    benchmark = json.load(open(f))
    array.append( [benchmark['benchmarkName'], len(benchmark['traningSet']), len(benchmark['testingSet']), len(benchmark['traningSet']) + len(benchmark['testingSet'] )]  )
    if benchmark['interface'] != benchmark['implementation']:
        array2.append(benchmark['benchmarkName'])
       
        count += 1
    else:
        array3.append(benchmark['benchmarkName'])
        interface_implementations.append(benchmark["interface"])
        interface_implementations.append(str(len(benchmark['traningSet']) + len(benchmark['testingSet']) + 1 ))
        interface_implementations.append(benchmark['exploitTx'])
        used_hack_contract_cases[benchmark["interface"]] = benchmark["exploitTx"]
        used_hack_contract_names[benchmark["interface"]] = os.path.basename(f)
        count2 += 1

# sort array by number of testingSet
array.sort(key=lambda x: x[1])

print("index (benchmark, trainingSet, testingSet size)")

for ii, a in enumerate(array):
    print(ii, a)

print("implementation == interface: ", count2)
print(array3)
print("\n".join(interface_implementations))

print("**"*10)
for key in array3:
    for benchmarkname, trainingSet, testingSet, total in array:
        if benchmarkname == key:
            print(benchmarkname, trainingSet, testingSet, total)
    

print("implementation != interface: ", count)
print(array2)


# print(os.listdir(invcon_result_dir))
import glob 
invcon_result_dir = "./result"
test_violations_file_list = glob.glob(os.path.join(invcon_result_dir, "*.test.violation.inv"))
print(test_violations_file_list)
count = 0 
results = []
hack_tx_results = []
addresses = []
success_hack_captured = set()
for item in test_violations_file_list:
    address = os.path.basename(item).split("-")[0]
    if address in used_hack_contract_cases:
        count += 1
        myresult = json.load(open(item))
        _result = []
        if len(myresult) == 0:
            print(item)
            continue
        for tx_hash in myresult:
            tx_test_result = myresult[tx_hash]
            tx_result = False
            for func in tx_test_result:
                has_violation = len(func["violated_invs"])>0
                tx_result = tx_result or has_violation
            _result.append(1 if tx_result else 0)
            if tx_hash.lower() == used_hack_contract_cases[address].lower():
                    hack_tx_results.append(1 if tx_result else 0)
                    if tx_result:
                        success_hack_captured.add(used_hack_contract_names[address])
        addresses.append(address)
        results.append(1-sum(_result)/len(_result))

print(hack_tx_results)
print(results)
print(addresses)
print([used_hack_contract_names[address] for address in addresses])

print(" ========================== Summary ==========================")
print("Captured Hacked Contract:", success_hack_captured)
print("True Positive:", sum(hack_tx_results), "out of total ", len(addresses), " benchmarks")
print("False Positive:", sum(results)/len(addresses))

inv_counts = []
for address in addresses:
    inv_result_file =  glob.glob(os.path.join(invcon_result_dir, address+ "*.training.inv.json"))
    inv_result = json.load(open(inv_result_file[0]))
    inv_count = sum([len(item["preconditions"]) + len(item["postconditions"]) if item["executionType"] == "TxType.NORMAL" else 0 for item in inv_result])
    inv_counts.append(inv_count)

print("average invariant number per contract:", sum(inv_counts)/len(inv_counts))