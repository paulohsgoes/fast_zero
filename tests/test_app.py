from http import HTTPStatus

# from fastapi import Response
from httpx import Response

from fast_zero.schemas import UserPublic


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


def test_create_users_with_same_name(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Dino da Silva Sauro',
            'email': 'dino@gmail.com',
            'password': 'password',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'Dino da Silva Sauro',
            'email': 'dino@yahoo.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_users(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': 'senhanova',
            'username': 'testusername2',
            'email': 'novoemail@test.com',
            'id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername2',
        'email': 'novoemail@test.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.json() == {'message': 'User deleted'}


"""
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
"""


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
