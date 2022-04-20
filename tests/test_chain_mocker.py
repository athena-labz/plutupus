import pytest
from Plutupus import Mocha
from Plutupus import TxBody
from Plutupus.Mocha.Mocha import MochaError
from Plutupus.Types import Value


def test_simple_transaction():
    body = TxBody.send_to_address(
        input_utxo="abc#0",
        input_address="addr_test1",
        output_address="addr_test2",
        value=Value.lovelace(2_000_000)
    )

    mocha = Mocha(
        initial_utxos=[{
            "hash": "abc",
            "index": 0,
            "address": "addr_test1",
            "value": Value.lovelace(10_000_000)
        }],
        fees=1_000_000
    )

    assert mocha.current_utxos() == [{
        "hash": "abc",
        "index": 0,
        "address": "addr_test1",
        "value": Value.lovelace(10_000_000)
    }]

    assert mocha.current_balances() == {
        "addr_test1": Value.lovelace(10_000_000)
    }

    tx_hash = mocha.submit_transaction(body)

    assert mocha.current_utxos() == [{
        "hash": tx_hash,
        "index": 0,
        "address": "addr_test1",
        "value": Value.lovelace(7_000_000)
    }, {
        "hash": tx_hash,
        "index": 1,
        "address": "addr_test2",
        "value": Value.lovelace(2_000_000)
    }]

    assert mocha.current_balances() == {
        "addr_test1": Value.lovelace(7_000_000),
        "addr_test2": Value.lovelace(2_000_000)
    }


def test_mint_transaction():
    body = TxBody()
    body.add_input("abc", "0")
    body.set_mint_value(Value.from_token("never.gonna", 5))
    body.set_change("addr_test1")
    body.add_output("addr_test2", Value.from_dictionary({
        "lovelace": 2_000_000,
        "never.gonna": 5
    }))

    mocha = Mocha(
        initial_utxos=[{
            "hash": "abc",
            "index": 0,
            "address": "addr_test1",
            "value": Value.lovelace(10_000_000)
        }],
        fees=1_000_000
    )

    assert mocha.current_utxos() == [{
        "hash": "abc",
        "index": 0,
        "address": "addr_test1",
        "value": Value.lovelace(10_000_000)
    }]

    assert mocha.current_balances() == {
        "addr_test1": Value.lovelace(10_000_000)
    }

    tx_hash = mocha.submit_transaction(body)

    assert mocha.current_utxos() == [{
        "hash": tx_hash,
        "index": 0,
        "address": "addr_test1",
        "value": Value.lovelace(7_000_000)
    }, {
        "hash": tx_hash,
        "index": 1,
        "address": "addr_test2",
        "value": Value.from_dictionary({
            "lovelace": 2_000_000,
            "never.gonna": 5
        })
    }]

    assert mocha.current_balances() == {
        "addr_test1": Value.lovelace(7_000_000),
        "addr_test2": Value.from_dictionary({
            "lovelace": 2_000_000,
            "never.gonna": 5
        })
    }


def test_collateral_transaction():
    body = TxBody()
    body.add_input("abc", "1")
    body.set_change("addr_test1")
    body.add_output("addr_test2", Value.lovelace(2_000_000))
    body.set_collateral("abc", "0")

    mocha = Mocha(
        initial_utxos=[{
            "hash": "abc",
            "index": 0,
            "address": "addr_test1",
            "value": Value.lovelace(5_000_000)
        }, {
            "hash": "abc",
            "index": 1,
            "address": "addr_test1",
            "value": Value.lovelace(10_000_000)
        }],
        fees=1_000_000
    )

    assert mocha.current_utxos() == [{
        "hash": "abc",
        "index": 0,
        "address": "addr_test1",
        "value": Value.lovelace(5_000_000)
    }, {
        "hash": "abc",
        "index": 1,
        "address": "addr_test1",
        "value": Value.lovelace(10_000_000)
    }]

    assert mocha.current_balances() == {
        "addr_test1": Value.lovelace(15_000_000)
    }

    tx_hash = mocha.submit_transaction(body)

    assert mocha.current_utxos() == [{
        "hash": tx_hash,
        "index": 0,
        "address": "addr_test1",
        "value": Value.lovelace(5_000_000)
    }, {
        "hash": tx_hash,
        "index": 1,
        "address": "addr_test1",
        "value": Value.lovelace(7_000_000)
    }, {
        "hash": tx_hash,
        "index": 2,
        "address": "addr_test2",
        "value": Value.lovelace(2_000_000)
    }]

    assert mocha.current_balances() == {
        "addr_test1": Value.lovelace(12_000_000),
        "addr_test2": Value.lovelace(2_000_000)
    }


def test_failing_transaction():
    body = TxBody.send_to_address(
        input_utxo="abc#0",
        input_address="addr_test1",
        output_address="addr_test2",
        value=Value.lovelace(10_000_000)
    )

    mocha = Mocha(
        initial_utxos=[{
            "hash": "abc",
            "index": 0,
            "address": "addr_test1",
            "value": Value.lovelace(10_000_000)
        }],
        fees=1_000_000
    )

    assert mocha.current_utxos() == [{
        "hash": "abc",
        "index": 0,
        "address": "addr_test1",
        "value": Value.lovelace(10_000_000)
    }]

    assert mocha.current_balances() == {
        "addr_test1": Value.lovelace(10_000_000)
    }

    with pytest.raises(MochaError):
        mocha.submit_transaction(body)
