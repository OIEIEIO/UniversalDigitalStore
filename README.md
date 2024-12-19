
# Universal Digital Store - Work in Progress

A Flask-based digital store with Monero payment integration.

---

The Universal Digital Store is a comprehensive e-commerce platform designed for the digital age. This application allows users to purchase digital products securely and privately using Monero. The app not only sells various digital products but also offers the unique opportunity to resell the app itself, providing a robust global e-commerce solution.

## Features

- **Front End:** Built with HTML, CSS, and JavaScript for a responsive and user-friendly interface.
- **Back End:** Powered by Flask, a lightweight WSGI web application framework for Python.
- **Database:** Uses SQLite for storing product information, orders, and payment details.
- **Payment System:** Integrated with Monero's network for secure, private, and decentralized transactions.

## How It Works

### Front End

The front end of the Universal Digital Store is designed to be simple and intuitive. It includes the following pages:

- **Home Page:** Browse available products.
- **My Orders:** View and manage your current orders.
- **Purchased Products:** Access products you have already purchased and confirmed.

### Back End

The back end is built with Flask, providing the core logic for the application. The main components include:

- **Routes:** Define the different endpoints for the application.
- **Order Management:** Handles placing orders, checking confirmations, and downloading products.
- **Database Interaction:** Manages data storage and retrieval using SQLAlchemy for ORM (Object Relational Mapping).

### Database

The application uses SQLite for data storage. The database schema includes tables for:

- **Products:** Information about the digital products available for purchase.
- **Orders:** Tracks orders placed by users, including payment status and download links.

### Payment System

Payments are processed using Monero, ensuring secure and private transactions. The app checks for payment confirmations and updates order status accordingly.

## Usage

- **Browse Products:** Navigate to the home page to view available products.
- **Place an Order:** Select a product and follow the prompts to complete your purchase using Monero.
- **View Orders:** Check the "My Orders" page to see the status of your orders.
- **Download Products:** Once payment is confirmed, download your purchased products from the "Purchased Products" page.

## Customization

The Universal Digital Store can be customized to fit your specific needs. Choose from standard or advanced versions to allow for further customization, including adding new product categories and integrating additional payment methods.

### Empower Your Business
Deploying the Universal Digital Store means you have a powerful e-commerce tool at your fingertips. It’s designed to be easy to set up, manage, and scale, allowing you to focus on what matters most: growing your business and reaching new customers. By purchasing and hosting the app, you open the door to reselling the store, thus expanding your business opportunities even further.

- List available digital products
- Place and track orders

### Prerequisites

- Monero Wallet RPC server

```./monero-wallet-rpc --rpc-bind-ip 0.0.0.0 --rpc-bind-port 18088 --confirm-external-bind --daemon-address 127.0.0.1:18081 --log-file /wallet_rpc.log --disable-rpc-login --wallet-dir ./wallets```

## **Setup and Run Instructions**

### **1. Clone the Repository**

Clone the project from GitHub:
```
git clone https://github.com/OIEIEIO/UniversalDigitalStore.git
cd UniversalDigitalStore
```

2. Set Up a Virtual Environment
To isolate dependencies, create and activate a virtual environment:

Create the Virtual Environment:

```
python3 -m venv venv
```
Activate the Virtual Environment:
```
source venv/bin/activate
```
Verify Activation: The terminal prompt will show (venv).

3. Install Dependencies
Install the required dependencies:
```
pip install -r requirements.txt
```

4. Fix the Import Path
The project expects a package named UniversalDigitalStore. To resolve this:

Create a Symlink:
```
ln -s . UniversalDigitalStore
```
Set the PYTHONPATH Environment Variable:
```
export PYTHONPATH=$(pwd)
```
5. Initialize the Database
If this is your first time running the project, initialize the database:
```
python scripts/initialize_db.py
```
6. Run the Flask Application
Start the development server:
```
python run.py
```
By default, the app will run on:
```
URL: http://127.0.0.1:5000
```
Quick Setup Checklist
- Clone the repository ✅
- Set up and activate the virtual environment ✅
- Install all dependencies ✅
- Fix the Python import path ✅
- Initialize the database ✅
- Run the Flask application ✅

  
Development Notes
Dependencies: Make sure to activate the virtual environment before running any Python commands.

Debug Mode: This app runs in debug mode for development purposes. Use a production-ready WSGI server like gunicorn for deployment.

Static Assets: Ensure the static/ folder contains all required files (e.g., style.css, favicon.ico).

## Future Enhancements

Add production deployment instructions using gunicorn or uWSGI.

Improve database management for production environments.


## Contact
For any questions or feedback, please reach out to [support@oieieio.net].
