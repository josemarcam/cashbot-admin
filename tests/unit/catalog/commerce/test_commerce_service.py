import math
import pytest
from src.domain.catalog.models import CreateCommerceModel, CommerceModel, RequestCommerceModel, UpdateCommerceStateModel
from src.shared.models import (
    RequestOrdenationModel,
    RequestPaginationModel
)
from src.domain.catalog.services import CommerceService
from src.domain.catalog.repositories import CommerceRepository
from src.shared.exceptions import NotFoundException, ValidationException
from tests.fixtures import get_new_commerce, base_commerce_dict

def test_create_commerce(app):

    commerce_dict = base_commerce_dict()
    create_commerce_model = CreateCommerceModel(**commerce_dict)

    service = CommerceService(CommerceRepository())

    commerce_model = service.create(create_commerce_model=create_commerce_model)
    assert type(commerce_model)==CommerceModel
    assert commerce_model.provider.name==create_commerce_model.provider.name

def test_get_single_commerce(app):

    initial_commerce = get_new_commerce()
    service = CommerceService(CommerceRepository())
    request_model = RequestCommerceModel(id = initial_commerce.id)
    commerce_found = service.get(request_model)
    print(commerce_found)
    assert commerce_found.id==initial_commerce.id
    assert commerce_found.provider.name==initial_commerce.provider.name

def test_get_single_commerce_invalid_id(app):

    initial_commerce = get_new_commerce()
    service = CommerceService(CommerceRepository())
    request_model = RequestCommerceModel(id = "umidinvalido")
    with pytest.raises(ValidationException):
        commerce_found = service.get(request_model)

def test_list_commerce(app):
    qtd = 13
    page = 1
    per_page = 5
     
    commerce = [] 
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())

    commerce = sorted(commerce, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination(page,per_page,order_name='_id')

    commerce_filtered = commerce

    assert len(results) == per_page
    assert count == len(commerce_filtered)
    assert pages == math.ceil(len(commerce_filtered) / per_page)

    commerce_page = commerce_filtered[:per_page]
    for commerce in commerce_page:
        results_index = results[commerce_page.index(commerce)]
        assert commerce.id == results_index.id

def test_list_commerce_with_invalid_id(app):
    
    page = 1
    per_page = 5
     
    commerce = [] 
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())
    commerce.append(get_new_commerce())

    with pytest.raises(ValidationException):
        params = {"id":"umidinvalido"}
        results, pages, count = _get_pagination(page,per_page,order_name='id',param=params)

def test_update_commerce(app):
    
    initial_commerce = get_new_commerce()
    service = CommerceService(CommerceRepository())
    
    initial_commerce.provider.name = "Janaina Alias"
    initial_commerce_model = CommerceModel.from_orm(initial_commerce)
    updated_commerce = service.update(initial_commerce_model)
    
    assert updated_commerce.id == initial_commerce.id
    assert updated_commerce.provider.name == initial_commerce.provider.name

    initial_commerce_model.id = "60f8b500a916f6f81cd61f75"
    with pytest.raises(NotFoundException):
        updated_commerce = service.update(initial_commerce_model)
    
def test_update_state_commerce(app):
    
    initial_commerce = get_new_commerce()
    service = CommerceService(CommerceRepository())
    
    activate_model = UpdateCommerceStateModel(id=initial_commerce.id,commerce_state=True)
    deactivate_model = UpdateCommerceStateModel(id=initial_commerce.id,commerce_state=False)

    activated_commerce = service.update_state(activate_model)
    
    assert activated_commerce.id == initial_commerce.id
    assert activated_commerce.state == True
    
    deactivated_commerce = service.update_state(deactivate_model)
    assert deactivated_commerce.id == initial_commerce.id
    assert deactivated_commerce.state == False

    activate_model.id = "60f8b500a916f6f81cd61f75"
    with pytest.raises(NotFoundException):
        updated_commerce = service.update_state(activate_model)



def _get_pagination(page,per_page,order_direction = 'desc',order_name = 'name',param = {}):
    
    pagination = RequestPaginationModel(page=page,per_page=per_page)
    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestCommerceModel(**param)

    service = CommerceService(CommerceRepository())
    list = service.getList(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order)
    
    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total
