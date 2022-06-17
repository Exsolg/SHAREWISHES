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


def test_create_user_without_info(client):
    response = client.post('http://localhost:5000/api/v1/users')
    assert response.status_code == 400


def test_create_user_not_enough_data(client):
    response = client.post('http://localhost:5000/api/v1/users', json={
        'surname': 'Popovich',
        'name': 'Iliya',
        'age': datetime(2001, 5, 10),
        'email': 'popovij@mail.ru'
    })
    assert response.status_code == 400


def test_create_user_without_password(client):
    response = client.post('http://localhost:5000/api/v1/users', json={
        'surname': 'Popovich',
        'name': 'Iliya',
        'nick': 'ilyuha',
        'age': datetime(2001, 5, 10).strftime('%d%m%Y'),
        'email': 'popovij@mail.ru'
    })
    assert response.json['message']['password'] == "Missing required parameter in the JSON body or the post body or the query string" 


def test_create_user(client):
    user = {
        'surname': 'Popovich',
        'name': 'Iliya',
        'nick': 'ilyuha',
        'age': datetime(2001, 5, 10).strftime('%Y-%m-%d %H:%M:%S'),
        'email': 'popovij@mail.ru'
    }
    response = client.post('http://localhost:5000/api/v1/users', json={
        'surname': 'Popovich',
        'name': 'Iliya',
        'nick': 'ilyuha',
        'age': datetime(2001, 5, 10).strftime('%d%m%Y'),
        'email': 'popovij@mail.ru',
        'password': 'shuha'
    })
    client.delete(f'http://localhost:5000/api/v1/user/{response.json["id"]}')
    print(user.items(), response.json.items(), sep="\n")
    assert set(user.items()).issubset(set(response.json.items()))
