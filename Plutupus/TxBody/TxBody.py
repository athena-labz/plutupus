from __future__ import annotations

import logging

from typing import Any

from Plutupus.Types.TxOutRef import TxOutRef
from Plutupus.Types.Value import Value


class TxBody(object):

    def __init__(self):
        # utxo {"hash": <txid>, "index": <txix>}
        self.collateral = None

        # list of utxos {"hash": <txid>, "index": <txix>}
        self.inputs: list[dict[str, str]] = []

        # bech32 address of the person who will receive the remaining ADA
        self.change = None

        # pubkeyhash
        self.required_signer = None

        self.outputs: list[dict] = []

        self.mint_scripts: list[dict[str, str]] = []
        self.mint_value = None

        self.metadata_path = None

    def set_collateral(self, txhash: str, txix: str):
        if self.collateral is not None:
            logging.warning(
                "Replacing existing collateral "
                f"{self.collateral['hash']}#{self.collateral['index']} "
                f"with {txhash}#{txix}"
            )

        self.collateral = {
            "hash": txhash,
            "index": txix
        }

    def add_input(self, txhash: str, txix: str):
        self.inputs.append({
            "type": "no-script",
            "hash": txhash,
            "index": txix
        })

    def add_script_input(self, txhash: str, txix: str, script_path: str,
                         redeemer_path: str, datum_path: str):
        self.inputs.append({
            "type": "script",
            "hash": txhash,
            "index": txix,
            "script": script_path,
            "redeemer": redeemer_path,
            "datum": datum_path
        })

    def set_change(self, addr: str):
        if self.change is not None:
            logging.warning(
                f"Replacing existing change address {self.change} {addr}")

        self.change = addr

    def set_required_signer(self, pubkeyhash: str):
        self.required_signer = pubkeyhash

    def add_output(self, receiver: str, value: Value):
        self.outputs.append({
            "type": "no-script",
            "address": receiver,
            "value": value.get()
        })

    def add_output_with_datum(self, receiver: str, value: Value, datum_path: str):
        self.outputs.append({
            "type": "script",
            "address": receiver,
            "value": value.get(),
            "datum": datum_path
        })

    def add_mint_script(self, script_path: str, redeemer_path: str):
        self.mint_scripts.append({
            "script": script_path,
            "redeemer": redeemer_path
        })

    def set_mint_value(self, value: Value):
        self.mint_value = value.get()

    def set_metadata(self, metadata_path: str):
        self.metadata_path = metadata_path

    def get(self) -> dict[str, Any]:
        return {
            "collateral": self.collateral,
            "inputs": self.inputs,
            "change": self.change,
            "required_signer": self.required_signer,
            "outputs": self.outputs,
            "mint_scripts": self.mint_scripts,
            "mint_value": self.mint_value
        }

    def cli(self, magic: str, protocol_parameters_file: str, out_file: str,
            cddl_mode: bool = False) -> str:
        # Make sure our cli is valid (at least the validations
        # we can do without a node)

        # See if we have the minimum arguments (input, output, change)
        if self.inputs == [] or self.outputs == [] or self.change is None:
            raise ValueError(
                "Transaction missing one of the required parameters: input, output or change")

        # If we have any script, make sure we also have a collateral
        if self.collateral is None and \
                (any([_input["type"] == "script" for _input in self.inputs]) or
                 any([output["type"] == "script" for output in self.outputs])):
            raise ValueError(
                "Transaction has scripts, but collateral is not set!")

        # If we have mint scripts but no mint value should fail
        if self.mint_scripts != [] and self.mint_value is None:
            raise ValueError("Mint script added, but no mint value defined!")

        inputs = []
        for _input in self.inputs:
            inputs.append(f"--tx-in {_input['hash']}#{_input['index']} \\")
            if "script" in _input and "redeemer" in _input and "datum" in _input:
                inputs.append(f"    --tx-in-script-file {_input['script']} \\")
                inputs.append(
                    f"    --tx-in-redeemer-file {_input['redeemer']} \\")
                inputs.append(f"    --tx-in-datum-file {_input['datum']} \\")

        outputs = []
        for output in self.outputs:
            tokens = []
            for asset, amount in output["value"].items():
                tokens.append(f"{amount} {asset}")

            parsed_tokens = " + ".join(tokens)

            outputs.append(
                f"--tx-out \"{output['address']} {parsed_tokens}\" \\")
            if "datum" in output:
                outputs.append(
                    f"    --tx-out-datum-embed-file {output['datum']} \\")

        mints = []
        if self.mint_value is not None:
            tokens = []
            for asset, amount in self.mint_value.items():
                tokens.append(f"{amount} {asset}")

            parsed_tokens = " + ".join(tokens)

            mints.append(f"--mint=\"{parsed_tokens}\" \\")

            for item in self.mint_scripts:
                mints.append(f"    --mint-script-file {item['script']} \\")
                mints.append(f"    --mint-redeemer-file {item['redeemer']} \\")

        required_signer_hash = []
        if self.required_signer:
            required_signer_hash.append(
                f"--required-signer-hash {self.required_signer} \\")

        collateral = []
        if self.collateral:
            collateral.append(
                f"--tx-in-collateral {self.collateral['hash']}#{self.collateral['index']} \\")

        metadata = []
        if self.metadata_path:
            metadata.append(f"--metadata-json-file {self.metadata_path} \\")

        cli_body = "\n".join(map(lambda x: "    " + x, [
            f"--cddl-format \\" if cddl_mode else f"--cli-format \\",
            f"--testnet-magic {magic} \\",
            *inputs,
            *required_signer_hash,
            *collateral,
            *outputs,
            f"--change-address {self.change} \\",
            *mints,
            *metadata,
            f"--protocol-params-file {protocol_parameters_file} \\",
            f"--out-file {out_file}"
        ]))

        return "\n".join([
            "cardano-cli transaction build \\",
            cli_body
        ])

    @staticmethod
    def send_to_address(input_utxo: str, input_address: str,
                        output_address: str, value: Value) -> TxBody:
        body = TxBody()

        splitted = input_utxo.split("#")
        assert len(splitted) == 2

        tx_hash, tx_ix = splitted

        body.add_input(tx_hash, tx_ix)
        body.set_change(input_address)
        body.add_output(output_address, value)

        return body
