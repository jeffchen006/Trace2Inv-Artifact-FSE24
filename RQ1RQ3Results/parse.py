import re
import sys

import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import RQ1RQ3Results.logicExpression as logicExpression


def sample_n_elements(input_list, n):
    if len(input_list) < n:
        return input_list
    else:
        return random.sample(input_list, n)
    

def parse_tab_separated_string(input_str):
    # Split the string by tabs and remove any empty strings
    str_list = [x for x in input_str.strip().split("\t") if x]
    return str_list


def parse_input(input_data):
    lines = input_data.strip().split("\n")
    parsed_data = {}
    current_benchmark = None
    
    for ii, line in enumerate(lines):
        if "====== benchmark" in line:
            current_benchmark = line[17:-2]
            parsed_data[current_benchmark] = {'fpmap': [], 'conditions': []}
        
        if "FPMap:" in line:
            fpmap_values = lines[ii + 1]
            parsed_data[current_benchmark]['fpmap'] = parse_tab_separated_string(fpmap_values)
        
        if "Successfully stops the exploit using" in line:
            condition = line.split("using")[-1].strip()
            parsed_data[current_benchmark]['conditions'].append(condition)

        if 'sampled FPs for' in line:
            current_key = line.split('sampled FPs for ')[1]
            parsed_data[current_benchmark][current_key] = []
            for jj in range(ii + 1, len(lines)):
                if not lines[jj].startswith('0x'):
                    break
                parsed_data[current_benchmark][current_key].append(lines[jj].strip())
        
        if 'exploitTx:' in line:
            exploitTx = line.split('exploitTx: ')[1]
            parsed_data[current_benchmark]['exploitTx'] = exploitTx.strip()

    
    return parsed_data



SignatureMap = {
    # AccessControl
    'require(origin==sender)': 0,
    'isSenderOwner': 1,
    'isSenderManager': 2,
    'isOriginOwner': 3,
    'isOriginManager': 4,

    
    # TimeLocks
    'same sender block': 0, 
    'same origin block': 1, 
    'enforced short same function gap': 2,

    # Gas
    'require(gasStart <= constant)': 0,
    "require(gasStart - gasEnd <= constant)": 1,

    # Re-entrancy
    'MoveNonReentrantLocks': 0,

    # Oracle
    'oracle range': 0,
    'oracle deviation': 1,

    # SpecialStorage
    'totalSupply': 0,
    'totalBorrow': 1,

    # Data Flow
    'mapping': 0,
    'callvalue': 1,
    'dataFlow upper bound': 2,
    'dataFlow lower bound': 3,
    
    # MoneyFlow
    "tokenInUpperBound": 0,
    "tokenOutUpperBound": 1,
    "tokenInRatioUpperBound": 2,
    "tokenOutRatioUpperBound": 3,

}


AllFuncs = ["RoninNetwork", "HarmonyBridge", "Nomad", "PolyNetwork"] + \
            ["bZx2", "Warp", "Warp_interface", "CheeseBank_1", "CheeseBank_2", "CheeseBank_3", "InverseFi", \
                    "CreamFi1_1", "CreamFi1_2", "CreamFi2_1", "CreamFi2_2", "CreamFi2_3", "CreamFi2_4", \
                    "RariCapital1", "RariCapital2_1", "RariCapital2_2", "RariCapital2_3", \
                    "RariCapital2_4", "XCarnival"] + \
            ["Harvest1_fUSDT", "Harvest2_fUSDC", "ValueDeFi", "Yearn1", "Yearn1_interface", "VisorFi", \
                    "UmbrellaNetwork", "PickleFi"] + \
            ["Eminence", "Opyn", "IndexFi", "RevestFi", "RevestFi_interface", "DODO", "Punk_1", "Punk_2", \
                    "Punk_3", "BeanstalkFarms", "BeanstalkFarms_interface"]

TrainingTesting = {}



