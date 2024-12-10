import pytest
from moviweb_app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to MovieWeb App!" in response.data


def test_users_list_page(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b"Users" in response.data  # Check for Users header on the page


def test_add_user_page(client):
    response = client.get('/add_user')
    assert response.status_code == 200
    assert b"Add a New User" in response.data


def test_nonexistent_user_page(client):
    response = client.get('/users/nonexistent')
    assert response.status_code == 404  # Should return 404 for nonexisting user
