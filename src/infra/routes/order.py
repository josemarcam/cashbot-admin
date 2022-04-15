from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from dependency_injector.wiring import inject, Provide
from src.config.containers import Container
from src.domain.orders.models.order_model import OrderModel, RequestOrderModel
from src.domain.orders.services.order_service import OrderService
from fastapi_pagination import Page, paginate, LimitOffsetPage

# Entrypoint /user/
router = APIRouter(
    prefix='/orders',
    tags=['orders'],
    responses={404: {'description': 'Not found'}},
)

@router.get("/{order_id}")
@inject
def get_order(order_id:int, service: OrderService = Depends(Provide[Container.order_container.order_service]), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    request_model = RequestOrderModel(user__id=current_user, id= order_id)
    order_model = service.find(request_model=request_model)
    return order_model

@router.get("/", response_model=LimitOffsetPage[OrderModel])
@inject
def get_my_orders(service: OrderService = Depends(Provide[Container.order_container.order_service]), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    order_model = service.find_list_by_user(current_user)
    return paginate(order_model)