TrainingTesting = {'RoninNetwork': ('66742', '28603'), 'HarmonyBridge': ('22505', '9644'), 'Nomad': ('10942', '4688'), 'PolyNetwork': ('31157', '13352'), 'bZx2': ('498', '213'), 'Warp': ('104', '44'), 'Warp_interface': ('22', '9'), 'CheeseBank_1': ('431', '184'), 'CheeseBank_2': ('416', '177'), 'CheeseBank_3': ('390', '167'), 'InverseFi': ('5314', '2276'), 'CreamFi1_1': ('4', '1'), 'CreamFi1_2': ('40729', '17455'), 'CreamFi2_1': ('890', '380'), 'CreamFi2_2': ('629', '269'), 'CreamFi2_3': ('183', '78'), 'CreamFi2_4': ('69', '29'), 'RariCapital1': ('467', '200'), 'RariCapital2_1': ('430', '184'), 'RariCapital2_2': ('527', '225'), 'RariCapital2_3': ('283', '121'), 'RariCapital2_4': ('544', '232'), 'XCarnival': ('240', '102'), 'Harvest1_fUSDT': ('1436', '614'), 'Harvest2_fUSDC': ('1513', '648'), 'ValueDeFi': ('207', '88'), 'Yearn1': ('471', '201'), 'Yearn1_interface': ('18682', '8006'), 'VisorFi': ('1185', '507'), 'UmbrellaNetwork': ('42', '17'), 'PickleFi': ('3808', '1631'), 'Eminence': ('14413', '6176'), 'Opyn': ('47', '20'), 'IndexFi': ('14449', '6192'), 'RevestFi': ('1145', '490'), 'RevestFi_interface': ('1025', '438'), 'DODO': ('30', '12'), 'Punk_1': ('20', '8'), 'Punk_2': ('30', '12'), 'Punk_3': ('26', '11'), 'BeanstalkFarms': ('4050', '1735'), 'BeanstalkFarms_interface': ('215', '91')}



replaceHelpMap = {
    "enforced short same function gap": "SameFuncGap",
    "same sender block": "checkSameSenderBlock",
    "same origin block": "checkSameOriginBlock",
    "MoveNonReentrantLocks": "NonReentrantLocks", 
    "oracle range": "oracle", 
    "oracle deviation": "oracle-ratio",
    "dataFlow upper bound": "dataFlowUpperBound",
    "dataFlow lower bound": "dataFlowLowerBound",
}

na = "-"
vi = "\\xmark"
ne = "$\\emptyset$"

def explainReason(invariantClass, invariantIndex, benchmark): 
    '''Given an invariant and a benchmark, explain why there is no fata'''

    if invariantClass == "AccessControl":
        if invariantIndex == 0:
            return vi
        if "Punk" in benchmark or benchmark == "CreamFi1_1":
            return ne
        else:
            return vi
    elif invariantClass == "TimeLocks":
        if invariantIndex == 2:
            if benchmark == "CreamFi1_1":
                return ne
            else:
                return vi
        else:
            if benchmark == "Warp_interface" or "Punk" in benchmark or \
                benchmark == "BeanstalkFarms_interface":
                return na
            else:
                return vi
    elif invariantClass == "ReEntrancy":
        return na
    elif invariantClass == "Oracle":
        if benchmark == "bZx2":
            return ne
        else:
            return na
    elif invariantClass == "SpecialStorage":
        return na
    elif invariantClass == "DataFlow":
        if invariantIndex == 0 or invariantIndex == 1:
            return na
        elif invariantIndex == 2 or invariantIndex == 3:
            if benchmark == "BeanstalkFarms_interface" or benchmark == "RevestFi_interface" or \
                benchmark == "Warp_interface" or benchmark == "PolyNetwork":
                return na
            else:
                return ne
    elif invariantClass == "MoneyFlow":
        if benchmark == "BeanstalkFarms_interface" or benchmark == "RevestFi_interface" or \
                benchmark == "Warp_interface":
            return na
        elif benchmark == "CreamFi1_1" and benchmark == "Yearn1" and benchmark == "Opyn" and \
                benchmark == "RevestFi" and benchmark == "DODO": 
            return ne
        else:
            return na
    elif invariantClass == "GasControl":
        return ne

    sys.exit("Error: invariantClass {} invariantIndex {} benchmark {}".format(invariantClass, invariantIndex, benchmark))
    
        
        
    

def generate_output(parsed_data, isAccessControl = False):
    output_data = {}
    TPFPMap = {}
    for benchmark, data in parsed_data.items():
        output_data[benchmark] = []
        fpmap_values = data['fpmap']
        conditions = data['conditions']
        exploitTx = data['exploitTx'] if 'exploitTx' in data else None

        TPFPMap[benchmark] = {}

        TruePositive = False
        TruePositiveInvariants = []
        FalsePositiveMap = {}
        for i, value in enumerate(fpmap_values):
            if isAccessControl:
                if i >= 5: 
                    TrainingTesting[benchmark] = (fpmap_values[5], fpmap_values[6])
                    
            entry = str(value)
            for sig in SignatureMap:
                if sig in conditions and i == SignatureMap[sig]:
                    entry += "*"
                    TruePositiveInvariants.append(sig)
                    TruePositive = True

                if sig in conditions and replaceHelpMap.get(sig, sig) not in data:
                    sys.exit("Error: sig {} in conditions but not in data".format(sig))

                # even if it's not TP, we still need to analyze FP
                sig = replaceHelpMap.get(sig, sig)
                if sig in data:
                    FalsePositiveMap[sig] = data[sig]
                
            output_data[benchmark].append(entry)
        
        TPFPMap[benchmark]["TP"] = TruePositive
        TPFPMap[benchmark]["TPInvariants"] = TruePositiveInvariants
        TPFPMap[benchmark]["FPMap"] = FalsePositiveMap
        TPFPMap[benchmark]["exploitTx"] = exploitTx

    # print(TrainingTesting)
    return output_data, TPFPMap



        



