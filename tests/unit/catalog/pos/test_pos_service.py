import math
import pytest
from src.domain.catalog.models import CreatePosModel, PosModel, RequestPosModel, UpdatePosStateModel
from src.shared.models import (
    RequestOrdenationModel,
    RequestPaginationModel
)
from src.domain.catalog.services import PosService
from src.domain.catalog.repositories import (
    PosRepository,
    ProjectCatalogRepository,
    PlatformCatalogRepository,
    WhiteLabelCatalogRepository
)
from src.shared.exceptions import NotFoundException, ValidationException
from tests.fixtures import (
    get_new_pos,
    base_pos_dict,
    get_new_project_catalog,
    get_new_platform_catalog,
    get_new_white_label_catalog
)

def _get_services():
    return PosService(PosRepository(), ProjectCatalogRepository(), PlatformCatalogRepository(), WhiteLabelCatalogRepository())

def test_create_pos(app):

    pos_dict = base_pos_dict()
    create_pos_model = CreatePosModel(**pos_dict)

    service = _get_services()

    pos_model = service.create(create_pos_model=create_pos_model)
    assert type(pos_model)==PosModel
    assert pos_model.provider.name==create_pos_model.provider.name

def test_get_single_pos(app):

    initial_pos = get_new_pos()
    service = PosService(PosRepository(), ProjectCatalogRepository(), PlatformCatalogRepository(), WhiteLabelCatalogRepository())
    request_model = RequestPosModel(id = initial_pos.id)
    pos_found = service.get(request_model)
    print(pos_found)
    assert pos_found.id==initial_pos.id
    assert pos_found.provider.name==initial_pos.provider.name

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

def test_update_pos(app):

    initial_pos = get_new_pos()
    service = _get_services()

    initial_pos.provider.name = "Janaina Alias"
    initial_pos_model = PosModel.from_orm(initial_pos)
    updated_pos = service.update(initial_pos_model)

    assert updated_pos.id == initial_pos.id
    assert updated_pos.provider.name == initial_pos.provider.name

    initial_pos_model.id = "60f8b500a916f6f81cd61f75"
    with pytest.raises(NotFoundException):
        updated_pos = service.update(initial_pos_model)

def test_update_state_pos(app):

    initial_pos = get_new_pos()
    service = _get_services()

    activate_model = UpdatePosStateModel(id=initial_pos.id,pos_state=True)
    deactivate_model = UpdatePosStateModel(id=initial_pos.id,pos_state=False)

    activated_pos = service.update_state(activate_model)

    assert activated_pos.id == initial_pos.id
    assert activated_pos.state == True

    deactivated_pos = service.update_state(deactivate_model)
    assert deactivated_pos.id == initial_pos.id
    assert deactivated_pos.state == False

    activate_model.id = "60f8b500a916f6f81cd61f75"
    with pytest.raises(NotFoundException):
        updated_pos = service.update_state(activate_model)

def test_delete_cost_pos(app):
    initial_pos = get_new_pos()

    service = _get_services()
    print(initial_pos.id)
    delete = service.delete_cost_pos(initial_pos.id)
    assert delete == True

def test_delete_pos_linked_on_project_catalog(app):
    initial_project_catalog = get_new_project_catalog()
    initial_pos = str(initial_project_catalog.pos[0].parent_pos.id)

    service = _get_services()
    with pytest.raises(ValidationException):
        delete = service.delete_cost_pos(initial_pos)

def test_delete_pos_linked_on_platform_catalog(app):
    initial_platform_catalog = get_new_platform_catalog()
    initial_pos = str(initial_platform_catalog.pos[0].parent_pos.id)

    service = _get_services()
    with pytest.raises(ValidationException):
        delete = service.delete_cost_pos(initial_pos)

def test_delete_pos_linked_on_white_label_catalog(app):
    initial_white_label_catalog = get_new_white_label_catalog()
    initial_pos = str(initial_white_label_catalog.pos[0].parent_pos.id)

    service = _get_services()
    with pytest.raises(ValidationException):
        delete = service.delete_cost_pos(initial_pos)

def _get_pagination(page,per_page,order_direction = 'desc',order_name = 'name',param = {}):

    pagination = RequestPaginationModel(page=page,per_page=per_page)
    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestPosModel(**param)

    service = _get_services()
    list = service.getList(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order)

    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total
