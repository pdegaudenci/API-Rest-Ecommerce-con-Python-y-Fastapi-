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

def test_get_products():
    response = client.get("/products")
    assert response.status_code==200

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

def test_get_product(setUp:setUp):
    data = setUp
    orders = client.get("/product/5",headers={"Authorization":"Bearer " + data['access_token']})
    assert orders.status_code==status.HTTP_200_OK

def test_getorderbyid(setUp:setUp):
    #Sin autenticacion
    orders = client.get("/order/2")
    assert orders.status_code==status.HTTP_401_UNAUTHORIZED
    # Con autenticacion
    data = setUp
    orders = client.get("/order/2",headers={"Authorization":"Bearer " + data['access_token']})
    assert orders.status_code==status.HTTP_200_OK

def test_get_withlimit(setUp:setUp):
    token = setUp
    data={
        "skip":5,
        "limit":10
    }
    response = client.post(
        '/products_page/',
        data=data,
        headers={"Authorization":"Bearer " + token['access_token']},
        allow_redirects=True
    )
    assert response.status_code==status.HTTP_200_OK
