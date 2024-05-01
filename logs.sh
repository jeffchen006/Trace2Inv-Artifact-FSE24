#!/bin/bash

python3.10 main.py AC | tee RQ1RQ3Results/AccessControl.txt  

python3.10 main.py TL | tee RQ1RQ3Results/TimeLocks.txt  

python3.10 main.py GC | tee RQ1RQ3Results/GasControl.txt

python3.10 main.py RE | tee RQ1RQ3Results/ReEntrancy.txt

python3.10 main.py SS | tee RQ1RQ3Results/SpecialStorage.txt

python3.10 main.py OR | tee RQ1RQ3Results/Oracle.txt 

python3.10 main.py DF | tee RQ1RQ3Results/DataFlow.txt  

python3.10 main.py MF | tee RQ1RQ3Results/MoneyFlow.txt 

python3.10 RQ1RQ3Results/parse.py | tee RQ1RQ3Results/RQ1RQ3-Results.txt
python3.10 RQ2Study/parseTPFP.py | tee RQ2Study/RQ2-Results.txt
python3.10 RQ4Results/readGas.py | tee RQ4Results/RQ4-Results.txt