def parse(path):
    with open(path, "r") as f:
        input_data = f.read()
    parsed_data = parse_input(input_data)
    output_data, TPFPMap = generate_output(parsed_data, "AccessControl" in path)

    # validate
    for benchmark in output_data:
        # check 1: check true positive
        count = 0
        for item in output_data[benchmark]:
            if "*" in item:
                count += 1
        count2 = len(TPFPMap[benchmark]["TPInvariants"])
        if count != count2:
            sys.exit("true positive count != count2")

        invariantClass = None
        if "AccessControl" in path:
            invariantClass = "AccessControl"
        elif "TimeLocks" in path:
            invariantClass = "TimeLocks"
        elif "GasControl" in path:
            invariantClass = "GasControl"
        elif "ReEntrancy" in path:
            invariantClass = "ReEntrancy"
        elif "Oracle" in path:
            invariantClass = "Oracle"
        elif "SpecialStorage" in path:
            invariantClass = "SpecialStorage"
        elif "DataFlow" in path:
            invariantClass = "DataFlow"
        elif "MoneyFlow" in path:
            invariantClass = "MoneyFlow"


        # check 2: check false positive
        count = 0
        resultVec = []
        for ii, item in enumerate(output_data[benchmark]):
            # remove star
            if "*" in item:
                item = item[:-1]
            if "AccessControl" == invariantClass:
                if ii > 4:
                    continue
                if item != "N/A" and item != "0":
                    resultVec.append( int(item) )
                    count += 1
            elif "Oracle"  == invariantClass:
                if ii > 1:
                    continue
                if item != "N/A" and item != "0":
                    resultVec.append( int(item) )
                    count += 1
            elif "SpecialStorage"  == invariantClass:
                if ii > 1:
                    continue
                if item != "N/A" and item != "0":
                    resultVec.append( int(item) )
                    count += 1
            elif "DataFlow"  == invariantClass:
                if ii > 3:
                    continue
                if item != "N/A" and item != "0":
                    resultVec.append( int(item) )
                    count += 1
                    
            else:
                if item != "N/A" and item != "0":
                    resultVec.append( int(item) )
                    count += 1

            if item == "N/A":
                reason = explainReason(invariantClass, ii, benchmark)
                output_data[benchmark][ii] = reason
               

        count2 = 0
        result2Vec = []
        for item in TPFPMap[benchmark]["FPMap"]:
            if TPFPMap[benchmark]["FPMap"][item] != []:
                result2Vec.append( len(TPFPMap[benchmark]["FPMap"][item]) )
                count2 += 1

        if count != count2:
            sys.exit("non-zero false positive count != count2")

        if len(resultVec) != len(result2Vec):
            sys.exit("len(resultVec) != len(result2Vec)")
        
        for ii in range(len(resultVec)):
            if result2Vec[ii] < 5 and result2Vec[ii] != resultVec[ii]:
                sys.exit("result2Vec[ii] < 5 and result2Vec[ii] != resultVec[ii]")
            if result2Vec[ii] == 5 and result2Vec[ii] < 5:
                sys.exit("result2Vec[ii] == 5 and result2Vec[ii] < 5")
    # printOutPutData(output_data)
    return output_data, TPFPMap


def get_column(data, column_index):
    return [row[column_index] for row in data]

def remove_after_last_underscore(s):
    last_underscore_index = s.rfind('_')
    if last_underscore_index == -1:  # No underscore found
        return s
    return s[:last_underscore_index]

def remove_stars(s):
    return s.replace('*', '')

def printList(aList):
    for item in aList:
        print("\t", item)


