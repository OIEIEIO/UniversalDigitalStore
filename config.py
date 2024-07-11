import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WALLET_RPC_URL = os.getenv("WALLET_RPC_URL")
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False