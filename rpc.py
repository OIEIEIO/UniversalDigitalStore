import requests
from UniversalDigitalStore.utils import rpc_request

def create_wallet(wallet_name, wallet_password):
    params = {
        "filename": wallet_name,
        "password": wallet_password,
        "language": "English"
    }
    return rpc_request("create_wallet", params)

def open_wallet(wallet_name, wallet_password):
    params = {
        "filename": wallet_name,
        "password": wallet_password
    }
    return rpc_request("open_wallet", params)

def get_block_height():
    response = rpc_request("get_height")
    if response.get("result"):
        return response["result"]["height"]
    else:
        raise Exception("Failed to get block height.")

def create_subaddress(label):
    response = rpc_request("create_address", {"label": label})
    if response.get("result"):
        return response["result"]["address"]
    else:
        raise Exception("Failed to create subaddress")

def check_payment(address):
    response = rpc_request("get_transfers", {"in": True})
    if response.get("result"):
        for transfer in response["result"]["in"]:
            if transfer["address"] == address:
                if transfer["confirmations"] >= 5:  # Change this to the required number of confirmations
                    return True, "Payment confirmed."
                else:
                    return False, "Payment not confirmed."
    return False, "No payment received."
