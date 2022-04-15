from src.domain.users.repositories.user_repository import UserRepository
from src.shared.exceptions import NotFoundException, ValidationException

from src.domain.users.models.user_model import RequestUpdateUserModel, UserModel, RequestUserModel

class UserService:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def find(self, request_model: RequestUserModel) -> UserModel:
        user_model = self._repository.find(request_model.id)
        if not user_model:
            raise NotFoundException(message="User não encontrado")
        return user_model
    
    def update_qrcode(self, user_id: int, qrcode: str) -> UserModel:
        user_model = self._repository.update_qrcode(user_id = user_id, qrcode = qrcode)
        return user_model
    
    def consume_balance(self, request_update_model: RequestUpdateUserModel) -> UserModel:
        request_model = RequestUserModel(id = request_update_model.id)
        user_model = self.find(request_model)
        
        if request_update_model.balance > user_model.balance or request_update_model.balance <= 0:
            raise NotFoundException(message="Numero de tokens invalido")
        request_update_model.balance = user_model.balance - request_update_model.balance
        user_model = self._repository.update_user(request_update_model)
        return user_model
    
    def update_user(self, request_update_model: RequestUpdateUserModel) -> UserModel:
        request_model = RequestUserModel(id = request_update_model.id)
        user_model = self.find(request_model)
        
        if request_update_model.balance > user_model.balance:
            raise NotFoundException(message="Numero de tokens invalido")

        user_model = self._repository.update_user(request_update_model)
        return user_model