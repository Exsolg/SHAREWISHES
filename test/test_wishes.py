from datetime import datetime
from flask import jsonify
import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_create_wish_without_info(client):
    response = client.post('http://localhost:5000/api/v1/wish')
    assert response.status_code == 400


def test_create_wish_not_enough_data(client):
    response = client.post('http://localhost:5000/api/v1/wish', json={
        'title': 'New'
    })
    assert response.status_code == 400


def test_create_wish_success(client):
    user = client.post('http://localhost:5000/api/v1/users', json={
        'surname': 'Popovich',
        'name': 'Iliya',
        'nick': 'ilyuha',
        'age': datetime(2001, 5, 10).strftime('%d%m%Y'),
        'email': 'popovij@mail.ru',
        'password': 'shuha'
    }).json

    wish = {
        'title': 'New',
        'description': 'Brand new wish',
        'user_id': user['id'],
        'is_private': 'True'
    }

    response = client.post('http://localhost:5000/api/v1/wish', json=wish)

    client.delete(f'http://localhost:5000/api/v1/wish/{response.json["id"]}')
    client.delete(f'http://localhost:5000/api/v1/user/{user["id"]}')
    
    for k, v in wish.items():
        if str(v) != str(response.json[k]):
            assert False

    assert True


def test_delete_not_existed_wish(client):
    response = client.delete(
        f'http://localhost:5000/api/v1/wish/99999999999999')
    assert response.status_code == 404


def test_delete_existed_wish(client):
    user = client.post('http://localhost:5000/api/v1/users', json={
        'surname': 'Popovich',
        'name': 'Iliya',
        'nick': 'ilyuha',
        'age': datetime(2001, 5, 10).strftime('%d%m%Y'),
        'email': 'popovij@mail.ru',
        'password': 'shuha'
    }).json

    wish = client.post('http://localhost:5000/api/v1/wish', json={
        'title': 'New',
        'description': 'Brand new wish',
        'user_id': user['id'],
        'is_private': 'True'
    }).json

    response = client.delete(f'http://localhost:5000/api/v1/wish/{wish["id"]}')
    client.delete(f'http://localhost:5000/api/v1/user/{user["id"]}')

    assert wish.items() <= response.json.items()


def test_get_not_existed_wish(client):
    response = client.get(f'http://localhost:5000/api/v1/wish/99999999999999')
    assert response.status_code == 404

def test_get_existed_wish(client):
    user = client.post('http://localhost:5000/api/v1/users', json={
        'surname': 'Popovich',
        'name': 'Iliya',
        'nick': 'ilyuha',
        'age': datetime(2001, 5, 10).strftime('%d%m%Y'),
        'email': 'popovij@mail.ru',
        'password': 'shuha'
    }).json

    wish = client.post('http://localhost:5000/api/v1/wish', json={
        'title': 'New',
        'description': 'Brand new wish',
        'user_id': user['id'],
        'is_private': 'True'
    }).json

    response = client.get(f'http://localhost:5000/api/v1/wish/{wish["id"]}').json

    client.delete(f'http://localhost:5000/api/v1/wish/{wish["id"]}')
    client.delete(f'http://localhost:5000/api/v1/user/{user["id"]}')

    assert wish == response