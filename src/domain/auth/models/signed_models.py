from pydantic import BaseModel


class SignedUserModel(BaseModel):
    id: int
    name: str
    cpf: str
