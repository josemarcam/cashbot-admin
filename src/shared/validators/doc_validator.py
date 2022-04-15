# from validate_docbr import CPF, CNPJ
# import json


# class DocValidator:

#     def __init__(self, value=None):
#         self._value = value

#     @property
#     def value(self):
#         return self._value

#     @value.setter
#     def value(self, value):
#         self._value = value

#     def cpf_validator(self):
#         return CPF().validate(self._value)

#     def cnpj_validator(self):
#         return CNPJ().validate(self._value)

#     def doc_validator(self):
#         return self.cpf_validator() or self.cnpj_validator()
