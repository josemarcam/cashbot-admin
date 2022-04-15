from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import base_entity

class Order(base_entity):
 
    __tablename__ = "orders"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', ForeignKey('user.id'), nullable=False)
    product_id = Column('product_id', ForeignKey('products.id'), nullable=False)
    status = Column('status', String(120), nullable=False)
    quantity = Column('quantity', Integer, nullable=False)
    
    user = relationship("User", back_populates="orders", uselist=False)
    product = relationship("Products", back_populates="orders", uselist=False)
    
    created_at = Column('created_at', DateTime, nullable=False, server_default=func.now())
    updated_at = Column('updated_at', DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
