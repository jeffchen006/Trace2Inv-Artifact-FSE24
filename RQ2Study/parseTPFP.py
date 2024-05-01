import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(SCRIPT_DIR) 

TPFPPath = SCRIPT_DIR + "/RQ2.txt"

lines = None
with open(TPFPPath, "r") as f:
    lines = f.readlines()

invariant2categoryMap = {
    # "invariant": {
    #   0: 0,
    #   1: 0,
    #              }
}

i = 0

separatorPlace = 0
separator = "============================================================================"

for ii, line in enumerate(lines):
    if separator in line:
        separatorPlace = ii
        break


while i < len(lines):
    if "FPs:" in lines[i]:
        break

    if i >= separatorPlace:
        break

    benchmark = None
    if lines[i+1].startswith("0x"):
        benchmark = lines[i].strip()
        # print("benchmark {}".format(benchmark))


    if "protected by:" in lines[i]:
        i += 1
        while i < len(lines):

            if separator in lines[i]:
                break
            invariant = None
            category = None

            if "\t" in lines[i]:
                invariant = lines[i].strip()
            i += 1
            if "\t" in lines[i]:
                category = lines[i].strip()[0]
                # if category is not a number
                if not category.isdigit():
                    sys.exit("category is not a number")
            i += 1
            if invariant not in invariant2categoryMap:
                invariant2categoryMap[invariant] = {}

            if category is not None and int(category) > 6:
                sys.exit("category is larger than 6")
            # if invariant == "tokenOutRatioUpperBound":
            #     print("count line {}".format(i))
            if category not in invariant2categoryMap[invariant]:
                invariant2categoryMap[invariant][category] = 1
            else:
                invariant2categoryMap[invariant][category] += 1

            if "protected by:" in lines[i] or "FPs:" in lines[i]:
                break


    else:
        i += 1
        if separator in lines[i]:
            separatorPlace = i
            break
        if "FPs:" in lines[i]:
            separatorPlace = i - 2
            break

invariantList = [
    "require(origin==sender)", "isSenderOwner", "isSenderManager", "isOriginOwner", "isOriginManager", \
    'same sender block', 'same origin block', 'enforced short same function gap',
    'require(gasStart <= constant)', 'require(gasStart - gasEnd <= constant)',
    'MoveNonReentrantLocks', 
    'oracle range', 'oracle deviation',
    'totalSupply', 'totalBorrow',
    'tokenInUpperBound', 'tokenOutUpperBound', 'tokenInRatioUpperBound', 'tokenOutRatioUpperBound', \
    'mapping', 'callvalue', 'dataFlow upper bound', 'dataFlow lower bound',
]


# for key in invariantList:
#     if key in invariant2categoryMap:
#         print(key)
#         print(invariant2categoryMap[key])


table = [[],[],[],[],[]]
maxLen = 0
for invariant in invariantList:
    categoryMap = invariant2categoryMap[invariant]

    maxLen = 0
    for numStr in categoryMap:
        num = int(numStr) - 1
        table[num].append(categoryMap[numStr])
        maxLen = len(table[num])

    for ii in table:
        if len(ii) < maxLen:
            ii.append(0)
    
# for row in table:
#     for cell in row:
#         print(cell, end=",")

#     print("")


print("RQ2 summarize ")

table = [[],[],[],]
maxLen = 0
for invariant in invariantList:
    categoryMap = invariant2categoryMap[invariant]
    # format categoryMap
    new_categoryMap = {'1': 0, '2': 0, '3': 0}
    for numStr in categoryMap:
        if numStr == '1':
            new_categoryMap['1'] += categoryMap[numStr]
        elif numStr == '2':
            new_categoryMap['1'] += categoryMap[numStr]
        elif numStr == '3':
            new_categoryMap['3'] += categoryMap[numStr]
        elif numStr == '4':
            new_categoryMap['2'] += categoryMap[numStr]
        elif numStr == '5':
            new_categoryMap['3'] += categoryMap[numStr]

    maxLen = 0
    for numStr in new_categoryMap:
        num = int(numStr) - 1
        table[num].append(new_categoryMap[numStr])
        maxLen = len(table[num])

    for ii in table:
        if len(ii) < maxLen:
            ii.append(0)
    
for row in table:
    for cell in row:
        print(cell, end=",")

    print("")




output = {}
current_dict = {}
current_key = None

for ii, line in enumerate(lines):
    if ii < separatorPlace:
        continue
    line = line.strip()
    # Check if the line starts a new section
    if line.startswith("For "):
        current_key = line[4:]
        if current_key is not None:
            output[current_key] = {}

    else:
        # Parse the data lines
        if line and "0x" not in line and  line[0].isdigit():
            category  = int(line[0])

            if category not in output[current_key]:
                output[current_key][category] = 1
            else:
                output[current_key][category] += 1

print("==================================================================")



invariantList2 = [
    "require(origin==sender)", "isSenderOwner", "isSenderManager", "isOriginOwner", "isOriginManager", \
    'checkSameSenderBlock', 'checkSameOriginBlock', 'SameFuncGap', \
    'require(gasStart <= constant)', 'require(gasStart - gasEnd <= constant)', \
    'NonReentrantLocks', \
    'oracle', 'oracle-ratio', \
    'totalSupply', 'totalBorrow', \
    'tokenInUpperBound', 'tokenOutUpperBound', 'tokenInRatioUpperBound', 'tokenOutRatioUpperBound', \
    'mapping', 'callvalue', 'dataFlowUpperBound', 'dataFlowLowerBound',
]


table = [[],[],[],]

for key in invariantList2:
    # print(key)
    # print(output[key])

    if len(output[key]) == 0:
        for ii in table:
            ii.append(0)
        continue

    maxLen = 0
    for numStr in output[key]:
        num = int(numStr) - 1
        table[num].append(output[key][numStr])
        maxLen = len(table[num])

    for ii in table:
        if len(ii) < maxLen:
            ii.append(0)
    
for row in table:
    for cell in row:
        print(cell, end=",")

    print("")