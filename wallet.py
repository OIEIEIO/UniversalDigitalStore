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

def check_balance():
    response = rpc_request("get_balance")
    if response.get("result"):
        return response["result"]["balance"]
    else:
        raise Exception("Failed to get balance.")

def get_block_height():
    try:
        response = rpc_request("get_height")
        if response.get("result"):
            return response["result"]["height"]
        else:
            print("Failed to get block height.")
            return "N/A"
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return "N/A"
    except Exception as e:
        print(f"Error: {e}")
        return "N/A"

def create_subaddress(label):
    response = rpc_request("create_address", {"label": label})
    if response.get("result"):
        return response["result"]["address"]
    else:
        raise Exception("Failed to create subaddress")

def check_payment(address):
    try:
        response = rpc_request("get_transfers", {"in": True})
        if response.get("result"):
            for transfer in response["result"]["in"]:
                if transfer["address"] == address:
                    confirmations = transfer.get("confirmations", 0)
                    if confirmations >= 5:  # Change this to the required number of confirmations
                        return confirmations, "Payment confirmed."
                    else:
                        return confirmations, "Payment not confirmed."
        return 0, "No payment received."
    except Exception as e:
        print(f"Error checking payment: {e}")
        return 0, "Error checking payment."
