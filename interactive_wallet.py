import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/wallet"

def create_wallet():
    wallet_name = input("Enter wallet name: ")
    wallet_password = input("Enter wallet password: ")
    payload = {
        "wallet_name": wallet_name,
        "wallet_password": wallet_password
    }
    response = requests.post(f"{BASE_URL}/create", json=payload)
    
    # Print response for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format")

def open_wallet():
    wallet_name = input("Enter wallet name: ")
    wallet_password = input("Enter wallet password: ")
    payload = {
        "wallet_name": wallet_name,
        "wallet_password": wallet_password
    }
    response = requests.post(f"{BASE_URL}/open", json=payload)
    
    # Print response for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format")

def check_balance():
    response = requests.get(f"{BASE_URL}/balance")
    
    # Print response for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format")

def add_product():
    product_id = input("Enter product ID: ")
    product_name = input("Enter product name: ")
    product_price = float(input("Enter product price (in XMR): "))
    product = {
        "id": product_id,
        "name": product_name,
        "price": product_price
    }
    # Assuming you have an endpoint to add products
    response = requests.post("http://127.0.0.1:5000/api/products", json=product)
    
    # Print response for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format")

def main():
    while True:
        print("1. Create Wallet")
        print("2. Open Wallet")
        print("3. Check Balance")
        print("4. Add Product")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            create_wallet()
        elif choice == '2':
            open_wallet()
        elif choice == '3':
            check_balance()
        elif choice == '4':
            add_product()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
