from enum import Enum

class BaseEnum(Enum):

    @classmethod
    def as_list(cls) -> list:
        return list(map(lambda c: c.value, cls))