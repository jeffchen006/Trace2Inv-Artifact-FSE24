# TxSpector
TxSpector is the first generic logic-driven framework for uncovering attacks on Ethereum Blockchain from transactions.

## Revised Go-Ethereum
### Generate transaction trace by replaying transactions in the Ethereum Blockchain
To collect transaction trace, we revised the offcial [Go-Ethereum EVM](https://github.com/ethereum/go-ethereum) to record transaction info, such as its date, sender, reciver, and so on. To obtain all the transaction traces in Ethereum Blockchain, you can just replay all the transactions by syncing. For only one transaction, you can simulate the interaction with the geth client. The traces will be recorded in the MongoDB dataset named "geth" automatically.

## Revised files
*go-ethereum/mongo/mongodb.go initializes the mongodb and creates some global data, such as transaction related metadata. <br />
*go-ethereum/mongo/bashdb.go creates the struct Transac that is used to store the transaction related info, including the transaction trace. <br />
*go-ethereum/core/state_processor.go and core/state_transition.go deal with the logic that execute transactions. <br />
*go-ethereum/core/state_prefetcher.go and core/vm/evm.go are changed to remove the redundency casued by prefetching. <br />
*go-ethereum/core/vm/interpreter.go, in Run function, every opcode is executed and its related trace is recored into the dataset. <br />
*go-ethereum/core/vm/instructions.go, every opcode related function is changed to return the results that we need for the furture anlysis, which are the arguments of the opcode. <br />
*go-ethereum/core/vm/tx_pool.go stores the left transaction traces into the "geth" mongodb dataset. <br />

# Detector

## Requirements
Modules needed from python are put in the detector/requirements.txt. In addition, we need souffle. Other versions may also work.
```
souffle==1.5.1
```

## Analyze the transaction trace and detect attacks
With the traces being collected, TxSpector can parse the trace into the EFG (execution flow graph). Then the trace opcode based EFG is converted into the IR based EFG and the logic relations are exported afterwards. Specifically, logic relations represent the data and control dependencies of the transactions. An example is a transaction trace example stored in the directory example 0x37085f336b5d3e588e37674544678f8cb0fc092a6de5d83bd647e20e5232897b.txt, to generate facts/logic relations, the command should be as the following: <br />
```
./bin/analyze_geth.sh  trace_file  facts_dir
```
```
./detector/bin/analyze_geth.sh example/0x37085f336b5d3e588e37674544678f8cb0fc092a6de5d83bd647e20e5232897b.txt facts
```

Before detecting the attacks, we need to generate a facts "sc_addr.facts" by ourself, in which we only need to fill the receiver smart contract address. This facts file will be used to detect reentrancy attack. You can use the browser Etherscan [0x37085f336b5d3e588e37674544678f8cb0fc092a6de5d83bd647e20e5232897b](https://etherscan.io/tx/0x37085f336b5d3e588e37674544678f8cb0fc092a6de5d83bd647e20e5232897b) to obtain the info or use the go-ethereum to get the related info.



After the facts are generated, users can customize their detection rules to detect related attacks. We define some rules in the directory rules. An example is that with the generated facts, we can use the following command: <br />
```
souffle -F facts_dir detection_rule_file
```
```
souffle -F facts ./detector/rules/1Reentrancy.dl (detect reentrancy attack)
```

Now we have the final results in file ReenResult.csv that have some metadata for forensic analysis. <br />

## Files
* directory bin storess the files that are used to analyze. <br />
* directory rules stores the rules to detect the attacks, including reentrancy attack, unchecked call attack,  failed send attack, timestamp dependence attack and other similar opcodes dependency attack, unsecured balance attack, misuse of origin attack, sucidal attack, and securify based reentrancy attack. <br />
* directory src stores the code <br />
   src/opcode.py stores the opcodes of EVM <br />
   src/evm_efg.py parses the transaction trace and builds a trace-based EFG (Execution Flow Graph) <br />
   src/tac_efg.py generates a IR (Intermediate Representation) based EFG <br />
   src/exporter.py exports the needed facts <br />
   other files are helpers to analyze <br />



## Usage

1Reentrancy.dl  => ReenResult.csv

2UncheckedCall.dl => Step1.csv, Step2.csv, Step3.csv

3FailedSend.dl => FailedSendResult.csv

4TimestampDependence.dl => TimestampDependenceResult.csv

5UnsecuredBalance.dl => Situation1.csv

6MisuseOfOrigin.dl => MisuseOriginResult.csv

7Suicidal.dl => SuicidalResult.csv

8Securify-Reentrancy.dl  => 8Securify-Reentrancy.dl .csv / GasConstantReen.csv


179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137215

6465080288632887992935785017466142041404191740450231097049595941908663756058008002954484894227235016850239840191280456664183552414061888320434790749718200197151758369117136656398238073201602645534608690999005576107431060412895014698698579951235097826400417372931126123211128042247125007061588114874296665196116381868282817597016550943368878418472137143190076141545767133991730938137977222904073062749399035392185775851860000951790351041733654457243328659296361258953376911461437058545893121962231071280827838980274754543694518738747215045603281448148972411620013120618110485085703611163580344232935300309603613262608762325479780373272565001431976550239562555312795927290179041585775969444647594478272512





    # 1Reentrancy.dl
    # ==> ReenResult  yes
        # sload_loc: The location (bytecode position) of the SLOAD operation.
        # jumpi_loc: The location of the JUMPI operation that is conditionally dependent on the SLOAD operation.
        # sload_depth: The call depth at which the SLOAD operation occurs.
        # sload_call_number: The call number (sequence) associated with the SLOAD operation's execution context.
        # sstore_loc: The location of the SSTORE operation.
        # sstore_depth: The call depth at which the SSTORE operation occurs.
        # sstore_cn: The call number associated with the SSTORE operation's execution context.
        # sstore_sc_addr: The smart contract address associated with the `SSTORE
        # sload_sc_addr: The smart contract address associated with the SLOAD operation.


    # 2UncheckedCall.dl
    # ==> Step1
    # ==> Step2
    # ==> Step3   yes


    # 3FailedSend.dl
    # ==> FailedSendResult   yes


    # 4TimestampDependence.dl
    # ==> TimestampDependenceResult  yes


    # 5UnsecuredBalance.dl
    # ==> Situation1
    # ==> Step1
    # ==> Step3   yes

    # 6MisuseOfOrigin.dl
    # ==> Step1
    # ==> MisuseOriginResult  yes

    # 7Suicidal.dl
    # ==> Step1
    # ==> SuicidalResult    yes

    # 8Securify-Reentrancy.dl
    # ==> GasDepReen   yes
    # ==> GasConstantReen     yes
