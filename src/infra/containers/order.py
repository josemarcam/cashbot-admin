from dependency_injector import containers, providers

from src.domain.orders.services.order_service import OrderService


class OrderContainer(containers.DeclarativeContainer):

    order_repository = providers.Dependency()

    order_service = providers.Factory(
        OrderService,
        repository=order_repository
    )
