from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user
from UniversalDigitalStore.api.routes.product_routes import product_bp
from UniversalDigitalStore.api.routes.order_routes import order_bp
from UniversalDigitalStore.api.routes.wallet_routes import wallet_bp
from UniversalDigitalStore.api.routes.users import user_bp
from UniversalDigitalStore.wallet import open_wallet, get_block_height
from datetime import datetime
from UniversalDigitalStore.config import Config
from UniversalDigitalStore.data.products import PRODUCTS
from UniversalDigitalStore.data.models import User  # Ensure correct import path

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../ui/templates', static_folder='../static')
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user_bp.login'

    @login_manager.user_loader
    def load_user(user_id):
        user = db.session.query(User).get(user_id)
        print(f"Loaded user: {user}")
        return user

    # Register blueprints
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp)
    app.register_blueprint(wallet_bp, url_prefix='/api/wallet')
    app.register_blueprint(user_bp, url_prefix='/users')

    @app.route('/')
    def index():
        products = PRODUCTS
        block_height = request.args.get('block_height', 'N/A')
        timestamp = request.args.get('timestamp', 'N/A')
        status = request.args.get('status', 'Not Connected')
        return render_template('index.html', products=products, block_height=block_height, timestamp=timestamp, status=status)

    @app.route('/connect_wallet', methods=['POST'])
    def connect_wallet():
        wallet_name = "wallet1"
        wallet_password = "1234"
        open_wallet(wallet_name, wallet_password)

        block_height = get_block_height()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return redirect(url_for('index', block_height=block_height, timestamp=timestamp, status='Connected'))

    with app.app_context():
        db.create_all()  # Ensure the database is created if it doesn't exist

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
