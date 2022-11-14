from fastapi.testclient import TestClient
from app import app  
from fastapi.responses import JSONResponse
from router.user import login_for_access_token

client = TestClient(app)

def test_get_orders_sinAutenticacion():
    response = client.get("/orders")

    assert response.status_code==401
def test_login():
    client = TestClient(app)

    user = {
        'username': 'example@example.com',
        'password': 'example123'
    }

    response = client.post(
        '/auth/login',
        json=user,
    )
    assert response.status_code == 201, response.text

    login = {
        'username': 'test_login',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/login/',
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
def test_get_orders_ConAutenticacion():
    token =login_for_access_token({"username":'example@example.com',"password":'example123'})
    response = client.get("/orders",headers=token)
    assert response.status_code==200