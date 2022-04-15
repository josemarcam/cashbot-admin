import pytest
import math
from src.domain.catalog.repositories import CommerceRepository
from src.domain.catalog.models import CreateCommerceModel, CommerceModel, RequestCommerceModel
from src.shared.models import (
    RequestOrdenationModel,
    RequestPaginationModel
)
from tests.fixtures import get_new_commerce, base_commerce_dict
from src.shared.exceptions import ValidationException

def test_create_commerce(app):
    commerce_dict = base_commerce_dict()
    create_commerce_model = CreateCommerceModel(**commerce_dict)
    commerce_repository = CommerceRepository()

    commerce_model = commerce_repository.create(create_commerce_model)
    assert type(commerce_model)==CommerceModel
    assert commerce_model.provider.name == create_commerce_model.provider.name

def test_find_single_commerce(app):
    initial_commerce = get_new_commerce()

    commerce_repository = CommerceRepository()
    request_commerce_model = RequestCommerceModel(id=initial_commerce.id)
    commerce_found = commerce_repository.find_commerce(request_commerce_model)

    assert commerce_found.id==initial_commerce.id

    request_commerce_model = RequestCommerceModel(provider__id=initial_commerce.provider.id)
    commerce_found = commerce_repository.find_commerce(request_commerce_model)
    assert commerce_found.id==initial_commerce.id

    request_commerce_model = RequestCommerceModel(id="60f8b500a916f6f81cd61f75")
    commerce_found = commerce_repository.find_commerce(request_commerce_model)

    assert commerce_found==None

def test_update_commerce(app):

    initial_commerce = get_new_commerce()
    commerce_repository = CommerceRepository()
    commerce_model = CommerceModel.from_orm(initial_commerce)
    commerce_model.provider.name = "Arlindo Ferreira"
    updated_commerce_model = commerce_repository.update_commerce(commerce_model)

    assert updated_commerce_model.id == commerce_model.id
    assert updated_commerce_model.provider.name == commerce_model.provider.name

    commerce_model.id = "60f8b500a916f6f81cd61f75"
    with pytest.raises(ValidationException):
        updated_commerce_model = commerce_repository.update_commerce(commerce_model)

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

def _get_pagination(page,per_page,order_direction = 'desc',order_name = 'name',param = {}):

    pagination = RequestPaginationModel(page=page,per_page=per_page)
    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestCommerceModel(**param)

    repository = CommerceRepository()
    list = repository.list_commerce(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order)

    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total
