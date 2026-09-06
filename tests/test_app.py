from http import HTTPStatus

import pytest

# from fastapi import Response
from httpx import Response


def test_read_rood_deve_retornar_OK_e_ola_mundo(client):
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Batatinhas fritas voadoras'}


def test_read_html_deve_retornar_OK_e_html(client):
    response: Response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert 'Cá estamos nós' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    # Voltou o status_code correto ?
    assert response.status_code == HTTPStatus.CREATED


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testusername',
                'email': 'test@test.com',
            }
        ]
    }


def test_update_users(client):
    response = client.put(
        '/users/1',
        json={
            'password': 'senhanova',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': 1,
        },
    )
    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


@pytest.mark.parametrize('user_id', [0, -1, 2])
def test_404_update_users(client, user_id):
    response = client.put(
        f'/users/{user_id}',
        json={
            'password': '222222',
            'username': 'testusername2',
            'email': 'paulohsgoes@gmail.com',
            'id': 2,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


@pytest.mark.parametrize('user_id', [0, -1, 2])
def test_404_delete_users(client, user_id):
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
