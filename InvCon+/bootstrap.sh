#!/bin/bash
ROOT_DIR=$(git rev-parse --show-toplevel)

# For InvCon installation please refer to invcon repository: https://github.com/ntu-SRSLab/InvCon.git
cd $ROOT_DIR && cat Trace2Inv/benchmark_contract_addresses.txt | parallel -j 1 -N 3 python3 -m invconplus.main --address {1} --maxCount {2} --hack_tx {3} --minSupport 10 --training_ratio 0.7 --output_dir ./Trace2Inv/result 
