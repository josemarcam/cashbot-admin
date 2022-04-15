

from src.domain.orders.models.order_model import OrderModel, OrderPaginatedModel, RequestOrderModel
from src.domain.orders.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self,repository: OrderRepository):
        self._repository = repository
    
    def find(self, request_model: RequestOrderModel) -> OrderModel:
        return self._repository.find(**request_model.dict())
    
    def find_list_by_user(self, user_id:int) -> OrderPaginatedModel:
        return self._repository.find_list_by_user(user_id)
