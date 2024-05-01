import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import json


def dict2TraceTree(dict):
    return TraceTree().from_dict(dict)


class TraceTree:
    def __init__(self, info: dict = {}) -> None:
        self.info = info
        self.internalCalls = []

    def __str__(self) -> str:
        # print both info and internalCalls
        return self.visualize()

    def visualize(self, indent=0):
        returnStr = ""
        returnStr += (' ' * indent + str(self.info) + "\n")
        for child in self.internalCalls:
            returnStr += child.visualize(indent + 2)
        return returnStr


    # eg. 'info': {'type': 'call', 'structLogsStart': 889505, 
    #               'gas': 919945, 'addr': '0x6b175474e89094c44da98b954eedeac495271d0f', 
    #               'msg.value': '0x0', 'msg.sender': '0x9c211bfa6dc329c5e757a223fb72f5481d676dc1', 
    #               'retOffset': '0x8d8', 'retLength': '0x0', 'structLogsEnd': 889829},
    #     'internalCalls': []}

    def from_dict(self, dict):
        self.info = dict['info']
        self.internalCalls = [TraceTree().from_dict(child) for child in dict['internalCalls']]
        return self
    
    def to_dict(self):
        children = [child.to_dict() for child in self.internalCalls]
        return {"info": self.info, "internalCalls": children}
    
    def to_json(self):
        # convert a TraceTree to json
        # this json is used for visualization  
        json_str = json.dumps(self.to_dict())
        return json_str

    def updateInfo(self, dict, depth = 0, allowOverwrite = False):
        if depth == 0:
            if not allowOverwrite:
                for key in dict.keys():
                    if key in self.info and self.info[key] != dict[key]:
                        sys.exit("TraceTree: Warning: key {} is overwritten".format(key))
            if "meta" in self.info:
                print("now is the time")
                print(dict)
            self.info.update(dict)
        elif depth == 1:
            self.internalCalls[-1].updateInfo(dict)
        else:
            self.internalCalls[-1].updateInfo(dict, depth - 1)

    def updateInfoList(self, key, value, depth = 0):
        if depth == 0:
            # if "meta" in self.info:
            #     print("now is the time")
            #     print(dict)
            if key not in self.info:
                self.info[key] = [value]
            else:
                self.info[key].append(value)
        elif depth == 1:
            self.internalCalls[-1].updateInfoList(key, value)
        else:
            self.internalCalls[-1].updateInfoList(key, value, depth - 1)


    def addInternalCall(self, newTraceTree, depth = 0):
        if depth == 0:
            # if depth is 0,
            # we should update self.info rather than add an internal call
            sys.exit("TraceTree: Depth cannot be 0")
        elif depth == 1:
            if newTraceTree.info['type'] == 'delegatecall' and \
                'msg.value' not in newTraceTree.info and 'msg.value' in self.info:
                newTraceTree.info['msg.value'] = self.info['msg.value']
                
            self.internalCalls.append(newTraceTree)
        else:
            self.internalCalls[-1].addInternalCall(newTraceTree, depth - 1)



    def splitTraceTree(self, contractAddress, proxyAddress = None): 
        """Given a contract, split the original trace tree into multiple trace tree"""
        splittedTraceTrees = []
        # print(self.info)
        if "meta" not in self.info and self.info['addr'].lower() == contractAddress.lower():
            if proxyAddress is None or 'type' not in self.info or self.info['type'] != 'delegatecall':

                splittedTraceTrees += [self]
                # if contractAddress.lower() == "0x85ca13d8496b2d22d6518faeb524911e096dd7e0":
                #     splittedTraceTrees += [self]
                # else:
                #     return [self]
            else:
                if self.info['proxy'].lower() == proxyAddress.lower():
                    splittedTraceTrees += [self]

                    # if contractAddress.lower() == "0x85ca13d8496b2d22d6518faeb524911e096dd7e0": 
                    #     splittedTraceTrees += [self]
                    # else:
                    #     return [self]
        for child in self.internalCalls:
            splittedTraceTrees += child.splitTraceTree(contractAddress, proxyAddress)
        return splittedTraceTrees

    def cleanStaticCall(self):
        # clean all staticcalls since they don't change storage
        # clean all enteries with 'type' == 'staticcall' in internalCalls
        self.internalCalls = [child for child in self.internalCalls if child.info['type'] != 'staticcall']

    def hideUnnecessaryInfo(self):
        # hide all info except for funcSelector
        for child in self.internalCalls:
            #  remove keys 
            child.info.pop('structLogsStart')
            child.info.pop('structLogsEnd')
            child.info.pop('retOffset')
            child.info.pop('retLength')
            child.hideUnnecessaryInfo()



if __name__ == "__main__":
    # test funcCall
    traceTree1 = TraceTree({"funcSelector": "0x0"})
    traceTree2 = TraceTree({"funcSelector": "0x1"})
    traceTree3 = TraceTree({"funcSelector": "0x2"})
    traceTree4 = TraceTree({"funcSelector": "0x3"})
    traceTree5 = TraceTree({"funcSelector": "0x4"})


    traceTree1.addInternalCall(traceTree2, 1)
    traceTree1.addInternalCall(traceTree4, 2)
    traceTree1.addInternalCall(traceTree5, 2)
    traceTree1.addInternalCall(traceTree3, 1)
    traceTree1.addInternalCall(traceTree5, 2)
    traceTree1.updateInfo({"mean": "0x5"}, 1)
    traceTree1.updateInfo({"mea342n": "0x6"}, 0)

    

    print(traceTree1)
    

    
