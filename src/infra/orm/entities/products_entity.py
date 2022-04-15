from sqlalchemy import Column, Integer, String, Boolean, func, DateTime
from sqlalchemy.orm import relationship
from src.config.database import base_entity

class Products(base_entity):
 
    __tablename__ = "products"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    label = Column('label', String(120), nullable=False)
    price = Column('price', String(120), nullable=False)
    recurrent = Column('recurrent', Boolean, nullable=False)
    active = Column('active', Boolean)
    orders = relationship("Order", back_populates="product")
    
    created_at = Column('created_at', DateTime, nullable=False, server_default=func.now())
    updated_at = Column('updated_at', DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
