
// File: contracts/lib/UInt256Lib.sol

pragma solidity >=0.4.24;


/**
 * @title Various utilities useful for uint256.
 */
library UInt256Lib {

    uint256 private constant MAX_INT256 = ~(uint256(1) << 255);

    /**
     * @dev Safely converts a uint256 to an int256.
     */
    function toInt256Safe(uint256 a)
        internal
        pure
        returns (int256)
    {
        require(a <= MAX_INT256);
        return int256(a);
    }
}

// File: contracts/lib/SafeMathInt.sol

/*
MIT License

Copyright (c) 2018 requestnetwork

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

pragma solidity >=0.4.24;


/**
 * @title SafeMathInt
 * @dev Math operations for int256 with overflow safety checks.
 */
library SafeMathInt {
    int256 private constant MIN_INT256 = int256(1) << 255;
    int256 private constant MAX_INT256 = ~(int256(1) << 255);

    /**
     * @dev Multiplies two int256 variables and fails on overflow.
     */
    function mul(int256 a, int256 b)
        internal
        pure
        returns (int256)
    {
        int256 c = a * b;

        // Detect overflow when multiplying MIN_INT256 with -1
        require(c != MIN_INT256 || (a & MIN_INT256) != (b & MIN_INT256));
        require((b == 0) || (c / b == a));
        return c;
    }

    /**
     * @dev Division of two int256 variables and fails on overflow.
     */
    function div(int256 a, int256 b)
        internal
        pure
        returns (int256)
    {
        // Prevent overflow when dividing MIN_INT256 by -1
        require(b != -1 || a != MIN_INT256);

        // Solidity already throws when dividing by 0.
        return a / b;
    }

    /**
     * @dev Subtracts two int256 variables and fails on overflow.
     */
    function sub(int256 a, int256 b)
        internal
        pure
        returns (int256)
    {
        int256 c = a - b;
        require((b >= 0 && c <= a) || (b < 0 && c > a));
        return c;
    }

    /**
     * @dev Adds two int256 variables and fails on overflow.
     */
    function add(int256 a, int256 b)
        internal
        pure
        returns (int256)
    {
        int256 c = a + b;
        require((b >= 0 && c >= a) || (b < 0 && c < a));
        return c;
    }

    /**
     * @dev Converts to absolute value, and fails on overflow.
     */
    function abs(int256 a)
        internal
        pure
        returns (int256)
    {
        require(a != MIN_INT256);
        return a < 0 ? -a : a;
    }
}

// File: contracts/interface/ISeigniorageShares.sol

pragma solidity >=0.4.24;


interface ISeigniorageShares {
    function setDividendPoints(address account, uint256 totalDividends) external returns (bool);
    function setDividendPointsEuro(address account, uint256 totalDividends) external returns (bool);

    function mintShares(address account, uint256 amount) external returns (bool);

    function lastDividendPoints(address who) external view returns (uint256);
    function lastDividendPointsEuro(address who) external view returns (uint256);
    function stakingStatus(address who) external view returns (uint256);
    
    function externalRawBalanceOf(address who) external view returns (uint256);
    function externalTotalSupply() external view returns (uint256);

    function totalStaked() external view returns (uint256);

    function deleteShare(address account, uint256 amount) external;
}

// File: openzeppelin-eth/contracts/math/SafeMath.sol

pragma solidity ^0.4.24;


/**
 * @title SafeMath
 * @dev Math operations with safety checks that revert on error
 */
library SafeMath {

  /**
  * @dev Multiplies two numbers, reverts on overflow.
  */
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
    // benefit is lost if 'b' is also tested.
    // See: https://github.com/OpenZeppelin/openzeppelin-solidity/pull/522
    if (a == 0) {
      return 0;
    }

    uint256 c = a * b;
    require(c / a == b);

    return c;
  }

  /**
  * @dev Integer division of two numbers truncating the quotient, reverts on division by zero.
  */
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b > 0); // Solidity only automatically asserts when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold

    return c;
  }

  /**
  * @dev Subtracts two numbers, reverts on overflow (i.e. if subtrahend is greater than minuend).
  */
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b <= a);
    uint256 c = a - b;

    return c;
  }

  /**
  * @dev Adds two numbers, reverts on overflow.
  */
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    require(c >= a);

    return c;
  }

  /**
  * @dev Divides two numbers and returns the remainder (unsigned integer modulo),
  * reverts when dividing by zero.
  */
  function mod(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b != 0);
    return a % b;
  }
}

