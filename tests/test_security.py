from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)
    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_without_sub(client):
    # Cria um token válido, mas SEM o campo 'sub'
    data = {'outra_chave': 'valor'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not_found_in_db(client):
    # Cria um token com um e-mail que NÃO está cadastrado no banco
    token = create_access_token(data={'sub': 'nao_existo@test.com'})

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
