from typing import Union
from sqlalchemy.sql.elements import and_
from sqlalchemy.orm import joinedload
from src.domain.orders.models.order_model import CreateOrderModel, OrderModel, OrderPaginatedModel
from src.infra.orm.entities.orders_entity import Order
from src.infra.orm.entities.user_entity import User
from src.shared.repositories.base_repository import BaseRepository
from src.shared.exceptions import ValidationException

class OrderRepository(BaseRepository):

    def find(self,id:int = None,**kwargs) -> Union[OrderModel, None]:
        filter_list = []
        
        query = self.session.query(Order)
        if id:
            filter_list.append(Order.id == id )
        
        for key in kwargs.keys():
            try:
                entity, col = key.split("__",1)

                if entity == "order" and kwargs[key]:
                    entity = Order
                elif entity == "user" and kwargs[key]:
                    entity = User

                if kwargs[key] != None:
                    filter_list.append(getattr(entity,col) == kwargs[key] )
            except :
                raise ValidationException(
                    message="Não foi possivel processar parâmetro",
                    field=key,
                    field_message="Parâmetro inexistente",
                    validation_type="malformed_field"
                )
            print(filter_list[0])
            print(id)
            order_entity = query.join(
                Order.user
            ).options(
                joinedload(Order.user)
            ).filter(and_(True,*filter_list)).first()
        if order_entity:
            return OrderModel.from_orm(order_entity)
        return None
    
    def find_list_by_user(self, user_id, page: int = 1, per_page: int = 20) -> list:

        query = self.session.query(Order)

        order_list = query.join(
            Order.user
        ).options(
            joinedload(Order.user)
        ).options(
            joinedload(Order.product)
        ).filter(User.id == user_id).all()
        
        return [OrderModel.from_orm(order) for order in order_list]
    
    def create(self,create_order_model: CreateOrderModel):

        order_entity = Order()
        for create_order_model_field in list(create_order_model.dict().keys()):
            setattr(order_entity,create_order_model_field,getattr(create_order_model,create_order_model_field))

        self.model = order_entity
        self.save()
        return self.find(self.model.id)

    
    def update(self,order_model:OrderModel):
        
        with self.session as session:
            query = session.query(Order)

            order_entity = query.filter(Order.id == order_model.id).first()
        
            for key in list(order_model.dict().keys()):
                setattr(order_entity,key,getattr(order_model,key))
        
            self.model = order_entity
            self.save()

            return self.find(order_model.id)