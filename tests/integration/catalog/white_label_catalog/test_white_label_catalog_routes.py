from src.domain.catalog.models.project_catalog_models import RequestUpdateProjectCatalogModel
from tests.fixtures import base_catalog_dict, base_project_catalog_dict, get_new_platform_catalog, get_new_white_label_catalog, get_new_commerce, get_new_pos
from src.infra.orm.factories.project_catalog import ProjectCatalogFactory

def test_create_white_label_catalog(test_client):
    
    catalog_dict = base_project_catalog_dict()
    parent_catalog = get_new_platform_catalog()
    
    catalog_dict['pos'][0]['parent_pos_id'] = str(parent_catalog.pos[0].pos.id)
    catalog_dict['commerce'][0]['parent_commerce_id'] = str(parent_catalog.commerce[0].commerce.id)
    catalog_dict['parent_catalog'] = parent_catalog.id
    response = test_client.post("/white_label_catalog/",json=catalog_dict)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['pos'][0]['parent_pos']['id'] == catalog_dict['pos'][0]['parent_pos_id']

def test_create_white_label_catalog_without_commerce(test_client):
    
    catalog_dict = base_project_catalog_dict()
    parent_catalog = get_new_platform_catalog()
    catalog_dict.pop("commerce")
    catalog_dict['pos'][0]['parent_pos_id'] = str(parent_catalog.pos[0].pos.id)
    catalog_dict['parent_catalog'] = parent_catalog.id

    response = test_client.post("/white_label_catalog/",json=catalog_dict)
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['pos'][0]['parent_pos']['id'] == catalog_dict['pos'][0]['parent_pos_id']
    assert response_json['commerce'] == []

def test_create_white_label_catalog_without_pos(test_client):
    
    catalog_dict = base_project_catalog_dict()
    parent_catalog = get_new_platform_catalog()
    catalog_dict.pop("pos")
    catalog_dict['commerce'][0]['parent_commerce_id'] = str(parent_catalog.commerce[0].commerce.id)

    response = test_client.post("/white_label_catalog/",json=catalog_dict)
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['pos'] == []

def test_get_list_white_label_catalog(test_client):
    
    catalog = get_new_white_label_catalog()
    children_account = [1]
    response = test_client.get("/white_label_catalog",json=children_account)
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

def test_get_single_white_label_catalog(test_client):
    
    catalog = get_new_white_label_catalog()
    children_account = [1]
    
    response = test_client.get(f"/white_label_catalog/{str(catalog.id)}",json=children_account)
    
    response_json = response.json()
    
    assert response_json.get("id","") == catalog.id

def test_update_white_label_catalog(test_client):
    catalog = get_new_white_label_catalog()
    children_account = [1]
        
    request_update_catalog_model = {}
    request_update_catalog_model["id"]= str(catalog.id)
    request_update_catalog_model["parent_catalog"]= str(catalog.parent_catalog.id)
    request_update_catalog_model["account_id"]= catalog.account_id
    request_update_catalog_model["pos"]= [{"parent_pos":str(pos.parent_pos.id),"pos":str(pos.pos.id),"profit_share":pos.profit_share} for pos in catalog.pos]
    request_update_catalog_model["commerce"]= [{"parent_commerce":str(commerce.parent_commerce.id),"commerce":str(commerce.commerce.id),"profit_share":commerce.profit_share} for commerce in catalog.commerce]
    
    request_update_catalog_dict = {}
    request_update_catalog_model["pos"][0]["profit_share"] = 60.45

    request_update_catalog_dict['request_model'] = request_update_catalog_model
    request_update_catalog_dict['children_account'] = children_account
    response = test_client.put(f"/white_label_catalog/",json=request_update_catalog_dict)
    
    response_json = response.json()

    print(response_json)
    assert response.status_code == 200
    assert response_json['pos'][0]['profit_share'] == request_update_catalog_model["pos"][0]["profit_share"]

def test_update_white_label_catalog_commerce(test_client):
    
    catalog = get_new_white_label_catalog()
    children_account = [1]

    request_update_catalog_model = {}
    request_update_catalog_model["id"]= str(catalog.id)
    request_update_catalog_model["parent_catalog"]= str(catalog.parent_catalog.id)
    request_update_catalog_model["account_id"]= catalog.account_id
    request_update_catalog_model["pos"]= [{"parent_pos":str(pos.parent_pos.id),"pos":str(pos.pos.id),"profit_share":pos.profit_share} for pos in catalog.pos]
    request_update_catalog_model["commerce"]= []
    
    request_update_catalog_dict = {}

    request_update_catalog_dict['request_model'] = request_update_catalog_model
    request_update_catalog_dict['children_account'] = children_account
    response = test_client.put(f"/white_label_catalog/",json=request_update_catalog_dict)
    
    response_json = response.json()

    assert response.status_code == 200
    print(response_json)
    assert response_json['commerce'] == request_update_catalog_model["commerce"]

def test_update_white_label_catalog_pos(test_client):
    
    catalog = get_new_white_label_catalog()
    children_account = [1]

    request_update_catalog_model = {}
    request_update_catalog_model["id"]= str(catalog.id)
    request_update_catalog_model["parent_catalog"]= str(catalog.parent_catalog.id)
    request_update_catalog_model["account_id"]= catalog.account_id
    request_update_catalog_model["pos"]= []
    request_update_catalog_model["commerce"]= [{"parent_commerce":str(commerce.parent_commerce.id),"commerce":str(commerce.commerce.id),"profit_share":commerce.profit_share} for commerce in catalog.commerce]
    
    request_update_catalog_dict = {}

    request_update_catalog_dict['request_model'] = request_update_catalog_model
    request_update_catalog_dict['children_account'] = children_account
    response = test_client.put(f"/white_label_catalog/",json=request_update_catalog_dict)
    
    response_json = response.json()

    assert response.status_code == 200
    print(response_json)
    assert response_json['pos'] == request_update_catalog_model["pos"]

def test_delete_white_label_catalog(test_client):
    
    catalog = get_new_white_label_catalog()
    request_dict = {
        "id":catalog.id
    }
    response = test_client.delete(f"/white_label_catalog/",params=request_dict)
    
    response_json = response.json()

    assert response.status_code == 200