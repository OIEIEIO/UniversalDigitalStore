from sqlalchemy import Column, Integer, String, Numeric, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    product_price = Column(Numeric, nullable=False)
    payment_address = Column(String, nullable=False)
    confirmations = Column(Integer, default=0)
    confirmed = Column(Boolean, default=False)
    canceled = Column(Boolean, default=False)  # New column for tracking canceled orders
    download_link = Column(String, nullable=True)  # New column for the download link

DATABASE_URL = "sqlite:///orders.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
