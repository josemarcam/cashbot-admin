import math

from bson.objectid import ObjectId
from src.domain.catalog.models.commerce_models import CommerceModel
from src.domain.catalog.models.pos_models import PosModel
from src.domain.catalog.repositories.platform_catalog_repository import PlatformCatalogRepository
from src.domain.catalog.models.platform_catalog_models import PlatformCatalogModel, CreatePlatformCatalogModel, RequestPlatformCatalogModel, RequestCreatePlatformCatalogModel, RequestOrdenationModel, RequestPaginationModel, RequestUpdatePlatformCatalogModel, UpdatePlatformCatalogModel
from tests.fixtures import base_catalog_dict, get_new_platform_catalog, get_new_commerce, get_new_pos
from src.infra.orm.factories import CommerceFactory, PosFactory

def test_create_platform_catalog(app):
    platform_catalog_dict = base_catalog_dict()
    
    commerce_entity = get_new_commerce()
    pos_entity = get_new_pos()
    
    parent_commerce_entity = get_new_commerce()
    parent_pos_entity = get_new_pos()

    
    platform_catalog_dict['pos'][0]['pos']['id'] = pos_entity.id
    platform_catalog_dict['pos'][0]['parent_pos']['id'] = parent_pos_entity.id
    
    platform_catalog_dict['commerce'][0]['commerce']['id'] = commerce_entity.id
    platform_catalog_dict['commerce'][0]['parent_commerce']['id'] = parent_commerce_entity.id
    
    platform_catalog_model = PlatformCatalogModel(**platform_catalog_dict)
    create_platform_catalog_entity = _create_catalog_model_from_request_models(platform_catalog_model,CreatePlatformCatalogModel)
    
    platform_catalog_repository = PlatformCatalogRepository()

    platform_catalog_model = platform_catalog_repository.create(create_platform_catalog_entity)
    
    assert type(platform_catalog_model)==PlatformCatalogModel
    assert platform_catalog_model.commerce[0].commerce.id == platform_catalog_model.commerce[0].commerce.id
    assert platform_catalog_model.commerce[0].parent_commerce.id == platform_catalog_model.commerce[0].parent_commerce.id
    assert platform_catalog_model.pos[0].pos.id == platform_catalog_model.pos[0].pos.id
    assert platform_catalog_model.pos[0].parent_pos.id == platform_catalog_model.pos[0].parent_pos.id

def test_find_single_catalog(app):
    platform_catalog = get_new_platform_catalog()
    request_model = RequestPlatformCatalogModel(children_account=[1],id=platform_catalog.id)
    platform_catalog_repository = PlatformCatalogRepository()
    platform_catalog_found = platform_catalog_repository.find_platform_catalog(request_model=request_model)
    assert platform_catalog_found.id == platform_catalog.id

def test_single_catalog_not_found(app):
    get_new_platform_catalog()
    request_model = RequestPlatformCatalogModel(children_account=[1],id="60f8b500a916f6f81cd61f75")
    platform_catalog_repository = PlatformCatalogRepository()
    platform_catalog_found = platform_catalog_repository.find_platform_catalog(request_model=request_model)
    assert platform_catalog_found == None

def test_update_catalog_client(app):
    
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
        pos_dict["pos"] = ObjectId(pos.pos.id)
        pos_dict["parent_pos"] = ObjectId(pos.parent_pos.id)
        pos_dict["profit_share"] = pos.profit_share
        platform_catalog_dict['pos'].append(pos_dict)

        
    for commerce in platform_catalog.commerce:
        commerce_dict = {}
        commerce_dict["commerce"] = ObjectId(commerce.commerce.id)
        commerce_dict["parent_commerce"] = ObjectId(commerce.parent_commerce.id)
        commerce_dict["profit_share"] = commerce.profit_share
        platform_catalog_dict['commerce'].append(commerce_dict)
    
    request_update_platform_catalog_model = RequestUpdatePlatformCatalogModel(**platform_catalog_dict)
    
    request_update_platform_catalog_model.pos[0].parent_pos = pos_entity.id
    request_update_platform_catalog_model.pos[0].profit_share = 60.45

    platform_catalog_repository = PlatformCatalogRepository()
    platform_catalog_updated = platform_catalog_repository.update_platform_catalog(request_update_platform_catalog_model,[1])
    
    assert platform_catalog_updated.pos[0].parent_pos.id == request_update_platform_catalog_model.pos[0].parent_pos
    assert platform_catalog_updated.pos[0].profit_share == request_update_platform_catalog_model.pos[0].profit_share

