from pydantic import BaseModel


class CreateQrcodeModel(BaseModel):

    qrcode: str
    user_id: int

class QrcodeUserModel(BaseModel):
    
    id: int
    mac: str
    name: str

    class Config:
        orm_mode = True

class QrcodeModel(BaseModel):
    
    qrcode: str
    user: QrcodeUserModel

    class Config:
        orm_mode = True

class QrcodeKafkaModel(BaseModel):
    
    qrcode: str
