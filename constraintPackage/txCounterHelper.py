import sys
import os
import random
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def sample_five_elements(input_list):
    if len(input_list) < 5:
        return input_list
    else:
        return random.sample(input_list, 5)
    
def sample_n_elements(input_list, n):
    if len(input_list) < n:
        return input_list
    else:
        return random.sample(input_list, n)

gasBenchmarks = ["HarmonyBridge", "Harvest1_fUSDT", "CreamFi2_1", "BeanstalkFarms"]

gasEOAOverhead = {
    "HarmonyBridge": 33,
    "Harvest1_fUSDT": 33,
    "CreamFi2_1": 33,
    "BeanstalkFarms": 92,
}

# For TSTORE and TLOAD (https://eips.ethereum.org/EIPS/eip-1153):
# TSTORE: 100 gas  TLOAD: 100 gas
# before:
# SSTORE: gas cost =  100 if warm access
#         gas cost = 

# SLOAD: gas cost = 100 if warm access
#        gas cost = 2100 if cold access
 

gasOBOverhead = {
    "HarmonyBridge": (20213 - 15000, 1025 - 500), # -10000 because using TSTORE to replace SSTORE
    "Harvest1_fUSDT": (20216 - 15000, 1028 - 500),
    "CreamFi2_1": (20213 - 15000, 1025 - 500),
    "BeanstalkFarms": (35594 - 18000, 1515 - 1200),
}



gasGCOverhead = {
    "HarmonyBridge": 43,
    "Harvest1_fUSDT": 40,
    "CreamFi2_1": 43,
    # "BeanstalkFarms": "N/A",
}

gasDFUOverhead = {
    "HarmonyBridge": 26,
    "Harvest1_fUSDT": 26,
    "CreamFi2_1": 26,
    "BeanstalkFarms": 104,
}

gasOBorDFUOverhead = {
    "HarmonyBridge": 1067,
    "Harvest1_fUSDT": 1070,
    "CreamFi2_1": 1067,
    "BeanstalkFarms": 1673,
}




# txCount 
thisMap = {
    "RoninNetwork": 99998,
    "HarmonyBridge": 40260,
    "HarmonyBridge_interface": 43418,
    "Nomad": 46954,
    "PolyNetwork": 54960,
    "bZx2": 780,
    "Warp": 266,
    "CheeseBank_1": 703,
    "CheeseBank_2": 694,
    "CheeseBank_3": 646,
    "InverseFi": 8380,
    "CreamFi1_1": 222,
    "CreamFi2_1": 63767,
    "CreamFi2_2": 42907,
    "CreamFi2_3": 18077,
    "CreamFi2_4": 212,
    "RariCapital1": 675,
    "RariCapital2_1": 693,
    "RariCapital2_2": 904,
    "RariCapital2_3": 471,
    "RariCapital2_4": 851,
    "XCarnival": 343,
    "Harvest1_fUSDT": 2094,
    "Harvest2_fUSDC": 2199,
    "ValueDeFi": 337,
    "Yearn1": 690,
    "VisorFi": 3282,
    "UmbrellaNetwork": 110,
    "PickleFi": 6040,
    "Eminence": 31259,
    "Opyn": 106,
    "IndexFi": 20942,
    "RevestFi": 1669,
    "DODO": 42,
    "Punk_1": 29,
    "Punk_2": 44,
    "Punk_3": 38,
    "BeanstalkFarms": 6309,
}


# two reasons why thisMapUpdated is smaller than thisMap:
# 1. some txs in thisMap get reverted
# 2. some txs in thisMap are done using old implementation instead of the new one
thisMapUpdated = { 
    "RoninNetwork": 95345,                    
    "HarmonyBridge": 32149,
    # "HarmonyBridge_interface": 41291,
    "Nomad": 15627,
    "PolyNetwork": 44509,
    "bZx2": 711,
    "Warp": 148,
    "Warp_interface": 31,
    "CheeseBank_1": 615,
    "CheeseBank_2": 593,
    "CheeseBank_3": 557,
    "InverseFi": 6562,
    "CreamFi1_1": 5,
    "CreamFi1_2": 58184,
    "CreamFi2_1": 1270,
    "CreamFi2_2": 898,
    "CreamFi2_3": 261,
    "CreamFi2_4": 98,
    "RariCapital1": 665,
    "RariCapital2_1": 614,
    "RariCapital2_2": 752,
    "RariCapital2_3": 404,
    "RariCapital2_4": 776,
    "XCarnival": 342,
    "Harvest1_fUSDT": 2050,
    "Harvest2_fUSDC": 2161,
    "ValueDeFi": 295,
    "Yearn1": 668,
    "Yearn1_interface": 26684,
    "VisorFi": 1693,
    "UmbrellaNetwork": 59,
    "PickleFi": 5439,
    "Eminence": 20589,
    "Opyn": 67,
    "IndexFi": 20641,
    "RevestFi": 1635,
    "RevestFi_interface": 1463,
    "DODO": 42,
    "Punk_1": 28,
    "Punk_2": 42,
    "Punk_3": 37,
    "BeanstalkFarms": 5785,
    "BeanstalkFarms_interface": 306,
}


