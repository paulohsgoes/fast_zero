from http import HTTPStatus

# from fastapi import Response


def test_read_rood_deve_retornar_OK_e_ola_mundo(client):
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Batatinhas fritas voadoras'}


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
