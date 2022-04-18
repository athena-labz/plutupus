import pytest
from Plutupus import TxBody
from Plutupus.Types.TxOutRef import TxOutRef
from Plutupus.Types.Value import Value


def test_build_methods():
    body = TxBody()
    body.set_collateral("hash", "index")

    assert body.collateral == {
        "hash": "hash",
        "index": "index"
    }

    body.add_input("hash", "index")

    assert body.inputs == [{
        "type": "no-script",
        "hash": "hash",
        "index": "index",
    }]

    body.add_script_input("hash", "index", "script", "redeemer", "datum")

    assert body.inputs == [{
        "type": "no-script",
        "hash": "hash",
        "index": "index",
    }, {
        "type": "script",
        "hash": "hash",
        "index": "index",
        "script": "script",
        "redeemer": "redeemer",
        "datum": "datum"
    }]

    body.set_change("addr")

    assert body.change == "addr"

    body.set_required_signer("pkh")

    assert body.required_signer == "pkh"

    body.add_output("receiver", Value.lovelace(2_000_000))

    assert body.outputs == [{
        "type": "no-script",
        "address": "receiver",
        "value": {
            "lovelace": 2_000_000
        },
    }]

    body.add_output_with_datum("receiver", Value.lovelace(3_000_000), "datum")

    assert body.outputs == [{
        "type": "no-script",
        "address": "receiver",
        "value": {
            "lovelace": 2_000_000
        },
    }, {
        "type": "script",
        "address": "receiver",
        "value": {
            "lovelace": 3_000_000
        },
        "datum": "datum"
    }]

    body.add_mint_script("script", "redeemer")
    assert body.mint_scripts == [{
        "script": "script",
        "redeemer": "redeemer"
    }]

    body.set_mint_value(Value.lovelace(2_000_000))
    assert body.mint_value == {
        "lovelace": 2_000_000
    }

    body.set_metadata("metadata")
    assert body.metadata_path == "metadata"


# def test_get():
#     body = TxBody()

#     body.set_collateral("hash", "index")
#     body.add_input("hash", "index")
#     body.add_script_input("hash", "index", "script", "redeemer", "datum")
#     body.set_change("addr")
#     body.set_required_signer("pkh")
#     body.add_output("receiver", Value.lovelace(2_000_000))
#     body.add_output_with_datum("receiver", Value.lovelace(3_000_000), "datum")
#     body.add_mint_script("script", "redeemer")
#     body.set_mint_value(Value.lovelace(2_000_000))
#     body.set_metadata("metadata")

#     assert body.get() == {
#         "collateral": {
#             "hash": "hash",
#             "index": "index"
#         },
#         "inputs": [{
#             "type": "no-script",
#             "hash": "hash",
#             "index": "index",
#         }, {
#             "type": "script",
#             "hash": "hash",
#             "index": "index",
#             "script": "script",
#             "redeemer": "redeemer",
#             "datum": "datum"
#         }],
#         "change": "addr",
#         "required_signer": "pkh",
#         "outputs": [{
#             "type": "no-script",
#             "address": "receiver",
#             "value": {
#                 "lovelace": 2_000_000
#             },
#         }, {
#             "type": "script",
#             "address": "receiver",
#             "value": {
#                 "lovelace": 3_000_000
#             },
#             "datum": "datum"
#         }],
#         "mint_scripts": [{
#             "script": "script",
#             "redeemer": "redeemer"
#         }],
#         "mint_value": {
#             "lovelace": 2_000_000
#         }
#     }


# def test_cli():
#     # A body must have at the minimum: an input, an output and a change

#     # No input
#     body = TxBody()
#     body.add_output("receiver", Value.lovelace(2_000_000))
#     body.set_change("sender")

#     with pytest.raises(ValueError):
#         body.cli("42", "protocol_params", "out_file")

#     # No output
#     body = TxBody()
#     body.add_input("hash", "index")
#     body.set_change("sender")

