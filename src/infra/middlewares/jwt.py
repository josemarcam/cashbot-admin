from fastapi import Depends
from fastapi.param_functions import Header
from fastapi.security import HTTPBearer
import jwt
from decouple import config

from src.domain.users.models.user_model import RequestUserModel, UserModel
from src.domain.auth.models.signed_models import SignedUserModel

from src.shared.exceptions import UnauthorizedException, NotFoundException
from src.config.containers import Container

oauth2_scheme = HTTPBearer()
container = Container()

def validate_access_token(token: str = Depends(oauth2_scheme)) -> UserModel:

    SECRET_KEY = config('SECRET_KEY')
    USER_TOKEN = token.credentials

    payload = jwt.decode(USER_TOKEN, SECRET_KEY, algorithms=['HS256'])

    user_id: int = payload.get("sub")

    if not user_id:
        raise UnauthorizedException(message='Credenciais inválidas')
    request_model = RequestUserModel(id= user_id)
    current_user = container.user_container.user_service().find(request_model)

    if not current_user:
        raise NotFoundException(message='Usuário não encontrado')

    return SignedUserModel(**current_user.dict())

    