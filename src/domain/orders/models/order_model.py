from typing import List, Optional
from pydantic import BaseModel


class OrderProductModel(BaseModel):
    id: int
    label: str
    price: str
    recurrent: bool
    active: bool

    class Config:
        orm_mode = True

class OrderUserModel(BaseModel):
    id: int
    cpf: str
    balance: int

    class Config:
        orm_mode = True

class OrderModel(BaseModel):
    id: int
    status: str
    quantity: int
    user: OrderUserModel
    product: OrderProductModel

    class Config:
        orm_mode = True

class CreateOrderModel(BaseModel):

    status: str
    quantity: int
    user_id: int
    product_id: int

    class Config:
        orm_mode = True

class RequestOrderModel(BaseModel):
    id: int
    user__id: int
    order__status: Optional[str]


class OrderPaginatedModel(BaseModel):
    count: int
    pages: int
    results: Optional[List[OrderModel]]