def test_update_catalog_client_remove_element(app):
    
    platform_catalog = get_new_platform_catalog()
    platform_catalog_dict = {
        "pos":[],
        "commerce":[],
        "account_id":platform_catalog.account_id,
        "id":platform_catalog.id

    }
    for pos in platform_catalog.pos:
        pos_dict = {}
        pos_dict["pos"] = ObjectId(pos.pos.id)
        pos_dict["parent_pos"] = ObjectId(pos.parent_pos.id)
        pos_dict["profit_share"] = pos.profit_share
        platform_catalog_dict['pos'].append(pos_dict)

        
    for commerce in platform_catalog.commerce:
        commerce_dict = {}
        commerce_dict["commerce"] = ObjectId(commerce.commerce.id)
        commerce_dict["parent_commerce"] = ObjectId(commerce.parent_commerce.id)
        commerce_dict["profit_share"] = commerce.profit_share
        platform_catalog_dict['commerce'].append(commerce_dict)
    
    request_update_platform_catalog_model = RequestUpdatePlatformCatalogModel(**platform_catalog_dict)    
    request_update_platform_catalog_model.pos = []

    platform_catalog_repository = PlatformCatalogRepository()
    platform_catalog_updated = platform_catalog_repository.update_platform_catalog(request_update_platform_catalog_model,[1])
    assert platform_catalog_updated.pos == []

def test_delete_catalog_client(app):
    platform_catalog = get_new_platform_catalog()
    
    platform_catalog_repository = PlatformCatalogRepository()
    platform_catalog_updated = platform_catalog_repository.delete_platform_catalog(platform_catalog.id)
    assert platform_catalog_updated==1

def test_list_platform_catalog(app):
    qtd = 13
    page = 1
    per_page = 5
     
    platform_catalogs = [] 
    for _ in range(25):
        platform_catalogs.append(get_new_platform_catalog())

    platform_catalogs = sorted(platform_catalogs, key=lambda x: x.id, reverse=True)

    results, pages, count = _get_pagination(page,per_page,order_name='_id')

    platform_catalog_filtered = platform_catalogs

    platform_catalog_page_1 = platform_catalog_filtered[:per_page]

    assert len(results) == per_page
    assert count == len(platform_catalog_filtered)
    assert pages == math.ceil(len(platform_catalog_filtered) / per_page)

    for platform_catalog in platform_catalog_page_1:
        results_index = results[platform_catalog_page_1.index(platform_catalog)]
        assert platform_catalog.id == results_index.id
    
    page = 2
    results_page_2, pages, count = _get_pagination(page,per_page,order_name='_id')
    platform_catalog_page_2 = platform_catalog_filtered[per_page:per_page * 2 ]
    
    assert len(results_page_2) == per_page
    assert count == len(platform_catalog_filtered)
    assert pages == math.ceil(len(platform_catalog_filtered) / per_page)
    
    for platform_catalog in platform_catalog_page_2:
        results_index = results_page_2[platform_catalog_page_2.index(platform_catalog)]
        assert platform_catalog.id == results_index.id
    

def _get_pagination(page,per_page,order_direction = 'desc',order_name = 'name',param = {}):
    
    pagination = RequestPaginationModel(page=page,per_page=per_page)

    param['children_account'] = [1]
    order = RequestOrdenationModel(order_direction=order_direction,order_name=order_name)
    request_model = RequestPlatformCatalogModel(**param)

    repository = PlatformCatalogRepository()
    list = repository.list_platform_catalog(request_model=request_model,request_pagination_model=pagination,request_ordenation_model=order)
    
    total = list.total
    total_pages = list.total_pages
    results = list.results

    return results, total_pages, total

def _create_catalog_model_from_request_models(request_platform_catalog_model,final_model):
        final_dict = {}
        pos_list = []
        commerce_list = []
        if request_platform_catalog_model.pos:
            for pos in request_platform_catalog_model.pos:
                pos_dict = {
                    "parent_pos": pos.parent_pos.id,
                    "pos": pos.pos.id,
                    "profit_share": pos.profit_share,
                }
                pos_list.append(pos_dict)
            final_dict['pos'] = pos_list
        
        if request_platform_catalog_model.commerce:
            for commerce in request_platform_catalog_model.commerce:
                commerce_dict = {
                    "parent_commerce": commerce.parent_commerce.id,
                    "commerce": commerce.commerce.id,
                    "profit_share": commerce.profit_share,
                }
                commerce_list.append(commerce_dict)
            
            final_dict['commerce'] = commerce_list
        final_dict['account_id'] = request_platform_catalog_model.account_id
        
        if request_platform_catalog_model.id != None:
            final_dict['id'] = request_platform_catalog_model.id

        return final_model(**final_dict)
