from dependency_injector import containers, providers

from src.domain.auth.services.login_service import LoginService


class AuthContainer(containers.DeclarativeContainer):

    user_repository = providers.Dependency()

    login_service = providers.Factory(
        LoginService,
        repository=user_repository
    )
