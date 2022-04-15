from typing import Union
from bson.objectid import ObjectId
import re

def set_query_params(request_model):

        params_list = {}
        for param, value in request_model:
            if value:
                if param == "children_account":
                    params_list["account_id"] = {"$in":value}
                else:
                    if "__" in param:
                        if param != "end_client_id":
                            model, attr = param.rsplit("__",1)
                            if ObjectId.is_valid(value):
                                params_list[f"{model}.{attr}"] = ObjectId(value)
                            else:
                                if type(value) == str:
                                    params_list[f"{model}.{attr}"] = re.compile(value, re.IGNORECASE)
                                else:
                                    params_list[f"{model}.{attr}"] = value

                        else:
                            if type(value) == str:
                                params_list[param] = re.compile(value, re.IGNORECASE)
                            else:
                                params_list[param] = value
                    else:
                        if param == "id":
                            params_list["_id"] = ObjectId(value)
                        else:
                            if ObjectId.is_valid(value):
                                params_list[param] = ObjectId(value)
                            else:
                                if type(value) == str:
                                    params_list[param] = re.compile(value, re.IGNORECASE)
                                else:
                                    params_list[param] = value

        return params_list

def sanitize_entity_dict(entity_dict,entity) -> Union[list,dict]:

    if type(entity_dict) == list:
        dict_list = []
        for single_dict in entity_dict:
            single_dict['id'] = single_dict['_id']
            single_dict.pop("_id")
            dict_list.append(entity(**single_dict))
        return dict_list
    else:
        entity_dict['id'] = entity_dict['_id']
        entity_dict.pop("_id")
        return entity(**entity_dict)



