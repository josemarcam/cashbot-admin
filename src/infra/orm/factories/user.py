from factory import alchemy, Faker
from src.infra.orm.entities import User
from src.config.containers import Container

db = Container.db()

class UserFactory(alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = db.get_scopped_session()

    name = Faker('company', locale='pt_BR')
    mac = Faker('md5')
    email = Faker('ascii_company_email')
    cpf = "39990139822"
    password = Faker('md5')
    balance = Faker('random_element', elements=[10, 5])
    key = Faker('md5')
    teste = Faker('md5')
    validity = Faker('md5')
