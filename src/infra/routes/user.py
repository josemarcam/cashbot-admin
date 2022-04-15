from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from dependency_injector.wiring import inject, Provide
from src.config.containers import Container
from src.domain.users.models.user_model import RequestUpdateUserModel, RequestUserModel
from src.domain.users.services.user_service import UserService

# Entrypoint /user/
router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {'description': 'Not found'}},
)

@router.get("/me")
@inject
def get_me(service: UserService = Depends(Provide[Container.user_container.user_service]), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    request_model = RequestUserModel(id=current_user)
    user_model = service.find(request_model=request_model)
    return user_model.dict(exclude={"password"})

@router.put("/consume-balance")
@inject
def consume_balance(request_update_model: RequestUpdateUserModel,service: UserService = Depends(Provide[Container.user_container.user_service]), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    request_update_model.id = current_user
    return service.consume_balance(request_update_model)