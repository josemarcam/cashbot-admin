from mongoengine.fields import ObjectId


class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId) and not type(v) == str:
            raise TypeError('ObjectId required')
        return str(v)
