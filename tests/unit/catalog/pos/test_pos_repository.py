import pytest
import math
from src.domain.catalog.repositories import PosRepository
from src.domain.catalog.models import CreatePosModel, PosModel, RequestPosModel
from src.shared.models import (
    RequestOrdenationModel,
    RequestPaginationModel
)
from tests.fixtures import (
    get_new_pos,
    base_pos_dict,
    get_new_platform_catalog,
    get_new_project_catalog,
    get_new_white_label_catalog,
    get_new_end_client_catalog
)
from src.shared.exceptions import ValidationException

def test_create_pos(app):
    pos_dict = base_pos_dict()
    create_pos_model = CreatePosModel(**pos_dict)
    pos_repository = PosRepository()

    pos_model = pos_repository.create(create_pos_model)
    assert type(pos_model)==PosModel
    assert pos_model.provider.name == create_pos_model.provider.name

def test_find_single_pos(app):
    initial_pos = get_new_pos()

    pos_repository = PosRepository()
    request_pos_model = RequestPosModel(id=initial_pos.id)
    pos_found = pos_repository.find_pos(request_pos_model)

    assert pos_found.id==initial_pos.id

    request_pos_model = RequestPosModel(provider__id=initial_pos.provider.id)
    pos_found = pos_repository.find_pos(request_pos_model)
    assert pos_found.id==initial_pos.id

    request_pos_model = RequestPosModel(id="60f8b500a916f6f81cd61f75")
    pos_found = pos_repository.find_pos(request_pos_model)

    assert pos_found==None

def test_update_pos(app):

    initial_pos = get_new_pos()
    pos_repository = PosRepository()
    pos_model = PosModel.from_orm(initial_pos)
    pos_model.provider.name = "Arlindo Ferreira"
    updated_pos_model = pos_repository.update_pos(pos_model)

    assert updated_pos_model.id == pos_model.id
    assert updated_pos_model.provider.name == pos_model.provider.name

    pos_model.id = "60f8b500a916f6f81cd61f75"
    with pytest.raises(ValidationException):
        updated_pos_model = pos_repository.update_pos(pos_model)

def test_list_pos(app):
    qtd = 13
    page = 1
    per_page = 5

    pos = []
    pos.append(get_new_pos())
    pos.append(get_new_pos())
    pos.append(get_new_pos())
    pos.append(get_new_pos())
    pos.append(get_new_pos())
    pos.append(get_new_pos())
    pos.append(get_new_pos())

    pos = sorted(pos, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination(page,per_page,order_name='_id')



    pos_filtered = pos

    assert len(results) == per_page
    assert count == len(pos_filtered)
    assert pages == math.ceil(len(pos_filtered) / per_page)

    pos_page = pos_filtered[:per_page]

    for pos in pos_page:
        results_index = results[pos_page.index(pos)]
        assert pos.id == results_index.id

def test_delete_pos(app):
    pos_repository = PosRepository()

    initial_pos = get_new_pos()

    delete_pos = pos_repository.delete_pos(str(initial_pos.id))
    assert delete_pos == True

def test_delete_pos_not_found(app):
    pos_repository = PosRepository()

    delete_pos = pos_repository.delete_pos("60f8b500a916f6f81cd61f75")
    assert delete_pos == False

def test_list_pos_platform_catalog(app):
    page = 1
    per_page = 5
    level = 'Pos.PosPlatform'

    platform_catalogs = []

    for _ in range(25):
        platform_catalogs.append(get_new_platform_catalog())

    count_pos = 0
    list_pos = []
    for platform_catalog in platform_catalogs:
        count_pos += len(platform_catalog.pos)
        for pos in platform_catalog.pos:
            list_pos.append(pos.pos)

    platform_catalogs = sorted(list_pos, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination_pos_by_level(page, per_page, level, order_name='id')

    pos_platform_catalog_filtered = platform_catalogs

    pos_platform_catalog_page_1 = pos_platform_catalog_filtered[:per_page]

    assert len(results) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_platform_catalog_filtered) / per_page)

    for pos_platform_catalog in pos_platform_catalog_page_1:
        results_index = results[pos_platform_catalog_page_1.index(pos_platform_catalog)]
        assert str(pos_platform_catalog.id) == results_index.id

    page = 2
    results_page_2, pages, count = _get_pagination_pos_by_level(page, per_page, level, order_name='id')
    pos_platform_catalog_page_2 = pos_platform_catalog_filtered[per_page:per_page * 2]

    assert len(results_page_2) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_platform_catalog_filtered) / per_page)

    for pos_platform_catalog in pos_platform_catalog_page_2:
        results_index = results_page_2[pos_platform_catalog_page_2.index(pos_platform_catalog)]
        assert str(pos_platform_catalog.id) == results_index.id

def test_list_pos_project_catalog(app):
    page = 1
    per_page = 5
    level = 'Pos.PosProject'

    project_catalogs = []

    for _ in range(25):
        project_catalogs.append(get_new_project_catalog())

    count_pos = 0
    list_pos = []
    for project_catalog in project_catalogs:
        count_pos += len(project_catalog.pos)
        for pos in project_catalog.pos:
            list_pos.append(pos.pos)

    project_catalogs = sorted(list_pos, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination_pos_by_level(page, per_page, level,order_name='id')

    pos_project_catalog_filtered = project_catalogs

    pos_project_catalog_page_1 = pos_project_catalog_filtered[:per_page]

    assert len(results) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_project_catalog_filtered) / per_page)

    for pos_project_catalog in pos_project_catalog_page_1:
        results_index = results[pos_project_catalog_page_1.index(pos_project_catalog)]
        assert str(pos_project_catalog.id) == results_index.id

    page = 2
    results_page_2, pages, count = _get_pagination_pos_by_level(page, per_page, level, order_name='id')
    pos_project_catalog_page_2 = pos_project_catalog_filtered[per_page:per_page * 2]

    assert len(results_page_2) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_project_catalog_filtered) / per_page)

    for pos_project_catalog in pos_project_catalog_page_2:
        results_index = results_page_2[pos_project_catalog_page_2.index(pos_project_catalog)]
        assert str(pos_project_catalog.id) == results_index.id

