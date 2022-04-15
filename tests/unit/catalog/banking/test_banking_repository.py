import pytest
import math
from src.domain.catalog.repositories import UserRepository
from src.domain.catalog.models import CreateBankingModel, BankingModel, RequestBankingModel
from src.shared.models import (
    RequestOrdenationModel,
    RequestPaginationModel
)
from tests.fixtures import get_new_banking, base_banking_dict
from src.shared.exceptions import ValidationException

def test_create_banking(app):
    banking_dict = base_banking_dict()
    create_banking_model = CreateBankingModel(**banking_dict)
    user_repository = UserRepository()

    banking_model = user_repository.create(create_banking_model)
    assert type(banking_model)==BankingModel
    assert banking_model.provider.name == create_banking_model.provider.name

def test_find_single_banking(app):
    initial_banking = get_new_banking()

    user_repository = UserRepository()
    request_banking_model = RequestBankingModel(id=initial_banking.id)
    banking_found = user_repository.find_banking(request_banking_model)

    assert banking_found.id==initial_banking.id

    request_banking_model = RequestBankingModel(provider__id=initial_banking.provider.id)
    banking_found = user_repository.find_banking(request_banking_model)
    assert banking_found.id==initial_banking.id

    request_banking_model = RequestBankingModel(id="60f8b500a916f6f81cd61f75")
    banking_found = user_repository.find_banking(request_banking_model)

    assert banking_found==None

def test_update_banking(app):

    initial_banking = get_new_banking()
    user_repository = UserRepository()
    banking_model = BankingModel.from_orm(initial_banking)
    banking_model.provider.name = "Arlindo Ferreira"
    updated_banking_model = user_repository.update_banking(banking_model)

    assert updated_banking_model.id == banking_model.id
    assert updated_banking_model.provider.name == banking_model.provider.name

    banking_model.id = "60f8b500a916f6f81cd61f75"
    with pytest.raises(ValidationException):
        updated_banking_model = user_repository.update_banking(banking_model)

def test_list_banking(app):
    qtd = 13
    page = 1
    per_page = 5

    banking = []
    banking.append(get_new_banking())
    banking.append(get_new_banking())
    banking.append(get_new_banking())
    banking.append(get_new_banking())
    banking.append(get_new_banking())
    banking.append(get_new_banking())
    banking.append(get_new_banking())

    banking = sorted(banking, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination(page,per_page,order_name='_id')

    banking_filtered = banking

    assert len(results) == per_page
    assert count == len(banking_filtered)
    assert pages == math.ceil(len(banking_filtered) / per_page)

    banking_page = banking_filtered[:per_page]
    for banking in banking_page:
        results_index = results[banking_page.index(banking)]
        assert banking.id == results_index.id
def _get_pagination(page,per_page,order_direction = 'desc',order_name = 'name',param = {}):

    pagination = RequestPaginationModel(page=page,per_page=per_page)

    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestBankingModel(**param)

    repository = UserRepository()
    list = repository.list_banking(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order)

    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total