def processFPTP():

    # Read input data from a file
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(SCRIPT_DIR)
    directory = SCRIPT_DIR + "/"
    paths = ["AccessControl.txt", "TimeLocks.txt", "GasControl.txt", "ReEntrancy.txt", \
    "Oracle.txt", "SpecialStorage.txt", "DataFlow.txt", "MoneyFlow.txt"]

    AccessControlMap, AccessControlTPFPMap = parse(directory + paths[0])
    TimeLocksMap, TimeLockTPFPMap = parse(directory + paths[1])
    GasControlMap, GasControlTPFPMap = parse(directory + paths[2])
    ReEntrancyMap, ReEntrancyTPFPMap = parse(directory + paths[3])
    OracleMap, OracleTPFPMap = parse(directory + paths[4])
    SpecialStorageMap, SpecialStorageTPFPMap = parse(directory + paths[5])
    DataFlowMap, DataFlowTPFPMap = parse(directory + paths[6])
    MoneyFlowMap, MoneyFlowTPFPMap = parse(directory + paths[7])

    TPFPLogs = ""

    # pick up all true positives
    # and randomly select up to 10 false positives
    # for each invariant
    invariant2TPFP = {
        # isEOA: {
        #   "TP": [(benchmark, exploitTx), ...],
        #   "FP": [(benchmark, tx), ...]
        # }
    }
    benchmark2TP = {
        # benchmarkExploit: exploitTx
        # benchmark: [invariant, ...]
    }
    for benchmark in AccessControlMap:
        exploitTx = AccessControlTPFPMap[benchmark]["exploitTx"]
        # benchmark2TP[benchmark + "exploit"] = exploitTx
        benchmark2TP[benchmark] = []

        if benchmark in AccessControlTPFPMap:
            benchmark2TP[benchmark] += AccessControlTPFPMap[benchmark]["TPInvariants"]
            for item in AccessControlTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))
        if benchmark in TimeLockTPFPMap:
            benchmark2TP[benchmark] += TimeLockTPFPMap[benchmark]["TPInvariants"]
            for item in TimeLockTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))
        if benchmark in GasControlTPFPMap:
            benchmark2TP[benchmark] += GasControlTPFPMap[benchmark]["TPInvariants"]
            for item in GasControlTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))
        if benchmark in ReEntrancyTPFPMap:
            benchmark2TP[benchmark] += ReEntrancyTPFPMap[benchmark]["TPInvariants"]
            for item in ReEntrancyTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))
        if benchmark in OracleTPFPMap:
            benchmark2TP[benchmark] += OracleTPFPMap[benchmark]["TPInvariants"]
            for item in OracleTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))
        if benchmark in SpecialStorageTPFPMap:
            benchmark2TP[benchmark] += SpecialStorageTPFPMap[benchmark]["TPInvariants"]
            for item in SpecialStorageTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))
        if benchmark in DataFlowTPFPMap:
            benchmark2TP[benchmark] += DataFlowTPFPMap[benchmark]["TPInvariants"]
            for item in DataFlowTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))
        if benchmark in MoneyFlowTPFPMap:
            benchmark2TP[benchmark] += MoneyFlowTPFPMap[benchmark]["TPInvariants"]
            for item in MoneyFlowTPFPMap[benchmark]["TPInvariants"]:
                item = replaceHelpMap.get(item, item)
                if item not in invariant2TPFP:
                    invariant2TPFP[item] = {"TP": [(benchmark, exploitTx)], "FP": []}
                else:
                    invariant2TPFP[item]["TP"].append((benchmark, exploitTx))



    for benchmark in AccessControlMap:
        if benchmark in AccessControlTPFPMap:
            for item in AccessControlTPFPMap[benchmark]["FPMap"]:
                if AccessControlTPFPMap[benchmark]["FPMap"][item] != []:
                    for item2 in AccessControlTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))

        if benchmark in TimeLockTPFPMap:
            for item in TimeLockTPFPMap[benchmark]["FPMap"]:
                if TimeLockTPFPMap[benchmark]["FPMap"][item] != []:
                    for item2 in TimeLockTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))

        if benchmark in GasControlTPFPMap:
            for item in GasControlTPFPMap[benchmark]["FPMap"]:
                if GasControlTPFPMap[benchmark]["FPMap"][item] != []:
                    TPFPLogs += item + "\n"
                    for item2 in GasControlTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))
        
        if benchmark in ReEntrancyTPFPMap:
            for item in ReEntrancyTPFPMap[benchmark]["FPMap"]:
                if ReEntrancyTPFPMap[benchmark]["FPMap"][item] != []:
                    TPFPLogs += item + "\n"
                    for item2 in ReEntrancyTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))

        if benchmark in OracleTPFPMap:
            for item in OracleTPFPMap[benchmark]["FPMap"]:
                if OracleTPFPMap[benchmark]["FPMap"][item] != []:
                    for item2 in OracleTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))
        
        if benchmark in SpecialStorageTPFPMap:
            for item in SpecialStorageTPFPMap[benchmark]["FPMap"]:
                if SpecialStorageTPFPMap[benchmark]["FPMap"][item] != []:
                    for item2 in SpecialStorageTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))
        
        if benchmark in DataFlowTPFPMap:
            for item in DataFlowTPFPMap[benchmark]["FPMap"]:
                if DataFlowTPFPMap[benchmark]["FPMap"][item] != []:
                    for item2 in DataFlowTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))
        
        if benchmark in MoneyFlowTPFPMap:
            for item in MoneyFlowTPFPMap[benchmark]["FPMap"]:
                if MoneyFlowTPFPMap[benchmark]["FPMap"][item] != []:
                    for item2 in MoneyFlowTPFPMap[benchmark]["FPMap"][item]:
                        invariant2TPFP[item]["FP"].append((benchmark, item2))
        
    TPFPLogs = ""
    # for TP, let's start from benchmarks
    for benchmark in AccessControlMap:
        exploitTx = AccessControlTPFPMap[benchmark]["exploitTx"]
        TPFPLogs += benchmark + "\n"
        TPFPLogs += exploitTx + "\n"
        TPFPLogs += "protected by: \n"
        for item in benchmark2TP[benchmark]:
            TPFPLogs += "\t" + item + "\n\t\n"
        TPFPLogs += "\n\n"




    # for FP, let's start from invariants
    for invariant in invariant2TPFP:
        TPFPLogs += "For " + invariant + "\n"
        TPFPLogs += "FPs: \n"
        sampledFPs = sample_n_elements(invariant2TPFP[invariant]["FP"], 10)
        for item in sampledFPs:
            TPFPLogs += "\t" + item[0] + "\t" + item[1] + "\n" + "\t\n"
        TPFPLogs += "\n\n"
    
    with open(directory + "TPFPLogs.txt", "w") as f:
        f.write(TPFPLogs)
    return
        

