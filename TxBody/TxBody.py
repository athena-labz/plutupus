class TxBody(object):

    def __init__(self, era, magic):
        self.__era = era
        self.__magic = magic

        self.setup()

    def setup(self):
        # utxo
        self.__collateral = None

        # list of utxos
        self.__inputs = []

        # address
        self.__change = None

        # pubkeyhash
        self.__required_signer = None

        # outputs
        self.__outputs = {}

        # mint
        self.__mint_scripts = []
        self.__mint_value = {}

        self.__metadata_path = None

    def add_collateral(self, txhash, txix):
        self.__collateral = {
            "hash": txhash,
            "index": txix
        }

    def add_input(self, txhash, txix):
        self.__inputs.append({
            "hash": txhash,
            "index": txix
        })

    def add_script_input(self, txhash, txix, script_path, redeemer_path, datum_path):
        self.__inputs.append({
            "hash": txhash,
            "index": txix,
            "script": script_path,
            "redeemer": redeemer_path,
            "datum": datum_path
        })

    def add_change(self, addr):
        self.__change = addr

    def add_required_signer(self, pubkeyhash):
        self.__required_signer = pubkeyhash

    def add_output(self, receiver, value):
        self.__outputs[receiver] = {
            "value": value.get(),
            "datum": None
        }

    def add_output_with_datum(self, receiver, value, datum_path):
        self.__outputs[receiver] = {
            "value": value.get(),
            "datum": datum_path
        }

    def add_mint_script(self, script_path, redeemer_path):
        self.__mint_scripts.append({
            "script": script_path,
            "redeemer": redeemer_path
        })

    def set_mint_value(self, value):
        self.__mint_value = value.get()

    def set_metadata(self, metadata_path):
        self.__metadata_path = metadata_path

    def get(self):
        return {
            "era": self.__era,
            "magic": self.__magic,
            "collateral": self.__collateral,
            "inputs": self.__inputs,
            "change": self.__change,
            "required_signer": self.__required_signer,
            "outputs": self.__outputs,
            "mint_scripts": self.__mint_scripts,
            "mint_value": self.__mint_value
        }

    def cli(self, protocol_parameters_file, out_file):
        inputs = []
        for _input in self.__inputs:
            inputs.append(f"--tx-in {_input['hash']}#{_input['index']} \\")
            if "script" in _input and "redeemer" in _input and "datum" in _input:
                inputs.append(f"--tx-in-script-file {_input['script']} \\")
                inputs.append(f"--tx-in-redeemer-file {_input['redeemer']} \\")
                inputs.append(f"--tx-in-datum-file {_input['datum']} \\")

        outputs = []
        for addr, output in self.__outputs.items():
            tokens = []
            for asset, amount in output["value"].items():
                tokens.append(f"{amount} {asset}")

            parsed_tokens = " + ".join(tokens)

            outputs.append(f"--tx-out \"{addr} {parsed_tokens}\" \\")
            if output["datum"] is not None:
                outputs.append(
                    f"--tx-out-datum-embed-file {output['datum']} \\")

        tokens = []
        for asset, amount in self.__mint_value.items():
            tokens.append(f"{amount} {asset}")

        mints = []
        if len(tokens) > 0:
            parsed_tokens = " + ".join(tokens)

            mints.append(f"--mint=\"{parsed_tokens}\" \\")

            for item in self.__mint_scripts:
                mints.append(f"--mint-script-file {item['script']} \\")
                mints.append(f"--mint-redeemer-file {item['redeemer']} \\")

        required_signer_hash = []
        if self.__required_signer:
            required_signer_hash.append(
                f"--required-signer-hash {self.__required_signer} \\")

        collateral = []
        if self.__collateral:
            collateral.append(
                f"--tx-in-collateral {self.__collateral['hash']}#{self.__collateral['index']} \\")

        metadata = []
        if self.__metadata_path:
            metadata.append(f"--metadata-json-file {self.__metadata_path} \\")

        cli_body = "\n".join(map(lambda x: "  " + x, [
            f"--cddl-format \\",
            f"--{self.__era}-era \\",
            f"--testnet-magic {self.__magic} \\",
            *inputs,
            *required_signer_hash,
            *collateral,
            *outputs,
            f"--change-address {self.__change} \\",
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
            f"--testnet-magic {self.__magic} \\",
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
            f"--testnet-magic {self.__magic}",
        ])

        return cli
