from tests.fixtures import (
    get_new_pos,
    format_dict,
    base_pos_dict,
    get_new_platform_catalog,
    get_new_project_catalog,
    get_new_white_label_catalog,
    get_new_end_client_catalog
)

def test_create_pos(test_client):

    pos_dict = base_pos_dict()
    response = test_client.post("/pos/",json=pos_dict)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json.get("provider",{}).get("name","") == pos_dict['provider']['name']

def test_create_pos_invalid_total_tx_type(test_client):

    pos_dict = base_pos_dict()
    pos_dict['card_brands'][0]['conditions']['credit'][0]['tx_type'] = "taxa invalida"
    response = test_client.post("/pos/",json=pos_dict)

    assert response.status_code == 422

def test_create_pos_invalid_tx_type(test_client):

    pos_dict = base_pos_dict()
    pos_dict['card_brands'][0]['conditions']['credit'][0]['taxes'][0]['tx_type'] = "taxa invalida"
    response = test_client.post("/pos/",json=pos_dict)

    assert response.status_code == 422

def test_create_pos_repeated_installment(test_client):
    pos_dict = base_pos_dict()
    pos_dict['card_brands'][0]['conditions']['credit'].append(pos_dict['card_brands'][0]['conditions']['credit'][0])
    response = test_client.post("/pos/",json=pos_dict)

    assert response.status_code == 422

def test_create_pos_with_invalid_brand_name(test_client):

    pos_dict = base_pos_dict()
    pos_dict['card_brands'][0]['name'] = "nome invalido"
    response = test_client.post("/pos/",json=pos_dict)

    assert response.status_code == 422

# def test_create_pos_with_repeated_brand_name(test_client):

#     pos_dict = base_pos_dict()
#     pos_dict['credit']['card_brands'].append(pos_dict['credit']['card_brands'][0])
#     response = test_client.post("/pos/",json=pos_dict)

#     assert response.status_code == 422

def test_get_list_pos(test_client):

    pos = get_new_pos()

    response = test_client.get("/pos")
    response_json = response.json()

    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert total == 1
    assert page == 1
    assert per_page == 10
    assert len(results) == 1
    assert results[0].get("id","") == str(pos.id)

def test_get_single_pos(test_client):

    pos = get_new_pos()

    response = test_client.get(f"/pos/{str(pos.id)}")

    response_json = response.json()

    assert response_json.get("id","") == pos.id

def test_update_pos(test_client):

    pos = get_new_pos()

    pos_dict = pos.to_mongo().to_dict()
    pos_dict['id'] = str(pos_dict['_id'])

    keys_to_remove = ['_id','created_at','updated_at']
    pos_dict = format_dict(pos_dict,keys_to_remove)

    pos_dict['provider']['name'] = "nicolas"

    response = test_client.put(f"/pos/",json=pos_dict)
    response_json = response.json()
    print(response_json)

    assert response_json.get("provider",{}).get("name","") == "nicolas"

def test_exception_update_pos(test_client):

    pos = get_new_pos()

    pos_dict = pos.to_mongo().to_dict()
    pos_dict['id'] = "60f8b500a916f6f81cd61f75"

    keys_to_remove = ['_id','created_at','updated_at']
    pos_dict = format_dict(pos_dict,keys_to_remove)

    pos_dict['provider']['name'] = "nicolas"

    response = test_client.put(f"/pos/",json=pos_dict)
    assert response.status_code == 404
    # response_json = response.json()

def test_update_state_pos(test_client):

    pos = get_new_pos()

    request_dict = {
        'id': str(pos.id),
        'pos_state': 1
    }

    response_activate_json = test_client.patch(f"/pos/state",json=request_dict).json()


    assert response_activate_json['state'] == True
    assert response_activate_json['id'] == request_dict['id']

    request_dict["pos_state"] = 0

    response_deactivate_json = test_client.patch(f"/pos/state",json=request_dict).json()

    assert response_deactivate_json['state'] == False
    assert response_deactivate_json['id'] == request_dict['id']

def test_exception_update_state_pos(test_client):

    pos = get_new_pos()

    request_dict = {
        'id': "60f8b500a916f6f81cd61f75",
        'pos_state': 1
    }

    response_activate_json = test_client.patch(f"/pos/state",json=request_dict)

    assert response_activate_json.status_code == 404

    request_dict["pos_state"] = 0

    response_deactivate_json = test_client.patch(f"/pos/state",json=request_dict)

    assert response_deactivate_json.status_code == 404

def test_delet_cost_pos(test_client):
    pos = get_new_pos()

    response_delete_params = test_client.delete(f"/pos/{str(pos.id)}")

    assert response_delete_params.status_code == 200

def test_delete_cost_pos_not_found(test_client):

    response_delete_params = test_client.delete("/pos/60f8b500a916f6f81cd61f75")

    assert response_delete_params.status_code == 404

def test_list_pos_platform(test_client):
    pos_catalog = get_new_platform_catalog()

    count = len(pos_catalog.pos)
    pos_list = []
    for pos_object in pos_catalog.pos:
        pos_list.append(pos_object.pos)


    response = test_client.get("/pos/platform")
    response_json = response.json()

    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert total == count
    assert page == 1
    assert per_page == 10
    assert len(results) == count

    pos_sorted = sorted(pos_list, key=lambda x: x.id, reverse=True)

    for pos_results in pos_sorted:
        results_index = results[pos_sorted.index(pos_results)]
        assert results_index.get("id","") == str(pos_results.id)

def test_list_pos_project(test_client):
    
    project_catalog = get_new_project_catalog()

    
    count = len(project_catalog.pos)
    
    pos_list = []
    
    for pos_project in project_catalog.pos:
        pos_list.append(pos_project.pos)

    response = test_client.get("/pos/project")
    response_json = response.json()

    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert page == 1
    assert per_page == 10
    assert len(results) == count
    assert total == count

    pos_sorted = sorted(pos_list, key=lambda x: x.id,reverse=True)

    for pos_results in pos_sorted:
        results_index = results[pos_sorted.index(pos_results)]
        assert results_index.get("id","") == str(pos_results.id)

def test_list_pos_white_label(test_client):
    pos_catalog = get_new_white_label_catalog()

    count = len(pos_catalog.pos)
    pos_list = []
    for pos_object in pos_catalog.pos:
        pos_list.append(pos_object.pos)

    response = test_client.get("/pos/white-label")
    response_json = response.json()

    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert total == count
    assert page == 1
    assert per_page == 10
    assert len(results) == count

    pos_sorted = sorted(pos_list, key=lambda x: x.id, reverse=True)

    for pos_results in pos_sorted:
        results_index = results[pos_sorted.index(pos_results)]
        assert results_index.get("id", "") == str(pos_results.id)

def test_list_pos_end_client(test_client):
    pos_catalog = get_new_end_client_catalog()

    count = len(pos_catalog.pos)
    pos_list = []
    for pos_object in pos_catalog.pos:
        pos_list.append(pos_object.pos)

    response = test_client.get("/pos/end-client")
    response_json = response.json()

    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert total == count
    assert page == 1
    assert per_page == 10
    assert len(results) == count

    pos_sorted = sorted(pos_list, key=lambda x: x.id, reverse=True)

    for pos_results in pos_sorted:
        results_index = results[pos_sorted.index(pos_results)]
        assert results_index.get("id", "") == str(pos_results.id)


