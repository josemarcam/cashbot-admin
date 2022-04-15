from src.domain.catalog.models.platform_catalog_models import RequestUpdatePlatformCatalogModel
from tests.fixtures import base_catalog_dict, get_new_platform_catalog, get_new_commerce, get_new_pos
from src.infra.orm.factories.project_catalog import ProjectCatalogFactory

# def test_do_test(app):
#     wl = ProjectCatalogFactory.build_batch(5)
    
#     for c in wl:
#         print(c.parent_catalog)
    
#     assert 4==5 

def test_create_platform_catalog(test_client):
    catalog_dict = base_catalog_dict()
    pos = get_new_pos()
    commerce = get_new_commerce()

    catalog_dict['pos'][0]['parent_pos_id'] = pos.id
    catalog_dict['commerce'][0]['parent_commerce_id'] = commerce.id

    response = test_client.post("/platform_catalog/",json=catalog_dict)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['pos'][0]['parent_pos']['id'] == catalog_dict['pos'][0]['parent_pos_id']

def test_create_platform_catalog_without_commerce(test_client):
    catalog_dict = base_catalog_dict()
    pos = get_new_pos()
    catalog_dict.pop("commerce")
    catalog_dict['pos'][0]['parent_pos_id'] = pos.id

    response = test_client.post("/platform_catalog/",json=catalog_dict)
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['pos'][0]['parent_pos']['id'] == catalog_dict['pos'][0]['parent_pos_id']
    assert response_json['commerce'] == []

def test_create_platform_catalog_without_pos(test_client):
    catalog_dict = base_catalog_dict()
    commerce = get_new_commerce()
    catalog_dict.pop("pos")
    catalog_dict['commerce'][0]['parent_commerce_id'] = commerce.id

    response = test_client.post("/platform_catalog/",json=catalog_dict)
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['pos'] == []

def test_get_list_platform_catalog(test_client):
    
    catalog = get_new_platform_catalog()
    children_account = [1]
    response = test_client.get("/platform_catalog",json=children_account)
    response_json = response.json()
    
    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert total == 1
    assert page == 1
    assert per_page == 10
    assert len(results) == 1
    assert results[0].get("id","") == str(catalog.id)

def test_get_single_platform_catalog(test_client):
    
    catalog = get_new_platform_catalog()
    children_account = [1]
    
    response = test_client.get(f"/platform_catalog/{str(catalog.id)}",json=children_account)
    
    response_json = response.json()
    
    assert response_json.get("id","") == catalog.id

def test_update_platform_catalog(test_client):

    catalog = get_new_platform_catalog()
    children_account = [1]
        
    request_update_catalog_model = {}
    request_update_catalog_model["id"]= str(catalog.id)
    request_update_catalog_model["account_id"]= catalog.account_id
    request_update_catalog_model["pos"]= [{"parent_pos":str(pos.parent_pos.id),"pos":str(pos.pos.id),"profit_share":pos.profit_share} for pos in catalog.pos]
    request_update_catalog_model["commerce"]= [{"parent_commerce":str(commerce.parent_commerce.id),"commerce":str(commerce.commerce.id),"profit_share":commerce.profit_share} for commerce in catalog.commerce]
    
    request_update_catalog_dict = {}
    request_update_catalog_model["pos"][0]["profit_share"] = 60.45

    request_update_catalog_dict['request_model'] = request_update_catalog_model
    request_update_catalog_dict['children_account'] = children_account
    response = test_client.put(f"/platform_catalog/",json=request_update_catalog_dict)
    
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['pos'][0]['profit_share'] == request_update_catalog_model["pos"][0]["profit_share"]

def test_delete_platform_catalog(test_client):
    catalog = get_new_platform_catalog()
    request_dict = {
        "id":catalog.id
    }
    response = test_client.delete(f"/platform_catalog/",params=request_dict)
    
    response_json = response.json()

    assert response.status_code == 200