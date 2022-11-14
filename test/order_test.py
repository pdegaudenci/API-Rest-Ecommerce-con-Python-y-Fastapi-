import pytest
from fastapi.testclient import TestClient
from app import app  
from fastapi import status
from fastapi.responses import JSONResponse
from router.user import login_for_access_token

client = TestClient(app)

@pytest.fixture
def setUp():
    login = {
        'username': 'example@example.com',
        'password': 'example123'
    }
    response = client.post(
        '/auth/login/',
        data=login,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )
    data = response.json()
    return data

def test_get_orders_sinAutenticacion():
    response = client.get("/orders")
    assert response.status_code==401

def test_login():
    login = {
        'username': 'example@example.com',
        'password': 'example123'
    }
    response = client.post(
        '/auth/login/',
        data=login,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data['access_token']) > 0
    assert data['token_type'] == 'bearer'

def test_getorders(setUp:setUp):
    data = setUp
    orders = client.get("/orders",headers={"Authorization":"Bearer " + data['access_token']})
    assert orders.status_code==status.HTTP_200_OK

def test_getorderbyid(setUp:setUp):
    #Sin autenticacion
    orders = client.get("/order/2")
    assert orders.status_code==status.HTTP_401_UNAUTHORIZED
    # Con autenticacion
    data = setUp
    orders = client.get("/order/2",headers={"Authorization":"Bearer " + data['access_token']})
    assert orders.status_code==status.HTTP_200_OK

def test_create_orders(setUp:setUp):
    token = setUp
    data={
  "shipping_address": "string",
  "order_address": "string",
  "order_email": "string",
  "customer": {
    "full_name": "string",
    "email": "string",
    "billing_address": "string",
    "default_shipping_address": "string",
    "zip_code": "string",
    "country": "string",
    "phone": "string"
  },
  "products": [
    {
      "sku":3,
      "quantity":1
    }
  ],
  "payment_method": "string"
}
    response = client.post(
        '/order',
        data=data,
        headers={"Authorization":"Bearer " + token['access_token']},
        allow_redirects=True
    )
    assert response.status_code==status.HTTP_201_CREATED
