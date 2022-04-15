from sqlalchemy import Column, Integer, String
from src.config.database import base_entity
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

class Qrcode(base_entity):
 
    __tablename__ = "qrcode"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    qrcode = Column('qrcode', String(120), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="qrcode", uselist=False)