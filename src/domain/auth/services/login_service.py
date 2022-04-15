from fastapi_jwt_auth.auth_jwt import AuthJWT
from datetime import timedelta
from decouple import config
from src.domain.users.models.user_model import UserModel

from src.shared.exceptions import ForbiddenException

from src.domain.users.repositories.user_repository import UserRepository

from src.domain.auth.models.signin_models import (
    AuthAccessTokenModel,
    CredentialModel,
    SigninUserModel,
    SigninModel,
)


class LoginService:

    def __init__(self,repository: UserRepository):
        self._repository = repository

    def login(self, credential_model: CredentialModel, Authorize: AuthJWT) -> SigninModel:
        payload = self._login(credential_model, Authorize)
        return payload
    
    def refresh_token(self,authorize: AuthJWT) -> AuthAccessTokenModel:
        current_user = authorize.get_jwt_subject()
        expires = timedelta(days=1)
        new_access_token = authorize.create_access_token(subject=current_user, expires_time=expires)
        return AuthAccessTokenModel(access_token=new_access_token)
    
    def _login(self, credential_model: CredentialModel, Authorize: AuthJWT) -> SigninModel:
        
        user = self._make_validations(credential_model)
        expires = timedelta(days=1)
        expires_refresh = timedelta(days=7)
        access_token = Authorize.create_access_token(subject=user.id, expires_time=expires)
        refresh_token = Authorize.create_refresh_token(subject=user.id, expires_time=expires_refresh)
        payload_user = SigninUserModel(
            id=user.id,
            name=user.name,
            cpf=user.cpf
        )
        payload = SigninModel(
            access_token=access_token,
            refresh_token=refresh_token,
            user=payload_user
        )
        return payload

    def _make_validations(self, credential_model: CredentialModel) -> UserModel:
        user = self._repository.find(cpf = credential_model.cpf)
        if not user:
            raise ForbiddenException(message='Usuário ou senha incorretos')

        if credential_model.password != user.password:
            raise ForbiddenException(message='Usuário ou senha incorretos')

        return user