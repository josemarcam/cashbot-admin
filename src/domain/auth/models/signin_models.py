from pydantic import BaseModel


class SigninUserModel(BaseModel):
    id: int
    name: str
    cpf: str
    
    class Config:
        orm_mode=True
    
class CredentialModel(BaseModel):
    cpf: str
    password: str

class SigninModel(BaseModel):
    access_token: str
    refresh_token: str
    user: SigninUserModel
    
    class Config:
        orm_mode=True

class AuthAccessTokenModel(BaseModel):
    access_token: str