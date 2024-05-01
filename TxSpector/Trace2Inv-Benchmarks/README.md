# Trace2Inv-Benchmarks

This repo includes all benchmarks used in the paper "Dymisfying Invariant Effectiveness for Securing Smart Contracts" (https://sites.google.com/view/trace2inv/).

42 victim smart contracts from 27 hack incidents on Ethereum Blockchain are included. 



## How to read the benchmarks

Under `benchmarks/` folder, each benchmark is a file with the following structure:

- category: the source of the benchmark, e.g. "DeFiHackLabs" - the benchmarks was collected from DeFiHackLabs (https://github.com/SunWeb3Sec/DeFiHackLabs)

- benchmarkName: a unique name for the benchmark, which matches the name in the paper

- exploitTx: the earliest transaction we found that exploits the victim contracts. 

- interface: the victim contracts 

- implementation: if the interface contract is using a proxy-implementation pattern, the implementation contract is also included. Otherwise, the implementation contract is the same as the interface contract.

- trainingSet: in the paper, we use 70% of transaction history from deployment to exploitTx as training set. The training set is sorted by block number, from its first transaction to the cutoff(70%) transaction.

- testingSet: in the paper, we use 30% of transaction history from deployment to exploitTx as testing set. The testing set is sorted by block number, from the cutoff(70%) transaction to the exploitTx.

