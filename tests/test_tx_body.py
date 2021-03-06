from Plutupus import TxBody
from Plutupus.Types.TxOutRef import TxOutRef
from Plutupus.Types.Value import Value


def test_build():
    body = TxBody.build(
        "alonzo",
        "magic_number",
        [TxOutRef("tx_hash_1", "tx_ix_1"), TxOutRef("tx_hash_2", "tx_ix_2")],
        "sender_address",
        [
            {"address": "receiver_address_1",
                "value": Value.lovelace(5_000_000)},
            {"address": "receiver_address_2",
                "value": Value.lovelace(7_000_000)}
        ],
        "path/to/metadata"
    )

    assert body.era == "alonzo"
    assert body.magic == "magic_number"
    assert body.inputs == [{
        "hash": "tx_hash_1",
        "index": "tx_ix_1"
    }, {
        "hash": "tx_hash_2",
        "index": "tx_ix_2"
    }]
    assert body.change == "sender_address"
    assert body.outputs == [
        {
            "address": "receiver_address_1",
            "value": {
                "lovelace": 5_000_000
            },
            "datum": None
        },
        {
            "address": "receiver_address_2",
            "value": {
                "lovelace": 7_000_000
            },
            "datum": None
        }
    ]
    assert body.metadata_path == "path/to/metadata"


def test_calculate_min_utxo():
    receiver = "addr_testabc"

    value = Value()

    value.add_token_amount("lovelace", 13_000_000)
    value.add_token_amount("abc123.444444", 5_000_000)
    value.add_token_amount("def456.555555", 3_000_000)
    value.add_token_amount("def456.666666", 17_000_000)

    datum_path = "/path/to/datum"

    # cardano-cli transaction calculate-min-required-utxo \
    # --protocol-params-file path/to/protocol.json \
    # --tx-out "addr_testabc 13000000 lovelace + 5000000 abc123.444444 + 3000000 def456.555555 + 17000000 def456.666666" \
    # --tx-out-datum-embed-file /path/to/datum \

    assert TxBody.calculate_min_utxo(
        receiver, value, "path/to/protocol.json", datum_path) == "\n".join([
            "cardano-cli transaction calculate-min-required-utxo \\",
            "--protocol-params-file path/to/protocol.json \\",
            '--tx-out "addr_testabc 13000000 lovelace + 5000000 abc123.444444 + 3000000 def456.555555 + 17000000 def456.666666" \\',
            "--tx-out-datum-embed-file /path/to/datum"
        ])