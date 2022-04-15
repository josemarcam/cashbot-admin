from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from dependency_injector.wiring import inject, Provide
from src.config.containers import Container
from src.domain.auth.models.signin_models import AuthAccessTokenModel, CredentialModel, SigninModel, SigninUserModel
from src.domain.auth.services.login_service import LoginService

# Entrypoint /auth/
router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {'description': 'Not found'}},
)

@router.post('/login', response_model=SigninModel)
@inject
def login(
    credential: CredentialModel,
    Authorize: AuthJWT = Depends(),
    service: LoginService = Depends(Provide[Container.auth_container.login_service])
):
    return service.login(credential, Authorize)

@router.get('/refresh-token', response_model=AuthAccessTokenModel)
@inject
def refresh_token(Authorize: AuthJWT = Depends(), service: LoginService = Depends(Provide(Container.auth_container.login_service))):
    Authorize.jwt_refresh_token_required()
    return service.refresh_token(Authorize)
