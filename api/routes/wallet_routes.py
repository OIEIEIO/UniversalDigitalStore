from flask import Blueprint, request, jsonify
from UniversalDigitalStore.wallet import create_wallet, open_wallet, check_balance

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    wallet_name = data.get('wallet_name')
    wallet_password = data.get('wallet_password')
    result = create_wallet(wallet_name, wallet_password)
    return jsonify(result)

@wallet_bp.route('/open', methods=['POST'])
def open():
    data = request.get_json()
    wallet_name = data.get('wallet_name')
    wallet_password = data.get('wallet_password')
    result = open_wallet(wallet_name, wallet_password)
    return jsonify(result)

@wallet_bp.route('/balance', methods=['GET'])
def balance():
    result = check_balance()
    return jsonify(result)
