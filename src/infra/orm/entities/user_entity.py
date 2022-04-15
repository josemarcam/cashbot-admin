from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.config.database import base_entity

class User(base_entity):
 
    __tablename__ = "user"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    mac = Column('mac', String(120), nullable=True, unique=True)
    name = Column('name', String, index=True, nullable=False)
    email = Column('email', String(120), nullable=False, unique=True)
    cpf = Column('cpf', String(120), nullable=False, unique=True)
    password = Column('password', String(120), nullable=False)
    balance = Column('balance', Integer, nullable=False)
    key = Column('key', String(120), nullable=False, unique=True)
    teste = Column('teste', String(120), nullable=False, unique=True)
    validity = Column('validity', String(120), nullable=False, unique=True)
    qrcode = relationship("Qrcode", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")
    
    # created_at = Column('created_at', DateTime, nullable=False, server_default=func.now())
    # updated_at = Column('updated_at', DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
