from dependency_injector import containers, providers

from src.domain.users.services import UserService
from src.domain.users.repositories.user_repository import UserRepository


class UserContainer(containers.DeclarativeContainer):

    user_repository = providers.Dependency()

    user_service = providers.Factory(
        UserService,
        repository=user_repository
    )