// File: zos-lib/contracts/Initializable.sol

pragma solidity >=0.4.24 <0.6.0;


/**
 * @title Initializable
 *
 * @dev Helper contract to support initializer functions. To use it, replace
 * the constructor with a function that has the `initializer` modifier.
 * WARNING: Unlike constructors, initializer functions must be manually
 * invoked. This applies both to deploying an Initializable contract, as well
 * as extending an Initializable contract via inheritance.
 * WARNING: When used with inheritance, manual care must be taken to not invoke
 * a parent initializer twice, or ensure that all initializers are idempotent,
 * because this is not dealt with automatically as with constructors.
 */
contract Initializable {

  /**
   * @dev Indicates that the contract has been initialized.
   */
  bool private initialized;

  /**
   * @dev Indicates that the contract is in the process of being initialized.
   */
  bool private initializing;

  /**
   * @dev Modifier to use in the initializer function of a contract.
   */
  modifier initializer() {
    require(initializing || isConstructor() || !initialized, "Contract instance has already been initialized");

    bool isTopLevelCall = !initializing;
    if (isTopLevelCall) {
      initializing = true;
      initialized = true;
    }

    _;

    if (isTopLevelCall) {
      initializing = false;
    }
  }

  /// @dev Returns true if and only if the function is running in the constructor
  function isConstructor() private view returns (bool) {
    // extcodesize checks the size of the code stored in an address, and
    // address returns the current address. Since the code is still not
    // deployed when running a constructor, any checks on its code size will
    // yield zero, making it an effective way to detect if a contract is
    // under construction or not.
    uint256 cs;
    assembly { cs := extcodesize(address) }
    return cs == 0;
  }

  // Reserved storage space to allow for layout changes in the future.
  uint256[50] private ______gap;
}

// File: openzeppelin-eth/contracts/token/ERC20/IERC20.sol

pragma solidity ^0.4.24;


/**
 * @title ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
interface IERC20 {
  function totalSupply() external view returns (uint256);

  function balanceOf(address who) external view returns (uint256);

  function allowance(address owner, address spender)
    external view returns (uint256);

  function transfer(address to, uint256 value) external returns (bool);

  function approve(address spender, uint256 value)
    external returns (bool);

  function transferFrom(address from, address to, uint256 value)
    external returns (bool);

  event Transfer(
    address indexed from,
    address indexed to,
    uint256 value
  );

  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}

// File: openzeppelin-eth/contracts/token/ERC20/ERC20Detailed.sol

pragma solidity ^0.4.24;




/**
 * @title ERC20Detailed token
 * @dev The decimals are only for visualization purposes.
 * All the operations are done using the smallest and indivisible token unit,
 * just as on Ethereum all the operations are done in wei.
 */
contract ERC20Detailed is Initializable, IERC20 {
  string private _name;
  string private _symbol;
  uint8 private _decimals;

  function initialize(string name, string symbol, uint8 decimals) public initializer {
    _name = name;
    _symbol = symbol;
    _decimals = decimals;
  }

  /**
   * @return the name of the token.
   */
  function name() public view returns(string) {
    return _name;
  }

  /**
   * @return the symbol of the token.
   */
  function symbol() public view returns(string) {
    return _symbol;
  }

  /**
   * @return the number of decimals of the token.
   */
  function decimals() public view returns(uint8) {
    return _decimals;
  }

  uint256[50] private ______gap;
}

// File: openzeppelin-eth/contracts/ownership/Ownable.sol

pragma solidity ^0.4.24;