def test_list_pos_white_label_catalog(app):
    page = 1
    per_page = 5
    level = 'Pos.PosWhiteLabel'

    white_label_catalogs = []

    for _ in range(25):
        white_label_catalogs.append(get_new_white_label_catalog())

    count_pos = 0
    list_pos = []
    for white_label_catalog in white_label_catalogs:
        count_pos += len(white_label_catalog.pos)
        for pos in white_label_catalog.pos:
            list_pos.append(pos.pos)

    white_label_catalogs = sorted(list_pos, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination_pos_by_level(page, per_page, level ,order_name='id')

    pos_white_label_catalog_filtered = white_label_catalogs

    pos_white_label_catalog_page_1 = pos_white_label_catalog_filtered[:per_page]

    assert len(results) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_white_label_catalog_filtered) / per_page)

    for pos_white_label_catalog in pos_white_label_catalog_page_1:
        results_index = results[pos_white_label_catalog_page_1.index(pos_white_label_catalog)]
        assert str(pos_white_label_catalog.id) == results_index.id

    page = 2
    results_page_2, pages, count = _get_pagination_pos_by_level(page, per_page, level, order_name='id')
    pos_white_label_catalog_page_2 = pos_white_label_catalog_filtered[per_page:per_page * 2]

    assert len(results_page_2) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_white_label_catalog_filtered) / per_page)

    for pos_white_label_catalog in pos_white_label_catalog_page_2:
        results_index = results_page_2[pos_white_label_catalog_page_2.index(pos_white_label_catalog)]
        assert str(pos_white_label_catalog.id) == results_index.id

def test_list_pos_end_client_catalog(app):
    page = 1
    per_page = 5
    level = 'Pos.PosEndClient'

    end_cleint_catalogs = []

    for _ in range(25):
        end_cleint_catalogs.append(get_new_end_client_catalog())

    count_pos = 0
    list_pos = []
    for end_client_catalog in end_cleint_catalogs:
        count_pos += len(end_client_catalog.pos)
        for pos in end_client_catalog.pos:
            list_pos.append(pos.pos)

    end_client_catalogs = sorted(list_pos, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination_pos_by_level(page, per_page, level ,order_name='id')

    pos_end_client_catalog_filtered = end_client_catalogs

    pos_end_client_catalog_page_1 = pos_end_client_catalog_filtered[:per_page]

    assert len(results) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_end_client_catalog_filtered) / per_page)

    for pos_end_client_catalog in pos_end_client_catalog_page_1:
        results_index = results[pos_end_client_catalog_page_1.index(pos_end_client_catalog)]
        assert str(pos_end_client_catalog.id) == results_index.id

    page = 2
    results_page_2, pages, count = _get_pagination_pos_by_level(page, per_page, level, order_name='id')
    pos_end_client_catalog_page_2 = pos_end_client_catalog_filtered[per_page:per_page * 2]

    assert len(results_page_2) == per_page
    assert count == count_pos
    assert pages == math.ceil(len(pos_end_client_catalog_filtered) / per_page)

    for pos_end_client_catalog in pos_end_client_catalog_page_2:
        results_index = results_page_2[pos_end_client_catalog_page_2.index(pos_end_client_catalog)]
        assert str(pos_end_client_catalog.id) == results_index.id

def test_list_cost_pos(app):
    page = 1
    per_page = 5
    level = 'Pos'

    cost_pos = []

    for _ in range(25):
        cost_pos.append(get_new_pos())

    cost_pos = sorted(cost_pos, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination_pos_by_level(page, per_page, level ,order_name='id')

    cost_pos_filtered = cost_pos

    cost_pos_page_1 = cost_pos_filtered[:per_page]

    assert len(results) == per_page
    assert count == len(cost_pos)
    assert pages == math.ceil(len(cost_pos_filtered) / per_page)

    for cost_pos_ in cost_pos_page_1:
        results_index = results[cost_pos_page_1.index(cost_pos_)]
        assert str(cost_pos_.id) == results_index.id

    page = 2
    results_page_2, pages, count = _get_pagination_pos_by_level(page, per_page, level, order_name='id')
    cost_pos_page_2 = cost_pos_filtered[per_page:per_page * 2]

    assert len(results_page_2) == per_page
    assert count == len(cost_pos)
    assert pages == math.ceil(len(cost_pos_filtered) / per_page)

    for cost_pos_ in cost_pos_page_2:
        results_index = results_page_2[cost_pos_page_2.index(cost_pos_)]
        assert str(cost_pos_.id) == results_index.id

""" paginações """
def _get_pagination(page,per_page,order_direction = 'desc',order_name = 'name',param = {}):

    pagination = RequestPaginationModel(page=page,per_page=per_page)
    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestPosModel(**param)

    repository = PosRepository()
    list = repository.list_pos(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order)

    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total

def _get_pagination_pos_by_level(page, per_page, level: str, order_direction = 'desc', order_name = 'name', param = {}):

    param['all_per_page'] = False
    pagination = RequestPaginationModel(page=page,per_page=per_page)
    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestPosModel(**param)

    repository = PosRepository()
    list = repository.list_pos_by_level(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order, level=level)

    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total
