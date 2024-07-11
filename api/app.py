from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .routes.product_routes import product_bp
from .routes.order_routes import order_bp
from .routes.wallet_routes import wallet_bp
from UniversalDigitalStore.wallet import open_wallet, get_block_height
from datetime import datetime
from UniversalDigitalStore.config import Config
from UniversalDigitalStore.data.products import PRODUCTS  # Import PRODUCTS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../ui/templates', static_folder='../static')
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate

    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp)  # No URL prefix here
    app.register_blueprint(wallet_bp, url_prefix='/api/wallet')

    @app.route('/')
    def index():
        products = PRODUCTS
        block_height = request.args.get('block_height', 'N/A')
        timestamp = request.args.get('timestamp', 'N/A')
        status = request.args.get('status', 'Not Connected')
        return render_template('index.html', products=products, block_height=block_height, timestamp=timestamp, status=status)

    @app.route('/connect_wallet', methods=['POST'])
    def connect_wallet():
        wallet_name = "test0"
        wallet_password = "1234"
        open_wallet(wallet_name, wallet_password)

        block_height = get_block_height()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return redirect(url_for('index', block_height=block_height, timestamp=timestamp, status='Connected'))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