def processTable():
    # Read input data from a file
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(SCRIPT_DIR)
    directory = SCRIPT_DIR + "/"
    paths = ["AccessControl.txt", "TimeLocks.txt", "GasControl.txt", "ReEntrancy.txt", \
    "Oracle.txt", "SpecialStorage.txt", "DataFlow.txt", "MoneyFlow.txt"]

    AccessControlMap, AccessControlTPFPMap = parse(directory + paths[0])
    TimeLocksMap, TimeLockTPFPMap = parse(directory + paths[1])
    GasControlMap, GasControlTPFPMap = parse(directory + paths[2])
    ReEntrancyMap, ReEntrancyTPFPMap = parse(directory + paths[3])
    OracleMap, OracleTPFPMap = parse(directory + paths[4])
    SpecialStorageMap, SpecialStorageTPFPMap = parse(directory + paths[5])
    DataFlowMap, DataFlowTPFPMap = parse(directory + paths[6])
    MoneyFlowMap, MoneyFlowTPFPMap = parse(directory + paths[7])


    RQ1Table = []
    for benchmark in TrainingTesting:
        row = [benchmark, TrainingTesting[benchmark][0], TrainingTesting[benchmark][1]]
        
        if benchmark in AccessControlMap and len(AccessControlMap[benchmark]) >= 5:
            row += AccessControlMap[benchmark][:5]
        else:
            for ii in range(5):
                row.append( explainReason("AccessControl", ii, benchmark) )
            

        if benchmark in TimeLocksMap and len(TimeLocksMap[benchmark]) >= 3:
            row += TimeLocksMap[benchmark][:3]
        else:
            for ii in range(3):
                row.append( explainReason("TimeLocks", ii, benchmark) )

        if benchmark in GasControlMap and len(GasControlMap[benchmark]) >= 2:
            row += GasControlMap[benchmark][:2]
        else:
            for ii in range(2):
                row.append( explainReason("GasControl", ii, benchmark) )
        
        if benchmark in ReEntrancyMap and len(ReEntrancyMap[benchmark]) >= 1:
            row += ReEntrancyMap[benchmark][:1]
        else:
            for ii in range(1):
                row.append( explainReason("ReEntrancy", ii, benchmark) )

        if benchmark in OracleMap and len(OracleMap[benchmark]) >= 2:
            row += OracleMap[benchmark][:2]
        else:
            for ii in range(2):
                row.append( explainReason("Oracle", ii, benchmark) )


        if benchmark in SpecialStorageMap and len(SpecialStorageMap[benchmark]) >= 2:
            row += SpecialStorageMap[benchmark][:2]
        else:
            for ii in range(2):
                row.append( explainReason("SpecialStorage", ii, benchmark) )

        if benchmark in DataFlowMap and len(DataFlowMap[benchmark]) >= 4:
            row += DataFlowMap[benchmark][:4]
        else:
            for ii in range(4):
                row.append( explainReason("DataFlow", ii, benchmark) )

        if benchmark in MoneyFlowMap and len(MoneyFlowMap[benchmark]) >= 4:
            row += MoneyFlowMap[benchmark][:4]
        else:
            for ii in range(4):
                row.append( explainReason("MoneyFlow", ii, benchmark) )

        RQ1Table.append(row)
    

    # print (RQ1Table)
    print("\n\n RQ1 Table")
    for row in RQ1Table:
        for item in row:
            print(item, end = ",")
        print("")



    def custom_round(number, x):
        rounded_number = round(number, x)
        str_number = str(rounded_number)
        str_number = str_number.rstrip('0').rstrip('.') if '.' in str_number else str_number
        return str_number

    # print ratio 
    print("\n\n Ratio Table")
    for row in RQ1Table:
        benchmarkName = row[0]
        print(benchmarkName, end = ",")
        trainingSet = int(row[1])
        testingSet = int(row[2])
        for ii in range(3, len(row)):
            # if no number in row[ii]
            isDigit = False
            for char in row[ii]:
                if char.isdigit():
                    isDigit = True
                    break
            if not isDigit:
                print(row[ii], end = ",")
                continue
             
            else:
                if "*" in row[ii]:
                    removed = remove_stars(row[ii])
                    ratio = int(removed) / testingSet * 100
                    ratio = custom_round(ratio, 1)
                    print(ratio, end = "*,")
                else:
                    ratio = int(row[ii]) / testingSet * 100
                    ratio = custom_round(ratio, 1)
                    print(ratio, end = ",")
        print("")


    inVariants = [
        'onlyEOA', 'isSenderOwner', 'isOriginOwner', 'isSenderManager', \
        'isOriginManager', 'SHA(sender,block)', 'SHA(origin,block)', \
        'lastUpdate', 'require(gasStart<=c)', \
        'require(gasStart-gasEnd<=c)', 'NonReentrantLocks','oracle 0.2', 'oracle deviation', \
        'totalsupply', 'totalborrow', \
        'MappingUpperBound', 'callValueUpperBound', 'dataFlowUpperBound', 'dataFlowLowerBound', \
        'tokenInCap', 'tokenOutCap', 'tokenInRatioCap', 'tokenOutRatioCap'
    ]

    # below is the summary information for an invariant
    # 1. Number of Contracts that the invariant is applied
    # 2. Number of Contracts that the invariant guard has protected
    # 3. Number of Hacks that the invariant guard has protected
    # 4. Average False Positive Rate Per Contract 


    SummaryTable = [
        [], [], [], []
    ]

    print("\n\n Summary Table")

    SelectedInvariants = {}
    SelectedInvariantsHacks = {}

    for ii in range(len(inVariants)):
        Applied = 0
        ContractProtected = []
        HackProtected = []
        FalsePositiveRate = []
        column = get_column(RQ1Table, ii + 3)
        if len(column) != len(TrainingTesting.keys()):
            print("len(column) != len(TrainingTesting.keys())")
            sys.exit(1)

        for jj in range(len(column)):
            benchmark = RQ1Table[jj][0]
            trainingSet = int(RQ1Table[jj][1])
            testingSet = int(RQ1Table[jj][2])

            if column[jj] != na and column[jj] != ne and column[jj] != vi:
                Applied += 1
                if "*" in column[jj]:
                    ContractProtected.append(benchmark)
                    hack = remove_after_last_underscore(benchmark)
                    if hack not in HackProtected:
                        HackProtected.append(hack)
                    removed = remove_stars(column[jj])
                    FalsePositiveRate.append(int(removed) / testingSet)
                else:
                    FalsePositiveRate.append(int(column[jj]) / testingSet)
        if len(FalsePositiveRate) != Applied:
            print("len(FalsePositiveRate) != Applied")
            sys.exit(1)
        if inVariants[ii] == "require(gasStart-gasEnd<=c)":
            print("require(gasStart-gasEnd<=c)")

        if inVariants[ii] == "onlyEOA" or inVariants[ii] == "SHA(origin,block)" or \
            inVariants[ii] == "require(gasStart-gasEnd<=c)" or inVariants[ii] == "dataFlowUpperBound":

            SelectedInvariants[inVariants[ii]] = ContractProtected
            SelectedInvariantsHacks[inVariants[ii]] = HackProtected

        
        # print("{} protected: ============================".format(inVariants[ii]))
        # print(ContractProtected)

        # # print("Applied: ", Applied)
        # # print("ContractProtected: ", ContractProtected)

        # print(" {} HackProtected: ".format(inVariants[ii]), HackProtected)
        # remove duplicates

        # print("FalsePositiveRate: ", sum(FalsePositiveRate) / len(FalsePositiveRate))
        # print("")

        NumContractProtected = len(ContractProtected)
        HackProtected = list(set(HackProtected))
        NumHackProtected = len(HackProtected)
        AverageFalsePositiveRate = sum(FalsePositiveRate) / len(FalsePositiveRate)

        # print(FalsePositiveRate)
    
        AverageFalsePositiveRate = AverageFalsePositiveRate * 100
        AverageFalsePositiveRate = round(AverageFalsePositiveRate, 1)

        SummaryTable[0].append(Applied)
        SummaryTable[1].append(NumContractProtected)
        SummaryTable[2].append(NumHackProtected)
        SummaryTable[3].append(AverageFalsePositiveRate)

        # print(Applied, end = " ")
        # print(NumContractProtected, end = " ")
        # print(NumHackProtected, end = " ")
        # print(AverageFalsePositiveRate, end = " ")
        # print("")


    for ii in range(len(inVariants)):
        print(inVariants[ii], end = " ")
    
    for ii in range(len(SummaryTable)):
        print("")
        for jj in range(len(SummaryTable[ii])):
            print(SummaryTable[ii][jj], end = " ")
    print("")



