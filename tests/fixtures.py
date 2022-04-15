from src.infra.orm.factories.project_catalog import ProjectCatalogFactory
from src.infra.orm.factories.end_client_catalog import EndClientCatalogFactory
from src.infra.orm.factories.white_label_catalog import WhiteLabelCatalogFactory
from src.infra.orm.factories import CommerceFactory, PosFactory, BankingFactory, PlatformCatalogFactory

def get_new_commerce(**kwargs):
    commerce = CommerceFactory(**kwargs)
    commerce.save()
    commerce.id = str(commerce.id)
    return commerce

def get_new_platform_catalog(**kwargs):
    catalog = PlatformCatalogFactory(**kwargs)
    catalog.save()
    catalog.id = str(catalog.id)
    return catalog

def get_new_white_label_catalog(**kwargs):
    catalog = WhiteLabelCatalogFactory(**kwargs)
    catalog.save()
    catalog.id = str(catalog.id)
    return catalog

def get_new_end_client_catalog(**kwargs):
    catalog = EndClientCatalogFactory(**kwargs)
    catalog.save()
    catalog.id = str(catalog.id)
    return catalog

def get_new_project_catalog(**kwargs):
    catalog = ProjectCatalogFactory(**kwargs)
    catalog.save()
    catalog.id = str(catalog.id)
    return catalog

def get_new_pos(**kwargs):
    pos = PosFactory(**kwargs)
    pos.save()
    pos.id = str(pos.id)
    return pos

def get_new_banking(**kwargs):
    banking = BankingFactory(**kwargs)
    banking.save()
    banking.id = str(banking.id)
    return banking

def format_dict(dict,keys_to_remove):
    for key in keys_to_remove:
        del dict[key]
    return dict

def base_catalog_dict():
  return{
    "pos":[
      {
        "parent_pos":base_pos_dict(),
        "pos":base_pos_dict(),
        "profit_share":40.32,

      }
    ],
    "commerce":[
      {
        "parent_commerce":base_commerce_dict(),
        "commerce":base_commerce_dict(),
        "profit_share":40.32,

      }
    ],
    "account_id":1
  }

def base_project_catalog_dict():
  return{
    "pos":[
      {
        "parent_pos_id":"",
        "pos":base_pos_dict(),
        "profit_share":40.32,

      }
    ],
    "commerce":[
      {
        "parent_commerce_id":"",
        "commerce":base_commerce_dict(),
        "profit_share":40.32,

      }
    ],
    "parent_catalog":"",
    "account_id":1,
    "children_account":[1]
  }

def base_end_client_catalog_dict():
  return{
    "pos":[
      {
        "parent_pos_id":"",
        "pos":base_pos_dict(),
        "profit_share":40.32,

      }
    ],
    "commerce":[
      {
        "parent_commerce_id":"",
        "commerce":base_commerce_dict(),
        "profit_share":40.32,

      }
    ],
    "parent_catalog":"",
    "end_client_id":1
  }

def base_commerce_dict():
    return {
      "provider": {
        "id": 4,
        "name": "PGS",
        "document": "1434234234"
      },
      "cashout":[
        {
        "condition_start":0,
        "condition_end":300,
        "value":500
        }
      ],
      "state": 0,
      "debit": {
        "card_brands": [
          {
            "tx_type": "v",
            "name": "mastercard",
            "label": "mastercard debito",
            "taxes": [
              {
                "tx_type": "p",
                "tx_value": 10
              }
            ]
          }
        ]
      },
      "credit": {
        "tx_anticipation": 1,
        "card_brands": [
          {
            "name": "visa",
            "installments": [
              {
                "tx_type": "v",
                "installment": 1,
                "label": "1 x 6",
                "taxes": [
                  {
                    "tx_type": "p",
                    "tx_value": 10
                  }
                ]
              }
            ]
          }
        ]
      },
      "ticket": {
        "taxes": [
          {
            "tx_code": "tx_emissao",
            "tx_value": 10
          }
        ],
        "expiration_time": {
          "time": 10,
          "tx_value": 14
        }
      },
      "pix": {
        "taxes": [
          {
            "tx_code": "tx_emissao",
            "tx_value": 10
          }
        ]
      }
    }

def base_pos_dict():
  return {
    'plan_type': 'D30',
    'label' : "Label do POS",
    'plan_id' : "Um id legal",
    'anticipation_tax' : 1.00,
    'mccs': [742, 3022, 3028], 
    'state': True, 
    'unitary_value': 4481, 
    'provider': {
      'id': 109, 
      'name': 'Gonçalves',
      'document': '18372095000130'
    },
    'card_brands': [{
      'name': 'mastercard',
      'conditions': {
        'credit': [{
          'tx_type': 'v',
          'installment': 1,
          'label': 'das Neves Silva S/A',
          'taxes': [
            {
              'tx_type': 'p',
              'tx_value': 50
            },
          ]
        }],
        'debit': {
          'label': 'Debito',
          'tx_type': 'v',
          'taxes': [{
              'tx_type': 'v',
              'tx_value': 50
          }]
        }
      }
    }]
  }

def base_banking_dict():
    return {
      "services": [
          {
          "code": "codigoservico1",
          "label": "labelservico1",
          "cust": 10
          },
          {
          "code": "codigoservico2",
          "label": "labelservico2",
          "cust": 20
          }
      ],
      "provider": {
          "id": 3,
          "name": "PGS",
          "document": "9023012"
      },
      "name": "Banking Teste"
    }