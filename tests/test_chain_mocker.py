from Plutupus import Mocha
from Plutupus import TxBody
from Plutupus.Types import Value


def test_chain_mocker():
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

    body = TxBody.send_to_address(
        input_utxo="abc#0",
        input_address="addr_test1",
        output_address="addr_test2",
        value=Value.lovelace(2_000_000)
    )

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