import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Import the FastAPI instance app from src.main
from src.main import app

# Load environment variables from .env.local file
load_dotenv('.env.local')

client = TestClient(app)


def test_read_users_me():
    print('test_read_users_me')
    url = "/users/me"
    headers = {
        'Authorization': f"Bearer {os.getenv('ACCESS_TOKEN')}",
        'Content-Type': 'application/json'
    }
    response = client.get(url, headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'result': {
            'username': 'sangle1',
            'email': 'sang.lequang94@gmail.com',
            'id': 1}}


def test_read_users_me_invalid_token():
    url = "/users/me"
    headers = {
        'Authorization': f"Bearer invalid_token",
        'Content-Type': 'application/json'
    }

    response = client.get(url, headers=headers)
    print(response.json())

    assert response.status_code == 401
