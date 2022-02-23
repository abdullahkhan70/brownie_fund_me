from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

# We need the eight Decimals, bacause as we know that Gwei has eight decimals points

DECIMALS = 8

# We also need to add the eight zeros along with our price.
STARTING_PRICE = 2000

LOCAL_BLOCKCHAIN = ["development", "ganache-local"]
MAINNET_FORK = ["mainnet-fork-dev", "mainnet-fork-third"]


def get_accounts():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN
        or network.show_active() in MAINNET_FORK
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The current Network is {network.show_active()}")
    print("The deploying get started...")

    # Make sure If we have already deployed our MockV3Aggregator contract, then we need to check
    # it's length, and then decide whether we should better go for it or not.
    # The MockV3Aggregator will simply returns the address of the fake Usd rate of one ETH.
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_accounts()}
        )
        print(f"Successfully, deployed at {MockV3Aggregator[-1].address}")
