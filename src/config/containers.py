from dependency_injector import containers, providers
from src.config.database import DB
from src.domain.orders.repositories.order_repository import OrderRepository
from src.domain.users.repositories.user_repository import UserRepository

from src.infra.containers import UserContainer
from src.infra.containers.auth import AuthContainer
from src.infra.containers.order import OrderContainer

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    db = providers.Singleton(DB)
    user_repository = providers.Factory(UserRepository, db=db)
    order_repository = providers.Factory(OrderRepository, db=db)
    order_container = providers.Container(OrderContainer, order_repository=order_repository)
    user_container = providers.Container(UserContainer, user_repository=user_repository)
    auth_container = providers.Container(AuthContainer, user_repository=user_repository)


def init_app() -> Container:
    return Container()
