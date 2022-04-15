from http import HTTPStatus

from src.shared.exceptions.base_exception import BaseException


class ValidationException(BaseException):
    
    def __init__(self, message, field, field_message, validation_type):
        payload = {
            field: [
                {
                    "msg": field_message,
                    "type": validation_type
                }
            ]
        }

        super().__init__(message=message, status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value, payload=payload)