## process false positive and true positive
def combineInvariants():
    invariants = ["onlyEOA", "SHA(origin,block)", "require(gasStart-gasEnd<=c)", "dataFlowUpperBound"]
    # directory = "/home/zhiychen/Documents/TxGuard/constraintPackage/cache/positives/"
    directory = SCRIPT_DIR + "/../constraintPackage/cache/positives_reserved/"

    literals = []
    
    for invariant in invariants:
        invariantDirectory = None
        if invariant == "onlyEOA":
            invariantDirectory =  directory + "isEOA/"
        elif invariant == "SHA(origin,block)":
            invariantDirectory =  directory + "checkSameOriginBlock/"
        elif invariant == "require(gasStart-gasEnd<=c)":
            invariantDirectory =  directory + "gasConsumed/"
        elif invariant == "dataFlowUpperBound":
            invariantDirectory =  directory + "dataFlowUpperBound/"
        # print("invariantDirectory", invariantDirectory)

        TPMap = {}
        FPMap = {}
        numFPs = 0
        for key in TrainingTesting.keys():
            exploitTx = None
            TP = False
            FPs = []
            path = invariantDirectory + key + ".txt"
            if not os.path.exists(path):
                pass
            else:
                with open(path, "r") as f:
                    # read line by line
                    lines = f.readlines()
                    for line in lines:
                        if "exploitTx" in line:
                            exploitTx = line.split(" ")[1].strip()
                        else:
                            tx = line.strip()
                            if tx == exploitTx:
                                TP = True
                            elif tx not in FPs:
                                FPs.append(tx)
                # check FPs:
                numFPs += len(FPs)
                TPMap[key] = TP
                FPMap[key] = FPs

        # print("invariant: ", invariant, "gives ", numFPs, "FPs")


        newLiteral = logicExpression.Literal(invariant, TPMap, FPMap)
        # print("invariant: ", invariant)
        applied = 0
        appliedBenchmarks = []
        protected = 0
        protectedBenchmarks = []
        prevented = 0
        preventedHacks = []

        for key in TPMap:
            applied += 1
            appliedBenchmarks.append(key)
            if TPMap[key]:
                protected += 1
                protectedBenchmarks.append(key)
                # print("protected: ", key)

                hack = remove_after_last_underscore(key)
                if hack not in preventedHacks:
                    preventedHacks.append(hack)
                    prevented += 1

        # print("protected: ", protected, "\t", "prevented: ", prevented)
        # print("appliedBenchmarks: ", appliedBenchmarks)
        # print("protectedBenchmarks: ", protectedBenchmarks)
        # print("FPMap: ", FPMap)


        # next construct literal
        TP = []
        FP = []
        for key in TrainingTesting.keys():
            if key not in TPMap and key in FPMap:
                sys.exit("Error: key not in TPMap but in FPMap")
            if key in TPMap and key not in FPMap:
                sys.exit("Error: key not in FPMap but in TPMap")

            if key not in TPMap:
                TP.append(None)
                FP.append(None)
            else:
                TP.append(TPMap[key])
                FP.append(FPMap[key])
        newLiteral = logicExpression.Literal(invariant, TP, FP)
        literals.append(newLiteral)


    for literal in literals:
        if len(literal.TP) != 42 or len(literal.FP) != 42:
            sys.exit("Error: len(literal.TP) != 42 or len(literal.FP) != 42") 
        # print(literal)
        # print("")

    operators = ["∧", "v"]
    # Generate and print formulas

    highestPrevented = 0
    highestPreventedFormula = []
    highestPreventedHacks = []
    highestPreventedSampleFPs = []

    highestProtected = 0
    highestProtectedFormula = []

    highestPreventedUnder100 = 0
    highestPreventedUnder100Formula = []
    highestPreventedUnder100Hacks = []
    highestPreventedUnder100SampledFPs = []

    highestProtectedUnder100 = 0
    highestProtectedUnder100Formula = []


    isPrint = False


    for length in range(1, 4):  # Lengths from 1 to 4
        # print(f"Formulas of length {length}:")
        for formula in logicExpression.generate_formulas(literals, operators, length):
            if isPrint:
                print(formula)
            
            # if str(formula) == "(onlyEOA v (require(gasStart-gasEnd<=c) v dataFlowUpperBound))":
            #     print("now is the time")

            new_TP, new_FP = formula.evaluate()
            # find the number of Trues in new_TP
            count = 0
            for item in new_TP:
                if item:
                    count += 1
            
            if isPrint:
                print("TP: ", count, end = "\t")

            FPSum = 0
            FPCounter = 0
            totalFP = 0
            counter = -1
            hacksPrevented = 0
            hacksPreventedList = []
            FPs = []
            for key in TrainingTesting.keys():
                counter += 1

                if new_TP[counter]:
                    hack = remove_after_last_underscore( key )
                    if hack not in hacksPreventedList:
                        hacksPreventedList.append(hack)
                        hacksPrevented += 1

                testingSet = int(TrainingTesting[key][1])
                if new_FP[counter] is not None:
                    # print(len(new_FP[counter]) / testingSet)
                    totalFP += len(new_FP[counter])
                    FPSum += len(new_FP[counter]) / testingSet
                    FPCounter += 1
                    
                    sampled_new_FP = sample_n_elements(new_FP[counter], 10)
                    for FP in sampled_new_FP:
                        if FP not in FPs:
                            FPs.append( (key, FP) )

            FPAverage = FPSum / FPCounter

            if isPrint:
                # print("totalFP", totalFP)
                # print("prevented: ", hacksPrevented, end = "\t")
                print("FP: ", FPAverage * 100)

            # if length == 3:
            #     print(formula, end = "\t")
            #     print("prevented: ", hacksPrevented)
            #     print("FP: ", FPAverage * 100)
                # print("prevented list, ", hacksPreventedList)

            if hacksPrevented > highestPrevented:
                highestPrevented = hacksPrevented
                highestPreventedFormula = [ (formula, FPAverage * 100) ]
                highestPreventedHacks = [ hacksPreventedList ]
                highestPreventedSampleFPs = [ FPs ]
            elif hacksPrevented == highestPrevented:
                highestPreventedFormula.append( (formula, FPAverage * 100) )
                highestPreventedHacks.append( hacksPreventedList )
                highestPreventedSampleFPs.append( FPs )
            
            if count > highestProtected:
                highestProtected = count
                highestProtectedFormula = [ (formula, FPAverage * 100) ]
            elif count == highestProtected:
                highestProtectedFormula.append( (formula, FPAverage * 100) )

            if FPAverage * 100 <= 1:
                if hacksPrevented > highestPreventedUnder100:
                    highestPreventedUnder100 = hacksPrevented
                    highestPreventedUnder100Formula = [ (formula, FPAverage * 100) ]
                    highestPreventedUnder100Hacks = [ hacksPreventedList ]
                    highestPreventedUnder100SampledFPs = [ FPs ]

                elif hacksPrevented == highestPreventedUnder100:
                    highestPreventedUnder100Formula.append(  (formula, FPAverage * 100) )
                    highestPreventedUnder100Hacks.append( hacksPreventedList )
                    highestPreventedUnder100SampledFPs.append( FPs )

                if count > highestProtectedUnder100:
                    highestProtectedUnder100 = count
                    highestProtectedUnder100Formula = [ (formula, FPAverage * 100) ]
                elif count == highestProtectedUnder100:
                    highestProtectedUnder100Formula.append( (formula, FPAverage * 100) )
        if isPrint:
            print()

    print("========================================")
    print("highestPrevented: ", highestPrevented)
    for ii, formula in enumerate(highestPreventedFormula):
        print(formula)
        if ii == 0:
            print("hacks blocked ")
            print(highestPreventedHacks[ii])
            # sampled = sample_n_elements( highestPreventedSampleFPs[ii], 10 )
            # for sample in sampled:
            #     print(sample)

    # print("highestProtected: ", highestProtected)
    # for ii, formula in enumerate(highestProtectedFormula):
    #     print(formula)
    print("========================================")
    print("highestPreventedUnder100: ", highestPreventedUnder100)
    for ii, formula in enumerate(highestProtectedUnder100Formula):
        print(formula)
        if ii == 0:
            print("hacks blocked ")
            print(highestPreventedUnder100Hacks[ii])
            # sampled = sample_n_elements( highestPreventedUnder100SampledFPs[ii], 10 )
            # for sample in sampled:
            #     print(sample)


    # print("highestProtectedUnder100: ", highestProtectedUnder100)
    # for ii, formula in enumerate(highestProtectedUnder100Formula):
    #     print(formula)




def RQ1():
    # print results of RQ1
    processTable()

def RQ3():
    combineInvariants()


if __name__ == "__main__":

    
    # print a raw results of RQ2, later for further manual analysis
    # processFPTP()  
    print( "==========================================================================================" )
    print( "==========================================  RQ1 ==========================================" )
    print( "==========================================================================================" )

    RQ1()
    
    print( "==========================================================================================" )
    print( "==========================================  RQ3 ==========================================" )
    print( "==========================================================================================" )

    RQ3()

