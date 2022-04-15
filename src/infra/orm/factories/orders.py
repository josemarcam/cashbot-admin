from factory import alchemy, Faker, SubFactory
from src.domain.orders.models.enum.order_status import OrderStatus
from src.infra.orm.entities import Order
from src.infra.orm.factories import ProductsFactory, UserFactory
from src.config.containers import Container

db = Container.db()

class OrdersFactory(alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Order
        sqlalchemy_session = db.get_scopped_session()

    status = Faker('random_element', elements=OrderStatus.as_list())
    quantity = Faker('lexify', text='?', letters='0123456789')
    product = SubFactory(ProductsFactory)
    user_id = 2