/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable is Initializable {
  address private _owner;


  event OwnershipRenounced(address indexed previousOwner);
  event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
  );


  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  function initialize(address sender) public initializer {
    _owner = sender;
  }

  /**
   * @return the address of the owner.
   */
  function owner() public view returns(address) {
    return _owner;
  }

  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(isOwner());
    _;
  }

  /**
   * @return true if `msg.sender` is the owner of the contract.
   */
  function isOwner() public view returns(bool) {
    return msg.sender == _owner;
  }

  /**
   * @dev Allows the current owner to relinquish control of the contract.
   * @notice Renouncing to ownership will leave the contract without an owner.
   * It will not be possible to call the functions with the `onlyOwner`
   * modifier anymore.
   */
  function renounceOwnership() public onlyOwner {
    emit OwnershipRenounced(_owner);
    _owner = address(0);
  }

  /**
   * @dev Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) public onlyOwner {
    _transferOwnership(newOwner);
  }

  /**
   * @dev Transfers control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function _transferOwnership(address newOwner) internal {
    require(newOwner != address(0));
    emit OwnershipTransferred(_owner, newOwner);
    _owner = newOwner;
  }

  uint256[50] private ______gap;
}

// File: contracts/usd/dollars.sol

pragma solidity >=0.4.24;







interface IDollarPolicy {
    function getUsdSharePrice() external view returns (uint256 price);
    function treasury() external view returns (address);
}

interface IBond {
    function mint(address _who, uint256 _amount) external;
    function rebond(address _who, uint256 _amount, uint256 _usdAmount) external;
    function remove(address _who, uint256 _amount, uint256 _usdAmount) external;
    function balanceOf(address who) external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function setLastRebase(uint256 newUsdAmount) external;
    function claimableProRataUSD(address _who) external view returns (uint256);
}

interface IPool {
    function setLastRebase(uint256 newUsdAmount) external;
}

interface IStake {
    function addRebaseFunds(uint256 newUsdAmount) external;    
}

/*
 *  Dollar ERC20
 */

