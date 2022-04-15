from typing import Optional
from pydantic import BaseModel

class RequestPaginationModel(BaseModel):
    
    page:Optional[int] = 1
    per_page:Optional[int] = 10

class RequestOrdenationModel(BaseModel):
    
    order_direction:Optional[str] = "desc"
    order_name:Optional[str] = "_id"