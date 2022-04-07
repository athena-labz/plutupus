from __future__ import annotations

from typing import List, Dict

from Plutupus.Types.TxOutRef import TxOutRef
from Plutupus.Types.Value import Value


class TxBody(object):

    def __init__(self, era, magic):
        self.era = era
        self.magic = magic

        self.setup()

    def setup(self):
        # utxo
        self.collateral = None

        # list of utxos
        self.inputs = []

        # address
        self.change = None

        # pubkeyhash
        self.required_signer = None

        # outputs
        self.outputs = {}

        # mint
        self.mint_scripts = []
        self.mint_value = {}

        self.metadata_path = None

    def add_collateral(self, txhash, txix):
        self.collateral = {
            "hash": txhash,
            "index": txix
        }

    def add_input(self, txhash, txix):
        self.inputs.append({
            "hash": txhash,
            "index": txix
        })

    def add_script_input(self, txhash, txix, script_path, redeemer_path, datum_path):
        self.inputs.append({
            "hash": txhash,
            "index": txix,
            "script": script_path,
            "redeemer": redeemer_path,
            "datum": datum_path
        })

    def add_change(self, addr):
        self.change = addr

    def add_required_signer(self, pubkeyhash):
        self.required_signer = pubkeyhash

    def add_output(self, receiver, value):
        self.outputs[receiver] = {
            "value": value.get(),
            "datum": None
        }

    def add_output_with_datum(self, receiver, value, datum_path):
        self.outputs[receiver] = {
            "value": value.get(),
            "datum": datum_path
        }

    def add_mint_script(self, script_path, redeemer_path):
        self.mint_scripts.append({
            "script": script_path,
            "redeemer": redeemer_path
        })

    def set_mint_value(self, value):
        self.mint_value = value.get()

    def set_metadata(self, metadata_path):
        self.metadata_path = metadata_path

    def get(self):
        return {
            "era": self.era,
            "magic": self.magic,
            "collateral": self.collateral,
            "inputs": self.inputs,
            "change": self.change,
            "required_signer": self.required_signer,
            "outputs": self.outputs,
            "mint_scripts": self.mint_scripts,
            "mint_value": self.mint_value
        }

    def cli(self, protocol_parameters_file, out_file):
        inputs = []
        for _input in self.inputs:
            inputs.append(f"--tx-in {_input['hash']}#{_input['index']} \\")
            if "script" in _input and "redeemer" in _input and "datum" in _input:
                inputs.append(f"--tx-in-script-file {_input['script']} \\")
                inputs.append(f"--tx-in-redeemer-file {_input['redeemer']} \\")
                inputs.append(f"--tx-in-datum-file {_input['datum']} \\")

        outputs = []
        for addr, output in self.outputs.items():
            tokens = []
            for asset, amount in output["value"].items():
                tokens.append(f"{amount} {asset}")

            parsed_tokens = " + ".join(tokens)

            outputs.append(f"--tx-out \"{addr} {parsed_tokens}\" \\")
            if output["datum"] is not None:
                outputs.append(
                    f"--tx-out-datum-embed-file {output['datum']} \\")

        tokens = []
        for asset, amount in self.mint_value.items():
            tokens.append(f"{amount} {asset}")

        mints = []
        if len(tokens) > 0:
            parsed_tokens = " + ".join(tokens)

            mints.append(f"--mint=\"{parsed_tokens}\" \\")

            for item in self.mint_scripts:
                mints.append(f"--mint-script-file {item['script']} \\")
                mints.append(f"--mint-redeemer-file {item['redeemer']} \\")

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

        cli_body = "\n".join(map(lambda x: "  " + x, [
            f"--cddl-format \\",
            f"--{self.era}-era \\",
            f"--testnet-magic {self.magic} \\",
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

    def sign(self, tx_body, skeys, out):
        parsed_keys = []
        for skey in skeys:
            parsed_keys.append(f"--signing-key-file {skey} \\")

        cli = "\n".join([
            "cardano-cli transaction sign \\",
            f"--tx-body-file {tx_body} \\",
            *parsed_keys,
            f"--testnet-magic {self.magic} \\",
            f"--out-file {out}"
        ])

        return cli

    def assemble(self, tx_body, tx_witness, out):
        cli = "\n".join([
            "cardano-cli transaction assemble \\",
            f"--tx-body-file {tx_body} \\",
            f"--witness-file {tx_witness} \\",
            f"--out-file {out}",
        ])

        return cli

    def submit(self, tx_sig):
        cli = "\n".join([
            "cardano-cli transaction submit \\",
            f"--tx-file {tx_sig} \\",
            f"--testnet-magic {self.magic}",
        ])

        return cli

    @staticmethod
    def build(era: str, magic: str, inputs: List[TxOutRef], change_address: str,
              outputs: List[Dict[str, str | Value]], metadata_path: str) -> TxBody:
        """
        Builds common shelley cardano transaction bodies given certain arguments.

        Args:
            era: The era in which this transaction should be built. (e.g. alonzo)
            magic: The current magic number. (e.g. 1097911063)
            inputs: The list of TxOutRef UTxOs that will be used as inputs
            change_address: The address that will receive the change
            outputs: The list of address, value of the receivers in the format {"address": <addr>, "value": <value>}
            metadata_path: The path for the metadata json file

        Returns:
            The corresponding TxBody
        """
        body = TxBody(era, magic)

        for _input in inputs:
            body.add_input(_input.tx_id, _input.tx_ix)
        
        body.add_change(change_address)

        for output in outputs:
            address: str = output["address"]
            value: Value = output["value"]

            body.add_output(address, value)

        body.set_metadata(metadata_path)

        return body
