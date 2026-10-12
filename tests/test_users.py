from http import HTTPStatus

from fast_zero.schemas import UserPublic


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

    assert response.status_code == HTTPStatus.FORBIDDEN


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


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': 'senhanova',
            'username': 'testusername2',
            'email': 'novoemail@test.com',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_create_users_with_same_email(client):
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
            'username': 'Paulo Góes',
            'email': 'dino@gmail.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