# two lists:
# 1. users joins the protocol - deposit, stake, mint. 
#    Usually transfer tokens to the protocol

# 2. users leaves the protocol - withdraw, unstake, redeem, borrow. 
#    Usually transfer tokens out from the protocol

thatMap2 = {
    "RoninNetwork": [
            ['depositBulkFor', 'depositERC20', 'depositERC20For', 'depositERC721', 'depositERC721For', 'depositEth', 'depositEthFor'],
            ['withdrawERC20', 'withdrawERC20For', 'withdrawERC721', 'withdrawERC721For', 'withdrawToken', 'withdrawTokenFor'],
    ],
    "HarmonyBridge": [
            ["lockEth"],
            ["unlockEth"],
    ],
    # "HarmonyBridge_interface": [
    #         [],
    #         [],
    # ],
    "Nomad": [
            ["enrollCustom", "enrollRemoteRouter", "send"],
            ["handle"],
    ],
    "PolyNetwork": [
            ["lock"],
            ["unlock"],
    ],
    "bZx2": [
            ["mintWithEther", "mint"],
            ["burn", "burnToEther", "borrowTokenFromDeposit", "marginTradeFromDeposit"],
    ],
    "Warp": [
            ["repayBorrow", "_repayLiquidatedLoan", "lendToWarpVault"],
            ["_borrow", "redeem"],
    ],
    "Warp_interface": [
            [],
            [],
    ],
    "CheeseBank_1": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow", "_addReserves"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CheeseBank_2": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow", "_addReserves"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CheeseBank_3": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow", "_addReserves"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "InverseFi": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow", "_addReserves"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CreamFi1_1": [
            ["liquidateBorrow", "repayBorrowBehalf", "repayBorrow", "mint", "_addReserves", "gulp"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CreamFi1_2": [
            ["liquidateBorrow", "repayBorrowBehalf", "repayBorrow", "mint", "_addReserves", "gulp"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CreamFi2_1": [
            ["liquidateBorrow", "repayBorrowBehalf", "repayBorrow", "mint", "_addReserves", "gulp"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CreamFi2_2": [
            ["liquidateBorrow", "repayBorrowBehalf", "repayBorrow", "mint", "_addReserves", "gulp"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CreamFi2_3": [
            ["liquidateBorrow", "repayBorrowBehalf", "repayBorrow", "mint", "_addReserves", "gulp"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "CreamFi2_4": [
            ["liquidateBorrow", "repayBorrowBehalf", "repayBorrow", "mint", "_addReserves", "gulp"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves"],
    ],
    "RariCapital1": [
            ["deposit"],
            ["withdraw", "withdrawReserve", "reduceReserve"],
    ],
    "RariCapital2_1": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves", "_withdrawFuseFees"],
    ],
    "RariCapital2_2": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves", "_withdrawFuseFees"],
    ],
    "RariCapital2_3": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves", "_withdrawFuseFees"],
    ],
    "RariCapital2_4": [
            ["mint", "repayBorrow", "repayBorrowBehalf", "liquidateBorrow"],
            ["redeem", "redeemUnderlying", "borrow", "_reduceReserves", "_withdrawFuseFees"],
    ],
    "XCarnival": [
            ["mint", "repayBorrow", "repayBorrowAndClaim", "liquidateBorrow"],
            ["redeem", "redeemUnderlying", "borrow", "reduceReserves"],
    ],
    "Harvest1_fUSDT": [
            ["deposit", "depositFor"],
            ["withdraw", "withdrawAll"],
    ],
    "Harvest2_fUSDC": [
            ["deposit", "depositFor"],
            ["withdraw", "withdrawAll"],
    ],
    "ValueDeFi": [
            ["deposit", "depositFor", "depositAllFor", "depositAll"],
            ["withdraw", "withdrawFor"],
    ],
    "Yearn1": [
            ['deposit', 'depositAll'],
            ["withdraw", "withdrawAll", "migrate", "earn", "harvest"],
    ],
    "Yearn1_interface": [
            ['deposit'],
            ["withdraw", "withdrawAll"],
    ],
    "VisorFi": [
            ["deposit"],
            ["withdraw"],
    ],
    "UmbrellaNetwork": [
            ["stake"],
            ["withdraw", "exit"],
    ],
    "PickleFi": [
            ["deposit", "depositAll", "leverageUntil", "stake"],
            ["earn", "yearn", "withdraw", "withdrawAll", "claimRewards"],
    ],
    "Eminence": [
            ["buy"],
            ["sell"],
    ],
    "Opyn": [
            ["uniswapBuyOToken", "addERC20Collateral", "addAndSellERC20CollateralOption", "createAndSellETHCollateralOption", "createERC20CollateralOption", \
             "addERC20CollateralOption", "addETHCollateral", "addETHCollateralOption", "liquidate", "createAndSellERC20CollateralOption", "addAndSellETHCollateralOption", \
             "createETHCollateralOption", "issueOTokens"],
            ["removeCollateral", "redeemVaultBalance",  "removeUnderlying", "sellOTokens",  "burnOTokens"],
    ],
    "IndexFi": [
            ["joinPool", "joinswapExternAmountIn", "joinswapPoolAmountOut"],
            ["exitPool", "exitswapPoolAmountIn", "exitswapExternAmountOut", "gulp"],
    ],
    "RevestFi": [
            ["createFNFT", "depositToken", "handleMultipleDeposits"],
            ["withdrawToken", "splitFNFT"],
    ],
    "RevestFi_interface": [
            ["depositAdditionalToFNFT", "mintTimeLock", "mintValueLock", "mintAddressLock"],
            ["unlockFNFT", "withdrawFNFT", "splitFNFT", "extendFNFTMaturity"],
    ],
    "DODO": [
            ["buyShares"],
            ["sellQuote", "sellShares", "sellBase"],
    ],
    "Punk_1": [
        #     ['invest', 'reInvest'],
            [],
            ['withdrawAllToForge', 'withdrawTo', 'withdrawToForge'],
    ],
    "Punk_2": [
        #     ['invest', 'reInvest'],
            [],
            ['withdrawAllToForge', 'withdrawTo', 'withdrawToForge'],
    ],
    "Punk_3": [
        #     ['invest', 'reInvest'],
            [],
            ['withdrawAllToForge', 'withdrawTo', 'withdrawToForge'],
    ],
    "BeanstalkFarms": [
            ["add_liquidity"],
            ["remove_liquidity", "remove_liquidity_imbalance", "remove_liquidity_one_coin"],
    ],
    "BeanstalkFarms_interface": [
            [],
            [],
    ],

}




# thisMap2 = {
#     "RoninNetwork": [],
#     "HarmonyBridge": [],
#     "HarmonyBridge_interface": [],
#     "Nomad": [],
#     "PolyNetwork": [],
#     "bZx2": [],
#     "Warp": [],
#     "CheeseBank_1": [],
#     "CheeseBank_2": [],
#     "CheeseBank_3": [],
#     "InverseFi": [],
#     "CreamFi1_1": [],
#     "CreamFi2_1": [],
#     "CreamFi2_2": [],
#     "CreamFi2_3": [],
#     "CreamFi2_4": [],
#     "RariCapital1": ["marketSell0xOrdersFillOrKill"],
#     "RariCapital2_1": [],
#     "RariCapital2_2": [],
#     "RariCapital2_3": [],
#     "RariCapital2_4": [],
#     "XCarnival": [],
#     "Harvest1_fUSDT": [],
#     "Harvest2_fUSDC": [],
#     "ValueDeFi": [],
#     "Yearn1": [],
#     "VisorFi": [],
#     "UmbrellaNetwork": [],
#     "PickleFi": [],
#     "Eminence": [],
#     "Opyn": [],
#     "IndexFi": [],
#     "RevestFi": [],
#     "DODO": ['addressToShortString', 'approve', 'buyShares', 'flashLoan', 'init', 'permit', 'sellBase', 'sellQuote', 'sellShares', 'sync', 'transfer', 'transferFrom', 'version'],
#     "Punk_1": [],
#     "Punk_2": [],
#     "Punk_3": [],
#     "BeanstalkFarms": [],
# }




# similarFuncs = {
#     "RoninNetwork": [],
#     "HarmonyBridge": [],
#     "HarmonyBridge_interface": [],
#     "Nomad": [],
#     "PolyNetwork": [],
#     "bZx2": [],
#     "Warp": [],
#     "CheeseBank_1": ["repayBorrow", "repayBorrowBehalf"],
#     "CheeseBank_2": ["repayBorrow", "repayBorrowBehalf"],
#     "CheeseBank_3": ["repayBorrow", "repayBorrowBehalf"],
#     "InverseFi": ["repayBorrow", "repayBorrowBehalf"],
#     "CreamFi1_1": ["repayBorrowBehalf", "repayBorrow"],
#     "CreamFi1_2": ["repayBorrowBehalf", "repayBorrow"],
#     "CreamFi2_1": ["repayBorrowBehalf", "repayBorrow"],
#     "CreamFi2_2": ["repayBorrowBehalf", "repayBorrow"],
#     "CreamFi2_3": ["repayBorrowBehalf", "repayBorrow"],
#     "CreamFi2_4": ["repayBorrowBehalf", "repayBorrow"],
#     "RariCapital1": [],
#     "RariCapital2_1": [],
#     "RariCapital2_2": [],
#     "RariCapital2_3": [],
#     "RariCapital2_4": [],
#     "XCarnival": [],
#     "Harvest1_fUSDT": ["deposit", "depositFor"],
#     "Harvest2_fUSDC": ["deposit", "depositFor"],
#     "ValueDeFi": [["deposit", "depositFor", "depositAllFor", "depositAll"], ["withdraw"], ["withdrawFor"]], 
#     "Yearn1": ["withdraw", "withdrawAll"],
#     "VisorFi": [],
#     "UmbrellaNetwork": [],
#     "PickleFi": [],
#     "Eminence": [],
#     "Opyn": [],
#     "IndexFi": [
#         ["joinPool", "joinswapExternAmountIn", "joinswapPoolAmountOut"],
#         ["swapExactAmountIn", "swapExactAmountOut"],
#         ["exitPool", "exitswapPoolAmountIn", "exitswapExternAmountOut"]
#     ],
#     "RevestFi": [],
#     "DODO": [],
#     "Punk_1": [],
#     "Punk_2": [],
#     "Punk_3": [],
#     "BeanstalkFarms": [],
# }



# tokenFlowFuncs = {
#     "RoninNetwork": [
#         [],
#         [],
#     ],
#     "HarmonyBridge": [
#         [],
#         [],
#     ],
#     "HarmonyBridge_interface": [
#         [],
#         [],
#     ],
#     "Nomad": [
#         [],
#         [],
#     ],
#     "PolyNetwork": [
#         [],
#         [],
#     ],
#     "bZx2": [
#         ["borrowTokenFromDeposit"],
#         ["burn", "burnToEther", "marginTradeFromDeposit"],
#     ],
#     "Warp": [
#         [],
#         [],
#     ],
#     "Warp_interface": [
#         [],
#         [],
#     ],
#     "CheeseBank_1": [
#         [],
#         [],
#     ],
#     "CheeseBank_2": [
#         [],
#         [],
#     ],
#     "CheeseBank_3": [
#         [],
#         [],
#     ],
#     "InverseFi": [
#         [],
#         [],
#     ],
#     "CreamFi1_1": [
#         [],
#         [],
#     ],
#     "CreamFi2_1": [
#         [],
#         [],
#     ],
#     "CreamFi2_2": [
#         [],
#         [],
#     ],
#     "CreamFi2_3": [
#         [],
#         [],
#     ],
#     "CreamFi2_4": [
#         [],
#         [],
#     ],
#     "RariCapital1": [
#         [],
#         [],
#     ],
#     "RariCapital2_1": [
#         [],
#         [],
#     ],
#     "RariCapital2_2": [
#         [],
#         [],
#     ],
#     "RariCapital2_3": [
#         [],
#         [],
#     ],
#     "RariCapital2_4": [
#         [],
#         [],
#     ],
#     "XCarnival": [
#         [],
#         [],
#     ],
#     "Harvest1_fUSDT": [
#         ["deposit", "depositFor"],
#         ["withdraw"],
#     ],
#     "Harvest2_fUSDC": [
#         ["deposit", "depositFor"],
#         ["withdraw"],
#     ],
#     "ValueDeFi": [
#         [],
#         [],
#     ], 
#     "Yearn1": [
#         ["deposit", "depositAll"],
#         ["withdraw", "withdrawAll"],
#     ],
#     "Yearn1_interface": [
#         [],
#         [],
#     ],
#     "VisorFi": [
#         [],
#         [],
#     ],
#     "UmbrellaNetwork": [
#         [],
#         [],
#     ],
#     "PickleFi": [
#         [],
#         [],
#     ],
#     "Eminence": [
#         ["buy"],
#         ["sell"],
#     ],
#     "Opyn": [
#         [],
#         [],
#     ],
#     "IndexFi": [
#         [],
#         [],
#     ],
#     "RevestFi": [
#         [],
#         [],
#     ],
#     "DODO": [
#         [],
#         [],
#     ],
#     "Punk_1": [
#         [],
#         [],
#     ],
#     "Punk_2": [
#         [],
#         [],
#     ],
#     "Punk_3": [
#         [],
#         [],
#     ],
#     "BeanstalkFarms": [
#         [],
#         [],
#     ],
#     "BeanstalkFarms_interface": [
#         [],
#         [],
#     ],
# }




def benchmark2txCount(benchmark):
    return thisMapUpdated[benchmark]

def benchmark2EnterExitFuncs(benchmark):
    return thatMap2[benchmark][0], thatMap2[benchmark][1]
