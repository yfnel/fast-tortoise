import pytest

from models import User


def test_root(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    data = response.json()
    assert data['app_name'] == 'Fast-Tortoise'
    assert data['version'].startswith('Fast-Tortoise')


@pytest.mark.asyncio
@pytest.mark.usefixtures('db')
async def test_user_representation():
    user = await User.create(username='test', first_name='test', last_name='test')
    assert str(user) == user.username


@pytest.mark.asyncio
async def test_user_detail(apiclient):
    user = await User.create(username='test', first_name='test', last_name='test')
    response = await apiclient.get(f'/users/{user.pk}')
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == user.username
    assert data['first_name'] == user.first_name
    assert data['last_name'] == user.last_name


@pytest.mark.asyncio
async def test_user_detail_404(apiclient):
    response = await apiclient.get('/users/123')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_list(apiclient):
    user = await User.create(username='test', first_name='test', last_name='test')
    response = await apiclient.get('/users')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    user_data = data[0]
    assert user_data['username'] == user.username
    assert user_data['first_name'] == user.first_name
    assert user_data['last_name'] == user.last_name
