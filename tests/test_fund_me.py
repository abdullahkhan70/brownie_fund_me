from scripts.deploy import deploy_fund_me_contract, get_accounts
from brownie import network, accounts, exceptions
import pytest
from scripts.helpful_script import LOCAL_BLOCKCHAIN


def test_fund_me_and_withdraw():
    account = get_accounts()
    fund_me = deploy_fund_me_contract()
    enterance_fee = fund_me.getEnteranceFee() + 100
    tx = fund_me.fund({"from": account, "value": enterance_fee})
    tx.wait(1)
    assert fund_me.getAddressOfPerson(account.address) == enterance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.getAddressOfPerson(account.address) == 0


def test_only_development():
    if network.show_active() not in LOCAL_BLOCKCHAIN:
        pytest.skip("Only the development network can be tested!")
    fund_me = deploy_fund_me_contract()
    account = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": account})
