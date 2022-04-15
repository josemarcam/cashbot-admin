from sqlalchemy.sql.elements import and_
from src.domain.users.models.user_model import UserModel
from src.domain.users.models.qrcode_model import CreateQrcodeModel, QrcodeModel
from src.infra.orm.entities.user_entity import User
from src.infra.orm.entities.qrcode_entity import Qrcode
from src.shared.repositories.base_repository import BaseRepository

class QrcodeRepository(BaseRepository):

    def find(self,id:int = None,**kwargs):
        
        query = self.session.query(User)
        if id:
            user_entity = query.filter(User.id == id).first()
        else:
            filter_list = []
            for key in kwargs.keys():
                filter_list.append(getattr(User, key) == kwargs[key])
            user_entity = query.filter(and_(True,*filter_list)).first()
        if user_entity:
            return UserModel.from_orm(user_entity)
        return None
    
    def create(self,create_qrcode_model: CreateQrcodeModel):

        qrcode_entity = Qrcode()
        for create_qrcode_model_field in list(create_qrcode_model.dict().keys()):
            setattr(qrcode_entity,create_qrcode_model_field,getattr(create_qrcode_model,create_qrcode_model_field))

        self.model = qrcode_entity
        self.save()
        return self.find(self.model.id)

    
    def update(self,qrcode_model:QrcodeModel):
        
        with self.session as session:
            query = session.query(Qrcode)

            qrcode_entity = query.filter(Qrcode.id == qrcode_model.id).first()
        
            for key in qrcode_model.dict_filters():
                setattr(qrcode_entity,key,getattr(qrcode_model,key))
        
            self.model = qrcode_entity
            self.save()

            return self.find(qrcode_model.id)