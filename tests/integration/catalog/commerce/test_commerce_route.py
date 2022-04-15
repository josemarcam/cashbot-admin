import json
from src.domain.catalog.models.commerce_models import RequestCommerceModel, CreateCommerceModel
from src.domain.catalog.repositories import CommerceRepository
from tests.fixtures import get_new_commerce, format_dict, base_commerce_dict

def test_create_commerce(test_client):
    
    commerce_dict = base_commerce_dict()
    response = test_client.post("/commerce/",json=commerce_dict)
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json.get("provider",{}).get("name","") == commerce_dict['provider']['name']

def test_create_commerce_without_ticket(test_client):
    
    commerce_dict = base_commerce_dict()
    commerce_dict.pop("ticket")
    response = test_client.post("/commerce/",json=commerce_dict)
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json.get("provider",{}).get("name","") == commerce_dict['provider']['name']

def test_create_commerce_without_cashout(test_client):
    
    commerce_dict = base_commerce_dict()
    commerce_dict.pop("cashout")
    response = test_client.post("/commerce/",json=commerce_dict)
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json.get("provider",{}).get("name","") == commerce_dict['provider']['name']

def test_create_commerce_invalid_brand(test_client):
    
    commerce_dict = base_commerce_dict()
    commerce_dict['credit']['card_brands'][0]['name'] = "nome invalido"
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422

def test_create_commerce_invalid_pix_tax(test_client):
    
    commerce_dict = base_commerce_dict()
    commerce_dict['pix']['taxes'][0]['tx_code'] = "nome invalido"
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422

def test_create_commerce_repeated_pix_tax(test_client):
    
    commerce_dict = base_commerce_dict()
    commerce_dict['pix']['taxes'].append(commerce_dict['pix']['taxes'][0])
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422
    

def test_create_commerce_repeated_brand(test_client):
    
    commerce_dict = base_commerce_dict()
    commerce_dict['credit']['card_brands'].append(commerce_dict['credit']['card_brands'][0])
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422
    
def test_create_commerce_invalid_total_tx_type(test_client):
    commerce_dict = base_commerce_dict()
    commerce_dict['credit']['card_brands'][0]['installments'][0]['tx_type'] = "taxa invalida"
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422

def test_create_commerce_invalid_tx_type(test_client):
    commerce_dict = base_commerce_dict()
    commerce_dict['credit']['card_brands'][0]['installments'][0]['taxes'][0]['tx_type'] = "taxa invalida"
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422

def test_create_commerce_repeated_installment(test_client):
    commerce_dict = base_commerce_dict()
    commerce_dict['credit']['card_brands'][0]['installments'].append(commerce_dict['credit']['card_brands'][0]['installments'][0])
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422

def test_create_commerce_ticket_code(test_client):
    commerce_dict = base_commerce_dict()
    commerce_dict['ticket']['taxes'][0]['tx_code'] = "codigo invalido"
    response = test_client.post("/commerce/",json=commerce_dict)

    assert response.status_code == 422

def test_create_commerce_invalid_cashout_condition(test_client):
    commerce_dict = base_commerce_dict()
    commerce_dict['cashout'].append(commerce_dict['cashout'][0])
    commerce_dict['cashout'][1]['condition_start'] = 5
    response = test_client.post("/commerce/",json=commerce_dict)
    
    assert response.status_code == 422

def test_get_list_commerce(test_client):
    
    commerce = get_new_commerce()
    
    response = test_client.get("/commerce")
    response_json = response.json()
    
    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert total == 1
    assert page == 1
    assert per_page == 10
    assert len(results) == 1
    assert results[0].get("id","") == str(commerce.id)

def test_get_single_commerce(test_client):
    
    commerce = get_new_commerce()
    
    response = test_client.get(f"/commerce/{str(commerce.id)}")
    
    response_json = response.json()
    
    assert response_json.get("id","") == commerce.id

def test_update_commerce(test_client):

    commerce = get_new_commerce()
    
    commerce_dict = commerce.to_mongo().to_dict()
    commerce_dict['id'] = str(commerce_dict['_id'])
    
    keys_to_remove = ['_id','created_at','updated_at']
    commerce_dict = format_dict(commerce_dict,keys_to_remove)
    
    commerce_dict['provider']['name'] = "nicolas"
    
    response = test_client.put(f"/commerce/",json=commerce_dict)
    response_json = response.json()
    
    assert response_json.get("provider",{}).get("name","") == "nicolas"

def test_exception_update_commerce(test_client):
    
    commerce = get_new_commerce()
    
    commerce_dict = commerce.to_mongo().to_dict()
    commerce_dict['id'] = "60f8b500a916f6f81cd61f75"
    
    keys_to_remove = ['_id','created_at','updated_at']
    commerce_dict = format_dict(commerce_dict,keys_to_remove)
    
    commerce_dict['provider']['name'] = "nicolas"
    
    response = test_client.put(f"/commerce/",json=commerce_dict)
    assert response.status_code == 404
    # response_json = response.json()

def test_update_state_commerce(test_client):

    commerce = get_new_commerce()
    
    request_dict = {
        'id': str(commerce.id),
        'commerce_state': 1
    }

    response_activate_json = test_client.patch(f"/commerce/state",json=request_dict).json()
    
    
    assert response_activate_json['state'] == True
    assert response_activate_json['id'] == request_dict['id']
    
    request_dict["commerce_state"] = 0
    
    response_deactivate_json = test_client.patch(f"/commerce/state",json=request_dict).json()

    assert response_deactivate_json['state'] == False
    assert response_deactivate_json['id'] == request_dict['id']

def test_exception_update_state_commerce(test_client):

    commerce = get_new_commerce()
    
    request_dict = {
        'id': "60f8b500a916f6f81cd61f75",
        'commerce_state': 1
    }

    response_activate_json = test_client.patch(f"/commerce/state",json=request_dict)
    
    assert response_activate_json.status_code == 404
    
    request_dict["commerce_state"] = 0
    
    response_deactivate_json = test_client.patch(f"/commerce/state",json=request_dict)

    assert response_deactivate_json.status_code == 404
