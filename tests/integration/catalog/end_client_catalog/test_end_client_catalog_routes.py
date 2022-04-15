from src.domain.catalog.models.platform_catalog_models import RequestUpdatePlatformCatalogModel
from tests.fixtures import base_catalog_dict, base_end_client_catalog_dict, get_new_project_catalog, get_new_end_client_catalog
from src.infra.orm.factories.project_catalog import ProjectCatalogFactory

# def test_do_test(app):
#     wl = ProjectCatalogFactory.build_batch(5)

#     for c in wl:
#         print(c.parent_catalog)

#     assert 4==5

def test_create_project_catalog(test_client):

    catalog_dict = base_end_client_catalog_dict()
    parent_catalog = get_new_project_catalog()

    catalog_dict['pos'][0]['parent_pos_id'] = str(parent_catalog.pos[0].pos.id)
    catalog_dict['commerce'][0]['parent_commerce_id'] = str(parent_catalog.commerce[0].commerce.id)
    catalog_dict['parent_catalog'] = parent_catalog.id
    response = test_client.post("/end_client_catalog/",json=catalog_dict)
    response_json = response.json()

    print(response_json)

    assert response.status_code == 200
    assert response_json['pos'][0]['parent_pos']['id'] == catalog_dict['pos'][0]['parent_pos_id']

def test_create_project_catalog_without_commerce(test_client):

    catalog_dict = base_end_client_catalog_dict()
    parent_catalog = get_new_project_catalog()
    catalog_dict.pop("commerce")
    catalog_dict['pos'][0]['parent_pos_id'] = str(parent_catalog.pos[0].pos.id)
    catalog_dict['parent_catalog'] = parent_catalog.id

    response = test_client.post("/end_client_catalog/",json=catalog_dict)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['pos'][0]['parent_pos']['id'] == catalog_dict['pos'][0]['parent_pos_id']
    assert response_json['commerce'] == []

def test_create_project_catalog_without_pos(test_client):

    catalog_dict = base_end_client_catalog_dict()
    parent_catalog = get_new_project_catalog()
    catalog_dict.pop("pos")
    catalog_dict['commerce'][0]['parent_commerce_id'] = str(parent_catalog.commerce[0].commerce.id)

    response = test_client.post("/end_client_catalog/",json=catalog_dict)
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['pos'] == []

def test_get_list_project_catalog(test_client):

    catalog = get_new_end_client_catalog()
    children_account = [1]
    response = test_client.get("/end_client_catalog",json=children_account)
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

def test_get_single_project_catalog(test_client):

    catalog = get_new_end_client_catalog()
    children_account = [1]

    response = test_client.get(f"/end_client_catalog/{str(catalog.id)}",json=children_account)

    response_json = response.json()

    assert response_json.get("id","") == catalog.id

def test_update_project_catalog(test_client):
    catalog = get_new_end_client_catalog()

    request_update_catalog_model = {}
    request_update_catalog_model["id"]= str(catalog.id)
    request_update_catalog_model["parent_catalog"]= str(catalog.parent_catalog.id)
    request_update_catalog_model["end_client_id"]= catalog.end_client_id
    request_update_catalog_model["pos"]= [{"parent_pos":str(pos.parent_pos.id),"pos":str(pos.pos.id),"profit_share":pos.profit_share} for pos in catalog.pos]
    request_update_catalog_model["commerce"]= [{"parent_commerce":str(commerce.parent_commerce.id),"commerce":str(commerce.commerce.id),"profit_share":commerce.profit_share} for commerce in catalog.commerce]

    request_update_catalog_dict = {}
    request_update_catalog_model["pos"][0]["profit_share"] = 60.45

    request_update_catalog_dict['request_model'] = request_update_catalog_model
    response = test_client.put(f"/end_client_catalog/",json=request_update_catalog_model)

    response_json = response.json()

    print(response_json)
    assert response.status_code == 200
    assert response_json['pos'][0]['profit_share'] == request_update_catalog_model["pos"][0]["profit_share"]

def test_update_project_catalog_commerce(test_client):

    catalog = get_new_end_client_catalog()
    children_account = [1]

    request_update_catalog_model = {}
    request_update_catalog_model["id"]= str(catalog.id)
    request_update_catalog_model["parent_catalog"]= str(catalog.parent_catalog.id)
    request_update_catalog_model["end_client_id"]= catalog.end_client_id
    request_update_catalog_model["pos"]= [{"parent_pos":str(pos.parent_pos.id),"pos":str(pos.pos.id),"profit_share":pos.profit_share} for pos in catalog.pos]
    request_update_catalog_model["commerce"]= []

    response = test_client.put(f"/end_client_catalog/",json=request_update_catalog_model)

    response_json = response.json()

    assert response.status_code == 200
    assert response_json['commerce'] == request_update_catalog_model["commerce"]

def test_update_project_catalog_pos(test_client):

    catalog = get_new_end_client_catalog()

    request_update_catalog_model = {}
    request_update_catalog_model["id"]= str(catalog.id)
    request_update_catalog_model["parent_catalog"]= str(catalog.parent_catalog.id)
    request_update_catalog_model["end_client_id"]= catalog.end_client_id
    request_update_catalog_model["pos"]= []
    request_update_catalog_model["commerce"]= [{"parent_commerce":str(commerce.parent_commerce.id),"commerce":str(commerce.commerce.id),"profit_share":commerce.profit_share} for commerce in catalog.commerce]

    response = test_client.put(f"/end_client_catalog/",json=request_update_catalog_model)

    response_json = response.json()

    assert response.status_code == 200
    assert response_json['pos'] == request_update_catalog_model["pos"]

def test_delete_project_catalog(test_client):

    catalog = get_new_end_client_catalog()
    request_dict = {
        "id":catalog.id
    }
    response = test_client.delete(f"/end_client_catalog/",params=request_dict)

    response_json = response.json()

    assert response.status_code == 200
