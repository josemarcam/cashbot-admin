from pydantic import BaseModel
from typing import List, Optional, Union


class CreateUserModel(BaseModel):

    mac: str
    name: str
    email: str
    key: str
    teste: str
    validity: str

class RequestUserModel(BaseModel):
    
    id:Optional[int] = None

class RequestUpdateUserModel(BaseModel):
    
    id: Optional[int] = None
    balance: int

class UserQrcodeModel(BaseModel):
    
    qrcode: str
    
    class Config:
        orm_mode = True

class UserModel(BaseModel):

    id:int
    mac: str
    name: str
    email: str
    cpf: str
    password: str
    balance: int
    key: str
    teste: str
    validity: str
    qrcode: Optional[UserQrcodeModel] = None

    class Config:
        orm_mode = True

class KafkaUpdateQrcodeModel(BaseModel):
    
    user_id:int
    qrcode:str