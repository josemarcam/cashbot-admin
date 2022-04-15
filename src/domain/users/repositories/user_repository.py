from typing import Union
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import and_
from src.domain.users.models.user_model import RequestUpdateUserModel, UserModel
from src.infra.orm.entities.user_entity import User
from src.shared.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):

    def find(self,id:int = None,**kwargs) -> Union[UserModel, None]:
        query = self.session.query(User)
        if id:
            user_entity = query.options(
                    joinedload(User.qrcode)
                ).filter(User.id == id).first()
        else:
            filter_list = []
            for key in kwargs.keys():
                filter_list.append(getattr(User, key) == kwargs[key])
            user_entity = query.options(
                    joinedload(User.qrcode)
                ).filter(and_(True,*filter_list)).first()
        if user_entity:
            return UserModel.from_orm(user_entity)
        return None
    
    def update_user(self,request_update_model: RequestUpdateUserModel):
        
        with self.session as session:
            query = session.query(User)

            user_entity = query.filter(User.id == request_update_model.id).first()
        
            for key in list(request_update_model.dict().keys()):
                setattr(user_entity,key,getattr(request_update_model,key))
        
            self.model = user_entity
            self.save()

            return self.find(request_update_model.id)