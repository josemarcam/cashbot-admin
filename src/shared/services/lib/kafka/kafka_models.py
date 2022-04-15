import json
from pydantic import BaseModel
from typing import Optional

class KafkaHeader(BaseModel):
    
    id: str
    label_code: Optional[str]
    application: str
    type: str

    @property
    def to_json(cls):
        dict_cls = cls.dict()
        return json.dumps(dict_cls)
    
class KafkaModel(BaseModel):
    
    header: KafkaHeader
    payload: dict
    
    @property
    def to_json(cls):
        dict_cls = cls.dict()
        return json.dumps(dict_cls)