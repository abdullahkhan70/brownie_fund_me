// SPDX-License-Identifier: MIT;

pragma solidity ^0.6.6;

// If we compile our code through brownie, then it won't compile at all.
// it is because @chainlink is a npm based library, but we can download it from,
// Github.

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// In order to fix the overflow, and or overflow we need to import some other
// library, but remember that in 0.8 version solidity, it is pre build, so you don't
// need to worry about it. If you are using the less than 0.8 version, then you need
// to use this library from the chainlink.

import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;
    // In order to track the transaction, we will need to make a function as payable.
    mapping(address => uint256) public getAddressOfPerson;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        // If someone, sends more than 50 dollars then what will he do.
        uint256 minimunUsd = 50 * 10**18;
        // Now we are going to check whether the user has spend more USD than the minimum.
        // If he ot she doesn't send enough eth then we can return the eth back to their wallet.
        require(
            getConversionRate(msg.value) >= minimunUsd,
            "You need to spend more ETH!"
        );

        // or we can revert back the amount through this way as well. But the most apportiate way is.
        // if(msg.value < minimunUsd) {
        //   revert?
        // }

        getAddressOfPerson[msg.sender] += msg.value;
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getDescription() public view returns (string memory) {
        return priceFeed.description();
    }

    function getDecimal() public view returns (uint8) {
        return priceFeed.decimals();
    }

    function getLatestRoundData()
        public
        view
        returns (
            uint80,
            int256,
            uint256,
            uint256,
            uint80
        )
    {
        return priceFeed.latestRoundData();
    }

    // returns the data from the Tuple.
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    // In order to convert the ETH to USD, then we can use the following function.
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        // But if someone tries to send the eth in wei, or Gwei format, then it needs
        // to convert it in order to get the real USD price.
        // So, for conversion we will make the logic something like this.
        // We will devide this by something like this, 1000000000000000000.

        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;

        // Now, it will returns some large number.
        // 0.000003021732141040
        return ethAmountInUsd;
    }

    // Now, we need to withdraw the ETH.
    function withdraw() public payable {
        require(msg.sender == owner, "First you need to spend some ETH!");
        msg.sender.transfer(address(this).balance);
    }

    function getEnteranceFee() public view returns (uint256) {
        // Minimuim USD is 50 dollars so we need to convert this into Wei charges.
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }
}
