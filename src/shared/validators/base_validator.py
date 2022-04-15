from pydantic import ValidationError
import json

class BaseValidator:

    def __init__(self, validator):
        self._validator = validator
    
    @property
    def errors(self):
        return self._errors

    def is_valid(self, data):
        try:
            self._validator(**data)
            return True
        except ValidationError as e:

            self._errors = self.parse_error(e.json())

            return False
    
    def parse_error(self, json_error: str) -> dict:
        errors = json.loads(json_error)
        as_dict = {}

        for error in errors:
            key = error['loc'][0]

            if not key in as_dict:
                as_dict[key] = []

            error_info = { "type": error["type"], "msg": error["msg"] }    
            as_dict[key].append(error_info)

        return as_dict
