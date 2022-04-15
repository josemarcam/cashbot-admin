import math
from bson.objectid import ObjectId
import pytest
from src.domain.catalog.models.platform_catalog_models import PlatformCatalogModel, RequestPlatformCatalogModel, RequestOrdenationModel, RequestPaginationModel, RequestUpdatePlatformCatalogModel
from src.domain.catalog.repositories.commerce_repository import CommerceRepository
from src.domain.catalog.repositories.pos_repository import PosRepository
from src.domain.catalog.repositories.platform_catalog_repository import PlatformCatalogRepository
from src.domain.catalog.services.platform_catalog_service import PlatformCatalogService
from tests.fixtures import base_catalog_dict, get_new_platform_catalog, get_new_commerce, get_new_pos
from src.domain.catalog.models import RequestCreatePlatformCatalogModel
from src.shared.exceptions import NotFoundException, ValidationException
def test_create_platform_catalog(app):

    platform_catalog_dict = base_catalog_dict()
    commerce = get_new_commerce()
    pos = get_new_pos()
    platform_catalog_dict['pos'][0]['parent_pos_id'] = pos.id
    platform_catalog_dict['commerce'][0]['parent_commerce_id'] = commerce.id
    create_platform_catalog_model = RequestCreatePlatformCatalogModel(**platform_catalog_dict)

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    platform_catalog_model = service.create(create_platform_catalog_model=create_platform_catalog_model)

    assert type(platform_catalog_model)==PlatformCatalogModel
    assert platform_catalog_model.pos[0].profit_share == platform_catalog_dict['pos'][0]['profit_share']

def test_create_platform_catalog_with_not_found_pos_parent(app):

    platform_catalog_dict = base_catalog_dict()
    commerce = get_new_commerce()
    pos = get_new_pos()
    platform_catalog_dict['pos'][0]['parent_pos_id'] = "60f8b500a916f6f81cd61f75"
    platform_catalog_dict['commerce'][0]['parent_commerce_id'] = commerce.id
    create_platform_catalog_model = RequestCreatePlatformCatalogModel(**platform_catalog_dict)

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    with pytest.raises(ValidationException):
        platform_catalog_model = service.create(create_platform_catalog_model=create_platform_catalog_model)

def test_create_platform_catalog_with_not_found_commerce_parent(app):

    platform_catalog_dict = base_catalog_dict()
    commerce = get_new_commerce()
    pos = get_new_pos()
    platform_catalog_dict['pos'][0]['parent_pos_id'] = pos.id
    platform_catalog_dict['commerce'][0]['parent_commerce_id'] = "60f8b500a916f6f81cd61f75"
    create_platform_catalog_model = RequestCreatePlatformCatalogModel(**platform_catalog_dict)

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    with pytest.raises(ValidationException):
        platform_catalog_model = service.create(create_platform_catalog_model=create_platform_catalog_model)

def test_get_platform_catalog(app):

    platform_catalog = get_new_platform_catalog()
    
    request_model = RequestPlatformCatalogModel(children_account=[1],id=platform_catalog.id)

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    platform_catalog_model = service.get(request_model=request_model)

    assert type(platform_catalog_model)==PlatformCatalogModel
    assert platform_catalog_model.id == platform_catalog.id
    

def test_list_platform_catalog(app):
    qtd = 13
    page = 1
    per_page = 5
     
    platform_catalogs = [] 
    platform_catalogs.append(get_new_platform_catalog())
    platform_catalogs.append(get_new_platform_catalog())
    platform_catalogs.append(get_new_platform_catalog())
    platform_catalogs.append(get_new_platform_catalog())
    platform_catalogs.append(get_new_platform_catalog())

    platform_catalogs = sorted(platform_catalogs, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination(page,per_page,order_name='_id')

    platform_catalog_filtered = platform_catalogs

    assert len(results) == per_page
    assert count == len(platform_catalog_filtered)
    assert pages == math.ceil(len(platform_catalog_filtered) / per_page)

    platform_catalog_page = platform_catalog_filtered[:per_page]
    for platform_catalog in platform_catalog_page:
        results_index = results[platform_catalog_page.index(platform_catalog)]
        assert platform_catalog.id == results_index.id

def test_update_catalog_client(app):
    
    platform_catalog = get_new_platform_catalog()

    platform_catalog_dict = {
        "pos":[],
        "commerce":[],
        "account_id":platform_catalog.account_id,
        "id":platform_catalog.id

    }
    for pos in platform_catalog.pos:
        pos_dict = {}
        pos_dict["pos"] = pos.pos.id
        pos_dict["parent_pos"] = pos.parent_pos.id
        pos_dict["profit_share"] = pos.profit_share
        platform_catalog_dict['pos'].append(pos_dict)

        
    for commerce in platform_catalog.commerce:
        commerce_dict = {}
        commerce_dict["commerce"] = commerce.commerce.id
        commerce_dict["parent_commerce"] = commerce.parent_commerce.id
        commerce_dict["profit_share"] = commerce.profit_share
        platform_catalog_dict['commerce'].append(commerce_dict)
    
    request_update_platform_catalog_model = RequestUpdatePlatformCatalogModel(**platform_catalog_dict)
    
    request_update_platform_catalog_model.pos[0].profit_share = 60.45

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    platform_catalog_updated = service.update(request_update_platform_catalog_model,[1])
    
    assert platform_catalog_updated.pos[0].profit_share == request_update_platform_catalog_model.pos[0].profit_share

def test_update_not_existing_catalog(app):
    
    platform_catalog = get_new_platform_catalog()
    pos_entity = get_new_pos()

    platform_catalog_dict = {
        "pos":[],
        "commerce":[],
        "account_id":platform_catalog.account_id,
        "id":platform_catalog.id

    }
    for pos in platform_catalog.pos:
        pos_dict = {}
        pos_dict["pos"] = pos.pos.id
        pos_dict["parent_pos"] = pos.parent_pos.id
        pos_dict["profit_share"] = pos.profit_share
        platform_catalog_dict['pos'].append(pos_dict)

        
    for commerce in platform_catalog.commerce:
        commerce_dict = {}
        commerce_dict["commerce"] = commerce.commerce.id
        commerce_dict["parent_commerce"] = commerce.parent_commerce.id
        commerce_dict["profit_share"] = commerce.profit_share
        platform_catalog_dict['commerce'].append(commerce_dict)
    
    request_update_platform_catalog_model = RequestUpdatePlatformCatalogModel(**platform_catalog_dict)
    
    request_update_platform_catalog_model.id = "60f8b500a916f6f81cd61f75"
    request_update_platform_catalog_model.pos[0].profit_share = 60.45

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    with pytest.raises(NotFoundException):
        service.update(request_update_platform_catalog_model,[1])

def test_delete_platform_catalog(app):
    
    platform_catalog = get_new_platform_catalog()

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    deleted = service.delete(platform_catalog.id)
    assert deleted == 1


def _get_pagination(page,per_page,order_direction = 'desc',order_name = 'name',param = {}):
    
    pagination = RequestPaginationModel(page=page,per_page=per_page)

    param['children_account'] = [1]
    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestPlatformCatalogModel(**param)

    service = PlatformCatalogService(repository=PlatformCatalogRepository(),pos_repository=PosRepository(),commerce_repository=CommerceRepository())
    list = service.getList(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order)
    
    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total