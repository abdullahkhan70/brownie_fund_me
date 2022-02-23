from brownie import FundMe
from scripts.helpful_script import get_accounts


def fund_me_withdraw():
    fund_me = FundMe[-1]
    account = get_accounts()
    entrance_fee = fund_me.getEnteranceFee()
    print(f"The Current entry fee is {entrance_fee}")
    print("Funding...")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_accounts()
    fund_me.withdraw(
        {
            "from": account,
        }
    )


def main():
    fund_me_withdraw()
    withdraw()
