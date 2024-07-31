#!/usr/bin/env python
from autctapi import *
import asyncio
from dataclasses import asdict

async def run_all_requests_example():
    # The following examples illustrate correct usage of the API in its 3 calls:
    # 1. "prove" - for which you need to provide the file location of the
    #    relevant private key; the proof will be returned in base64.
    # 2. "verify" - for which you need to pass in the proof in base64.
    # 3. "createkeys" - will store a new private key in a file and give the
    #    corresponding taproot address.

    # First, create a default config set:
    config = AutctConfig()

    # Here is where you can add specific settings for your environment,
    # by editing the `config` object. For example:
    #
    # config.rpc_port = 12345
    #
    # config.keysets = anothercontext:anotherkeysetfile
    #
    # etc.
    #
    # Examine the definition of the dataclass AutctConfig or look at
    # ~/.config/autct/default-config.toml for the full list.

    # parameters for "prove":
    # this is just an example; the private key 040404... stored in a file
    config.privkey_file_str = "privkey-four"

    proving_request = config.config_to_proof_req()
    proving_result = await rpc_request(asdict(config), "RPCProver.prove",
                                       proving_request)
    if proving_result["accepted"] == 0:
        print("Proving request successful!")
    else:
        if proving_result["accepted"] not in RPC_PROOF_ERRORCODES:
            print("Unrecognized error code from server!: {}".format(
                proving_result["accepted"]))
        else:
            print("Proving failed due to error: \n{}".format(
                RPC_PROOF_ERRORCODES[proving_result["accepted"]]))

    # The proof is now available in base64 encoding in the "proof" entry
    # in the json object that was returned from the server. (Note that it
    # is not automatically stored in the file `config.proof_file_str` ;
    # that is only done in the CLI client. If you need to store it, store it yourself.
    print("\nNow we try verifying the proof that we just created:\n")
    verifying_req = config.config_to_verify_req(proving_result["proof"])
    verifying_result = await rpc_request(asdict(config), "RPCProofVerifier.verify",
                                         verifying_req)
    if verifying_result["accepted"] not in RPC_VERIFY_ERRORCODES:
        print("Unrecognized error code from server!: {}".format(
            verifying_result["accepted"]))
    else:    
        print("Server response: \n{}".format(RPC_VERIFY_ERRORCODES[
            verifying_result["accepted"]]))

    # lastly we create a new key and taproot address;
    # specify a file location for the private key:
    config.privkey_file_str = "new-privkey"
    createkeys_request = config.config_to_createkeys_request()
    createkeys_result = await rpc_request(asdict(config),
                        "RPCCreateKeys.createkeys", createkeys_request)
    print("Server response: \n{}".format(
        RPC_CREATEKEYS_ERRORCODES[createkeys_result["accepted"]]))
    if createkeys_result["accepted"] == 0:
        print("The server generated this address: {}, "
              "and stored the corresponding private key in {}".format(
                  createkeys_result["address"],
                  createkeys_result["privkey_file_loc"]))

# Just run the sample requests if this file is executed:
asyncio.run(run_all_requests_example())
   
                     
                        