contract Dollars is ERC20Detailed, Ownable {
    using SafeMath for uint256;
    using SafeMathInt for int256;

    event LogRebase(uint256 indexed epoch, uint256 totalSupply);
    event LogContraction(uint256 indexed epoch, uint256 dollarsToBurn);
    event LogRebasePaused(bool paused);
    event LogBurn(address indexed from, uint256 value);
    event LogClaim(address indexed from, uint256 value);
    event LogMonetaryPolicyUpdated(address monetaryPolicy);

    // Used for authentication
    address public monetaryPolicy;
    address public sharesAddress;

    modifier onlyMonetaryPolicy() {
        require(msg.sender == monetaryPolicy);
        _;
    }

    // Precautionary emergency controls.
    bool public rebasePaused;

    modifier whenRebaseNotPaused() {
        require(!rebasePaused);
        _;
    }

    uint256 public stakeToShareRatio;

    modifier validRecipient(address to) {
        require(to != address(0x0));
        require(to != address(this));
        _;
    }

    uint256 private constant DECIMALS = 9;
    uint256 private constant MAX_UINT256 = ~uint256(0);
    uint256 private constant INITIAL_DOLLAR_SUPPLY = 1 * 10**6 * 10**DECIMALS;
    uint256 private _maxDiscount;

    modifier validDiscount(uint256 discount) {
        require(discount >= 0);
        require(discount <= _maxDiscount);
        _;
    }

    uint256 private constant MAX_SUPPLY = ~uint128(0);  // (2^128) - 1

    uint256 private _totalSupply;

    uint256 private constant POINT_MULTIPLIER = 10 ** 9;

    uint256 private _totalDividendPoints;
    uint256 private _unclaimedDividends;

    ISeigniorageShares Shares;

    mapping(address => uint256) private _dollarBalances;

    // This is denominated in Dollars, because the cents-dollars conversion might change before
    // it's fully paid.
    mapping (address => mapping (address => uint256)) private _allowedDollars;

    IDollarPolicy DollarPolicy;
    uint256 public rebaseRewardUSDx;
    uint256 public debaseBoolean;   // 1 is true, 0 is false
    uint256 public lpToShareRatio;

    uint256 public minimumBonusThreshold;

    bool reEntrancyMutex;
    bool reEntrancyRebaseMutex;

    address public timelock;
    mapping(address => bool) public deprecatedDeleteWhitelist;
    event LogDeletion(address account, uint256 amount);
    bool usdDeletion;

    modifier onlyMinter() {
        require(msg.sender == monetaryPolicy || msg.sender == DollarPolicy.treasury(), "Only Minter");
        _;
    }

    address public stakeAddress;
    event LogDollarReserveUpdated(address deprecated);

    mapping(address => bool) public debased; // mapping if an address has deleted 50% of their dollar tokens

    modifier onlyShare() {
        require(msg.sender == sharesAddress, "unauthorized");
        _;
    }

    uint256 public remainingUsdToMint;
    uint256 public redeemingBonus;

    bool public emptyVariable1;      // bool variable for use in future

    mapping(address => uint256) public debtPoints;
    uint256 private _totalDebtPoints;
    uint256 private _unclaimedDebt;
    address[] public uniSyncPairs;

    bool public tenPercentCap;
    uint256 public bondToShareRatio;
    event NewBondToShareRatio(uint256 ratio);
    uint256 public bondSupply;
    address public bondAddress;
    bool public lastRebasePositive;
    address public poolRewardAddress;
    bool public lastRebaseNeutral;

    string private _symbol;

    mapping(address => bool) public debaseWhitelist; // addresses that are true will not be debased
    event LogDebaseWhitelist(address user, bool value);

    /**
     * @param monetaryPolicy_ The address of the monetary policy contract to use for authentication.
     */
    function setMonetaryPolicy(address monetaryPolicy_)
        external
        onlyOwner
    {
        monetaryPolicy = monetaryPolicy_;
        DollarPolicy = IDollarPolicy(monetaryPolicy_);
        emit LogMonetaryPolicyUpdated(monetaryPolicy_);
    }

    function setDebaseWhitelist(address user, bool val) {
        require(msg.sender == timelock || msg.sender == address(0x89a359A3D37C3A857E62cDE9715900441b47acEC));
        debaseWhitelist[user] = val;
        emit LogDebaseWhitelist(user, val);
    }

    function changeSymbol(string memory symbol) public {
        require(msg.sender == timelock);
        _symbol = symbol;
    }

    function setRebaseRewardUSDx(uint256 reward) external {
        require(msg.sender == timelock || msg.sender == address(0x89a359A3D37C3A857E62cDE9715900441b47acEC));
        rebaseRewardUSDx = reward;
    }
    
    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function setTimelock(address timelock_)
        external
        onlyOwner
    {
        timelock = timelock_;
    }

    function setBondShareRatio(uint256 val_)
        external
    {
        require(msg.sender == timelock || msg.sender == address(0x89a359A3D37C3A857E62cDE9715900441b47acEC));
        require(val_ <= 100);

        bondToShareRatio = val_;   
        emit NewBondToShareRatio(bondToShareRatio);
    }

    function setLpToShareRatio(uint256 val_)
        external
    {
        require(msg.sender == timelock || msg.sender == address(0x89a359A3D37C3A857E62cDE9715900441b47acEC));
        require(val_ <= 100);

        lpToShareRatio = val_;
    }

    function setStakeToShareRatio(uint256 val_)
        external
    {
        require(msg.sender == timelock || msg.sender == address(0x89a359A3D37C3A857E62cDE9715900441b47acEC));
        require(val_ <= 100);

        stakeToShareRatio = val_;
    }

    function setBondAddress(address bond_) external onlyOwner {
        bondAddress = bond_;
    }

    function setStakeAddress(address stake_) external onlyOwner {
        stakeAddress = stake_;
    }

    function setPoolAddress(address pool_) external onlyOwner {
        poolRewardAddress = pool_;
    }

    // number of dollars to bond
    function bond(uint256 amount) updateAccount(msg.sender) external {
        require(!reEntrancyMutex, "dp::reentrancy");
        reEntrancyMutex = true;

        require(balanceOf(msg.sender) >= amount, "insufficient usd balance");

        uint256 totalDollarBonded = balanceOf(address(this));
        uint256 totalBonds = IBond(bondAddress).totalSupply();
        
        // 1-1 if negative rebase
        if (totalBonds == 0 || totalDollarBonded == 0 || (!lastRebasePositive && !lastRebaseNeutral)) {
            IBond(bondAddress).mint(msg.sender, amount);
        } else {
            uint256 bondAmount = amount.mul(totalBonds).div(totalDollarBonded);
            IBond(bondAddress).mint(msg.sender, bondAmount);
        }

        _dollarBalances[msg.sender] = _dollarBalances[msg.sender].sub(amount);
        _dollarBalances[address(this)] = _dollarBalances[address(this)].add(amount);

        emit Transfer(msg.sender, address(this), amount);
        reEntrancyMutex = false;
    }

    function unbondMax(bool rebond) updateAccount(msg.sender) external {
        require(!reEntrancyMutex, "dp::reentrancy");
        reEntrancyMutex = true;

        // can only redeem during a positive rebase
        require(lastRebasePositive, "can only redeem during positive rebase!");

        uint256 totalBonds = IBond(bondAddress).totalSupply();
        uint256 dollarRedeemedAmount = IBond(bondAddress).claimableProRataUSD(msg.sender);
        uint256 bondsToBurn = dollarRedeemedAmount.mul(totalBonds).div(balanceOf(address(this)));

        require(IBond(bondAddress).balanceOf(msg.sender) >= bondsToBurn, "insufficient bond balance");

        if (rebond) {
            IBond(bondAddress).rebond(msg.sender, bondsToBurn, dollarRedeemedAmount);
        } else {
            IBond(bondAddress).remove(msg.sender, bondsToBurn, dollarRedeemedAmount);

            _dollarBalances[msg.sender] = _dollarBalances[msg.sender].add(dollarRedeemedAmount);
            _dollarBalances[address(this)] = _dollarBalances[address(this)].sub(dollarRedeemedAmount);

            emit Transfer(address(this), msg.sender, dollarRedeemedAmount);
        }

        reEntrancyMutex = false;
    }

    function removeUniPair(uint256 index) external onlyOwner {
        if (index >= uniSyncPairs.length) return;

        for (uint i = index; i < uniSyncPairs.length-1; i++){
            uniSyncPairs[i] = uniSyncPairs[i+1];
        }
        uniSyncPairs.length--;
    }

    function getUniSyncPairs()
        external
        view
        returns (address[] memory)
    {
        address[] memory pairs = uniSyncPairs;
        return pairs;
    }

    function addSyncPairs(address[] memory uniSyncPairs_)
        public
        onlyOwner
    {
        for (uint256 i = 0; i < uniSyncPairs_.length; i++) {
            uniSyncPairs.push(uniSyncPairs_[i]);
        }
    }

    function setTenPercentCap(bool _val)
        external
    {
        require(msg.sender == timelock);
        tenPercentCap = _val;
    }

    /**
     * @dev Pauses or unpauses the execution of rebase operations.
     * @param paused Pauses rebase operations if this is true.
     */
    function setRebasePaused(bool paused)
        external
    {
        require(msg.sender == timelock || msg.sender == address(0x89a359A3D37C3A857E62cDE9715900441b47acEC));
        rebasePaused = paused;
        emit LogRebasePaused(paused);
    }

    function setDebaseBoolean(uint256 val_)
        external
    {
        require(msg.sender == timelock || msg.sender == address(0x89a359A3D37C3A857E62cDE9715900441b47acEC));
        require(val_ <= 1, "value must be 0 or 1");
        debaseBoolean = val_;
    }

    function syncUniswapV2()
        external
    {
        for (uint256 i = 0; i < uniSyncPairs.length; i++) {
            (bool success, ) = uniSyncPairs[i].call(abi.encodeWithSignature('sync()'));
        }
    }

    /**
     * @dev Notifies Dollars contract about a new rebase cycle.
     * @param supplyDelta The number of new dollar tokens to add into circulation via expansion.
     * @return The total number of dollars after the supply adjustment.
     */
    function rebase(uint256 epoch, int256 supplyDelta)
        external
        onlyMonetaryPolicy
        whenRebaseNotPaused
        updateAccount(tx.origin)
        returns (uint256)
    {
        require(!reEntrancyRebaseMutex, "dp::reentrancy");
        reEntrancyRebaseMutex = true;

        if (supplyDelta == 0) {
            IPool(poolRewardAddress).setLastRebase(0);
            IBond(bondAddress).setLastRebase(0);

            lastRebasePositive = false;
            lastRebaseNeutral = true;
        } else if (supplyDelta < 0) {
            lastRebasePositive = false;
            lastRebaseNeutral = false;

            IPool(poolRewardAddress).setLastRebase(0);
            IBond(bondAddress).setLastRebase(0);

            if (debaseBoolean == 1) {
                negativeRebaseHelper(epoch, supplyDelta);
            }
        } else { // > 0
            positiveRebaseHelper(supplyDelta);

            emit LogRebase(epoch, _totalSupply);
            lastRebasePositive = true;
            lastRebaseNeutral = false;

            if (_totalSupply > MAX_SUPPLY) {
                _totalSupply = MAX_SUPPLY;
            }
        }

        for (uint256 i = 0; i < uniSyncPairs.length; i++) {
            (bool success, ) = uniSyncPairs[i].call(abi.encodeWithSignature('sync()'));
        }

        _dollarBalances[tx.origin] = _dollarBalances[tx.origin].add(rebaseRewardUSDx);
        _totalSupply = _totalSupply.add(rebaseRewardUSDx);
        emit Transfer(address(0x0), tx.origin, rebaseRewardUSDx);

        reEntrancyRebaseMutex = false;
        return _totalSupply;
    }

    function negativeRebaseHelper(uint256 epoch, int256 supplyDelta) internal {
        uint256 dollarsToDelete = uint256(supplyDelta.abs());
        if (dollarsToDelete > _totalSupply.div(10) && tenPercentCap) { // maximum contraction is 10% of the total USD Supply
            dollarsToDelete = _totalSupply.div(10);
        }

        _totalDebtPoints = _totalDebtPoints.add(dollarsToDelete.mul(POINT_MULTIPLIER).div(_totalSupply));
        _unclaimedDebt = _unclaimedDebt.add(dollarsToDelete);
        emit LogContraction(epoch, dollarsToDelete);
    }

    function positiveRebaseHelper(int256 supplyDelta) internal {
        uint256 dollarsToBonds = uint256(supplyDelta).mul(bondToShareRatio).div(100);
        uint256 dollarsToLPs = uint256(supplyDelta).sub(dollarsToBonds).mul(lpToShareRatio).div(100);
        uint256 dollarsToStake = uint256(supplyDelta).sub(dollarsToBonds).sub(dollarsToLPs).mul(stakeToShareRatio).div(100);
        
        IPool(poolRewardAddress).setLastRebase(dollarsToLPs);
        _dollarBalances[poolRewardAddress] = _dollarBalances[poolRewardAddress].add(dollarsToLPs);
        emit Transfer(address(0x0), poolRewardAddress, dollarsToLPs);

        _dollarBalances[address(this)] = _dollarBalances[address(this)].add(dollarsToBonds);
        IBond(bondAddress).setLastRebase(dollarsToBonds);
        emit Transfer(address(0x0), address(this), dollarsToBonds);

        _dollarBalances[stakeAddress] = _dollarBalances[stakeAddress].add(dollarsToStake);
        IStake(stakeAddress).addRebaseFunds(dollarsToStake);
        emit Transfer(address(0x0), stakeAddress, dollarsToStake);
        
        _totalSupply = _totalSupply.add(dollarsToBonds).add(dollarsToLPs).add(dollarsToStake);

        disburse(uint256(supplyDelta).sub(dollarsToBonds).sub(dollarsToLPs).sub(dollarsToStake));
    }

    function initialize(address owner_, address seigniorageAddress)
        public
        initializer
    {
        ERC20Detailed.initialize("Dollars", "USD", uint8(DECIMALS));
        Ownable.initialize(owner_);

        rebasePaused = false;
        _totalSupply = INITIAL_DOLLAR_SUPPLY;

        sharesAddress = seigniorageAddress;
        Shares = ISeigniorageShares(seigniorageAddress);

        _dollarBalances[owner_] = _totalSupply;
        _maxDiscount = 50 * 10 ** 9;                // 50%
        minimumBonusThreshold = 100 * 10 ** 9;      // 100 dollars is the minimum threshold. Anything above warrants increased discount

        emit Transfer(address(0x0), owner_, _totalSupply);
    }

    /**
     * @return The total number of dollars.
     */
    function totalSupply()
        external
        view
        returns (uint256)
    {
        return _totalSupply;
    }

    /**
     * @param who The address to query.
     * @return The balance of the specified address.
     */
    function balanceOf(address who)
        public
        view
        returns (uint256)
    {
        // bond holders get no debt
        uint256 debt = debtOwing(who);
        debt = debt <= _dollarBalances[who] ? debt : _dollarBalances[who];

        return _dollarBalances[who].sub(debt);
    }

    /**
     * @dev Transfer tokens to a specified address.
     * @param to The address to transfer to.
     * @param value The amount to be transferred.
     * @return True on success, false otherwise.
     */
    function transfer(address to, uint256 value)
        external
        validRecipient(to)
        updateAccount(msg.sender)
        updateAccount(to)
        returns (bool)
    {
        require(!reEntrancyRebaseMutex, "dp::reentrancy");

        _dollarBalances[msg.sender] = _dollarBalances[msg.sender].sub(value);
        _dollarBalances[to] = _dollarBalances[to].add(value);
        emit Transfer(msg.sender, to, value);

        return true;
    }

    /**
     * @dev Function to check the amount of tokens that an owner has allowed to a spender.
     * @param owner_ The address which owns the funds.
     * @param spender The address which will spend the funds.
     * @return The number of tokens still available for the spender.
     */
    function allowance(address owner_, address spender)
        external
        view
        returns (uint256)
    {
        return _allowedDollars[owner_][spender];
    }

    /**
     * @dev Transfer tokens from one address to another.
     * @param from The address you want to send tokens from.
     * @param to The address you want to transfer to.
     * @param value The amount of tokens to be transferred.
     */
    function transferFrom(address from, address to, uint256 value)
        external
        validRecipient(to)
        updateAccount(from)
        updateAccount(to)
        returns (bool)
    {
        require(!reEntrancyRebaseMutex, "dp::reentrancy");

        _allowedDollars[from][msg.sender] = _allowedDollars[from][msg.sender].sub(value);

        _dollarBalances[from] = _dollarBalances[from].sub(value);
        _dollarBalances[to] = _dollarBalances[to].add(value);
        emit Transfer(from, to, value);

        return true;
    }

    /**
     * @dev Approve the passed address to spend the specified amount of tokens on behalf of
     * msg.sender. This method is included for ERC20 compatibility.
     * increaseAllowance and decreaseAllowance should be used instead.
     * Changing an allowance with this method brings the risk that someone may transfer both
     * the old and the new allowance - if they are both greater than zero - if a transfer
     * transaction is mined before the later approve() call is mined.
     *
     * @param spender The address which will spend the funds.
     * @param value The amount of tokens to be spent.
     */
    function approve(address spender, uint256 value)
        external
        validRecipient(spender)
        returns (bool)
    {
        _allowedDollars[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    /**
     * @dev Increase the amount of tokens that an owner has allowed to a spender.
     * This method should be used instead of approve() to avoid the double approval vulnerability
     * described above.
     * @param spender The address which will spend the funds.
     * @param addedValue The amount of tokens to increase the allowance by.
     */
    function increaseAllowance(address spender, uint256 addedValue)
        external
        returns (bool)
    {
        _allowedDollars[msg.sender][spender] =
            _allowedDollars[msg.sender][spender].add(addedValue);
        emit Approval(msg.sender, spender, _allowedDollars[msg.sender][spender]);
        return true;
    }

    /**
     * @dev Decrease the amount of tokens that an owner has allowed to a spender.
     *
     * @param spender The address which will spend the funds.
     * @param subtractedValue The amount of tokens to decrease the allowance by.
     */
    function decreaseAllowance(address spender, uint256 subtractedValue)
        external
        returns (bool)
    {
        uint256 oldValue = _allowedDollars[msg.sender][spender];
        if (subtractedValue >= oldValue) {
            _allowedDollars[msg.sender][spender] = 0;
        } else {
            _allowedDollars[msg.sender][spender] = oldValue.sub(subtractedValue);
        }
        emit Approval(msg.sender, spender, _allowedDollars[msg.sender][spender]);
        return true;
    }

    function claimDividends(address account) external updateAccount(account) returns (bool) {
        return true;
    }

    function dividendsOwing(address account) public view returns (uint256) {
        if (_totalDividendPoints > Shares.lastDividendPoints(account) && Shares.stakingStatus(account) == 1) {
            uint256 newDividendPoints = _totalDividendPoints.sub(Shares.lastDividendPoints(account));
            uint256 sharesBalance = Shares.externalRawBalanceOf(account);
            return sharesBalance.mul(newDividendPoints).div(POINT_MULTIPLIER);
        } else {
            return 0;
        }
    }

    function debtOwing(address account) public view returns (uint256) {
        if (_totalDebtPoints > debtPoints[account] && !debaseWhitelist[account]) {
            uint256 newDebtPoints = _totalDebtPoints.sub(debtPoints[account]);
            uint256 dollarBalance = _dollarBalances[account];
            return dollarBalance.mul(newDebtPoints).div(POINT_MULTIPLIER);
        } else {
            return 0;
        }
    }

    modifier updateAccount(address account) {
        uint256 owing = dividendsOwing(account);
        uint256 debt = debtOwing(account);

        if (owing > 0) {
            _unclaimedDividends = owing <= _unclaimedDividends ? _unclaimedDividends.sub(owing) : 0;
            _dollarBalances[account] = _dollarBalances[account].add(owing);
            _totalSupply = _totalSupply.add(owing);
            emit Transfer(address(0), account, owing);
        }

        if (debt > 0) {
            _unclaimedDebt = debt <= _unclaimedDebt ? _unclaimedDebt.sub(debt) : 0;

            // only debase non-whitelisted users
            if (!debaseWhitelist[account]) {
                debt = debt <= _dollarBalances[account] ? debt : _dollarBalances[account];

                _dollarBalances[account] = _dollarBalances[account].sub(debt);
                _totalSupply = _totalSupply.sub(debt);
                emit Transfer(account, address(0), debt);
            }
        }

        emit LogClaim(account, owing);

        Shares.setDividendPoints(account, _totalDividendPoints);
        debtPoints[account] = _totalDebtPoints;

        _;
    }

    function unclaimedDividends()
        external
        view
        returns (uint256)
    {
        return _unclaimedDividends;
    }

    function totalDividendPoints()
        external
        view
        returns (uint256)
    {
        return _totalDividendPoints;
    }

    function unclaimedDebt()
        external
        view
        returns (uint256)
    {
        return _unclaimedDebt;
    }

    function totalDebtPoints()
        external
        view
        returns (uint256)
    {
        return _totalDebtPoints;
    }

    function disburse(uint256 amount) internal returns (bool) {
        _totalDividendPoints = _totalDividendPoints.add(amount.mul(POINT_MULTIPLIER).div(Shares.totalStaked()));
        _unclaimedDividends = _unclaimedDividends.add(amount);

        return true;
    }
}
