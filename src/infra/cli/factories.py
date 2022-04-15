import typer

from src.config.containers import Container
from src.infra.orm.factories.user import UserFactory
from src.infra.orm.factories.orders import OrdersFactory
from src.infra.orm.factories.products import ProductsFactory

app = typer.Typer()

container = Container()
db = Container.db()

def _persist_factory(list_entity):
    session = db.get_scopped_session()
    for entity in list_entity:
        session.add(entity)
    session.commit()
    return entity

def _generate_factory(Factory, persist, batch):
    if batch > 0:
        list_entity = Factory.build_batch(batch)
    else:
        list_entity = [Factory()]
    
    if persist:    
        print("persistindo no banco!")
        _persist_factory(list_entity)

@app.command()
def user_factory(persist:bool = False, batch: int = 0):
    _generate_factory(UserFactory, persist, batch)

@app.command()
def product_factory(persist:bool = False, batch: int = 0):
    _generate_factory(ProductsFactory, persist, batch)


@app.command()
def order_factory(persist:bool = False, batch: int = 0):
    _generate_factory(OrdersFactory, persist, batch)