#     with pytest.raises(ValueError):
#         body.cli("42", "protocol_params", "out_file")

#     # No change
#     body = TxBody()
#     body.add_input("hash", "index")
#     body.add_output("receiver", Value.lovelace(2_000_000))

#     with pytest.raises(ValueError):
#         body.cli("42", "protocol_params", "out_file")

#     # No collateral, but w/ script (should fail)
#     body = TxBody()
#     body.add_script_input("hash", "index", "script", "redeemer", "datum")
#     body.add_output("receiver", Value.lovelace(2_000_000))
#     body.set_change("sender")

#     with pytest.raises(ValueError):
#         body.cli("42", "protocol_params", "out_file")

#     # With mint script but without mint value
#     body = TxBody()
#     body.add_input("hash", "index")
#     body.add_output("receiver", Value.lovelace(2_000_000))
#     body.set_change("sender")
#     body.add_mint_script("script", "redeemer")

#     with pytest.raises(ValueError):
#         body.cli("42", "protocol_params", "out_file")

#     # Simplest working body
#     body = TxBody()
#     body.add_input("hash", "index")
#     body.add_output("receiver", Value.lovelace(2_000_000))
#     body.set_change("sender")

#     # cli format
#     assert body.cli("42", "protocol_params", "out_file") == "\n".join([
#         "cardano-cli transaction build \\",
#         "    --cli-format \\",
#         "    --testnet-magic 42 \\",
#         "    --tx-in hash#index \\",
#         "    --tx-out \"receiver 2000000 lovelace\" \\",
#         "    --change-address sender \\",
#         "    --protocol-params-file protocol_params \\",
#         "    --out-file out_file"
#     ])

#     # cddl format
#     assert body.cli("42", "protocol_params", "out_file", cddl_mode=True) == "\n".join([
#         "cardano-cli transaction build \\",
#         "    --cddl-format \\",
#         "    --testnet-magic 42 \\",
#         "    --tx-in hash#index \\",
#         "    --tx-out \"receiver 2000000 lovelace\" \\",
#         "    --change-address sender \\",
#         "    --protocol-params-file protocol_params \\",
#         "    --out-file out_file"
#     ])

#     # Body with everything combined
#     body = TxBody()
#     body.set_collateral("hash", "index")
#     body.add_input("hash1", "index1")
#     body.add_script_input("hash2", "index2", "script", "redeemer", "datum")
#     body.set_change("addr")
#     body.set_required_signer("pkh")
#     body.add_output("receiver", Value.lovelace(2_000_000))
#     body.add_output_with_datum("receiver", Value.lovelace(3_000_000), "datum")
#     body.add_mint_script("script", "redeemer")
#     body.set_mint_value(Value.lovelace(2_000_000))
#     body.set_metadata("metadata")

#     assert body.cli("42", "protocol_params", "out_file") == "\n".join([
#         "cardano-cli transaction build \\",
#         "    --cli-format \\",
#         "    --testnet-magic 42 \\",
#         "    --tx-in hash1#index1 \\",
#         "    --tx-in hash2#index2 \\",
#         "        --tx-in-script-file script \\",
#         "        --tx-in-redeemer-file redeemer \\",
#         "        --tx-in-datum-file datum \\",
#         "    --required-signer-hash pkh \\",
#         "    --tx-in-collateral hash#index \\",
#         "    --tx-out \"receiver 2000000 lovelace\" \\",
#         "    --tx-out \"receiver 3000000 lovelace\" \\",
#         "        --tx-out-datum-embed-file datum \\",
#         "    --change-address addr \\",
#         "    --mint=\"2000000 lovelace\" \\",
#         "        --mint-script-file script \\",
#         "        --mint-redeemer-file redeemer \\",
#         "    --metadata-json-file metadata \\",
#         "    --protocol-params-file protocol_params \\",
#         "    --out-file out_file"
#     ])