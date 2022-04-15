from tests.fixtures import get_new_banking, format_dict, base_banking_dict

def test_create_banking(test_client):
    
    banking_dict = base_banking_dict()
    response = test_client.post("/banking/",json=banking_dict)
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json.get("provider",{}).get("name","") == banking_dict['provider']['name']

def test_get_list_banking(test_client):
    
    banking = get_new_banking()
    
    response = test_client.get("/banking")
    response_json = response.json()
    
    total = response_json.get('total',0)
    page = response_json.get('page',0)
    per_page = response_json.get('per_page',0)
    results = response_json['results']

    assert total == 1
    assert page == 1
    assert per_page == 10
    assert len(results) == 1
    assert results[0].get("id","") == str(banking.id)

def test_get_single_banking(test_client):
    
    banking = get_new_banking()
    
    response = test_client.get(f"/banking/{str(banking.id)}")
    
    response_json = response.json()
    
    assert response_json.get("id","") == banking.id

def test_update_banking(test_client):

    banking = get_new_banking()
    
    banking_dict = banking.to_mongo().to_dict()
    banking_dict['id'] = str(banking_dict['_id'])
    
    keys_to_remove = ['_id','created_at','updated_at']
    banking_dict = format_dict(banking_dict,keys_to_remove)
    
    banking_dict['provider']['name'] = "nicolas"
    
    response = test_client.put(f"/banking/",json=banking_dict)
    response_json = response.json()
    
    assert response_json.get("provider",{}).get("name","") == "nicolas"

def test_exception_update_banking(test_client):
    
    banking = get_new_banking()
    
    banking_dict = banking.to_mongo().to_dict()
    banking_dict['id'] = "60f8b500a916f6f81cd61f75"
    
    keys_to_remove = ['_id','created_at','updated_at']
    banking_dict = format_dict(banking_dict,keys_to_remove)
    
    banking_dict['provider']['name'] = "nicolas"
    
    response = test_client.put(f"/banking/",json=banking_dict)
    assert response.status_code == 404