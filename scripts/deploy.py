from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_script import get_accounts, deploy_mocks, LOCAL_BLOCKCHAIN
from web3 import Web3


def deploy_fund_me_contract():
    account = get_accounts()

    # Whenever, we run our scripts, then it generates an address.
    # This address is basically used to define what is going on with our
    # transaction, and once it is done then it returns the message "Successfully transaction complete" likewise.
    # But whenever we want to see whether the contract is vrified or not,
    # then it shows us about our information related of our Smart Contract.
    # It basically returns our bytecode's object as in the contract section, when oru contract is not
    # verified by Etherscan.io
    # In order to verified it we need to verified our contract by publishing our contract source code,
    # If we just copy and paste our contract source code in the contract section, then It won't know about
    # chainlink module. So, for solving this problem we can use the "Flattening" method, In Flattening method,
    # we just need to copy and paste all the chainlink's sol interfaces into our contract, but Brownie,
    # automatically do these all stuff by it ownself.
    # simply give a perimeter as publish_source=True which allows to automatically publish our source code to the Etherscan.
    # we need the Etherscan API key and define it in our .env as ETHERSCAN_TOKEN.
    # NOTE:
    #  If we provide our smart contract source code to Etherscan, then it will show the others that this
    #  contract is valid.
    #
    # fund_me_contract = FundMe.deploy({"from":account}, publish_source=True)
    # print(f"Contract Deployed at {fund_me_contract.address}")

    # Now, there is a question araise and that is, how can we get the
    # the USD rate of one Etherium. There are two methods.
    # 1. Forking
    # 2. Mocking
    # In the first method we generally define our own test network or mainnet address through brownie-config.yaml file.
    # And in the second method we generally define our dummy address through chainlink-mix library.
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        price_feed_contract = config["networks"][network.show_active()]["eth_usd"]
    else:
        deploy_mocks()
        price_feed_contract = MockV3Aggregator[-1].address

    fund_me_contract = FundMe.deploy(
        price_feed_contract,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract Deployed at {fund_me_contract.address}")
    return fund_me_contract


def main():
    deploy_fund_me_contract()
