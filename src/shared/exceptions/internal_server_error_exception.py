from http import HTTPStatus

from src.shared.exceptions.base_exception import BaseException


class InternalServerErrorException(BaseException):
    
    def __init__(self, message=None):
        
        message = message or HTTPStatus.INTERNAL_SERVER_ERROR.phrase

        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value)