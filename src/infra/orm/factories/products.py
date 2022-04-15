from factory import alchemy, Faker
from src.infra.orm.entities import Products
from src.config.containers import Container

db = Container.db()

class ProductsFactory(alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Products
        sqlalchemy_session = db.get_scopped_session()

    label = Faker('company', locale='pt_BR')
    price = Faker('pricetag')
    recurrent = Faker('boolean')
    active = Faker('boolean')