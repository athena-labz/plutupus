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
            {"address": "receiver_address_1", "value": Value.lovelace(5_000_000)},
            {"address": "receiver_address_2", "value": Value.lovelace(7_000_000)}
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
    assert body.outputs == {
        "receiver_address_1": {
            "value": {
                "lovelace": 5_000_000
            },
            "datum": None
        },
        "receiver_address_2": {
            "value": {
                "lovelace": 7_000_000
            },
            "datum": None
        }
    }
    assert body.metadata_path == "path/to/metadata"
