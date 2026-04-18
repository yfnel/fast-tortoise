import uuid

import pytest

from app.models import Event, State
from config import settings


def test_root(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    data = response.json()
    assert data['app_name'] == 'Fast-Tortoise'
    assert data['version'].startswith('Fast-Tortoise')

@pytest.mark.asyncio
@pytest.mark.usefixtures('db')
async def test_state_representation():
    state = await State.objects.get_instance()
    assert str(state) == str(state.pk)


@pytest.mark.asyncio
async def test_get_empty_state(apiclient):
    response = await apiclient.get('/state')
    assert response.status_code == 200
    data = response.json()
    assert data is not None


@pytest.mark.asyncio
async def test_get_empty_event(apiclient):
    response = await apiclient.get('/event')
    assert response.status_code == 200
    data = response.json()
    assert data is None


@pytest.mark.asyncio
async def test_get_event(apiclient):
    event = await Event.create(name='test')
    await State.create(event=event)
    response = await apiclient.get('/event')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(event.pk)
    assert data['name'] == event.name


@pytest.mark.asyncio
@pytest.mark.usefixtures('db')
async def test_event_representation():
    event = await Event.create(name='test')
    assert str(event) == event.name


@pytest.mark.asyncio
async def test_event_detail(apiclient):
    event = await Event.create(name='test')
    response = await apiclient.get(f'/events/{event.pk}')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == event.name


@pytest.mark.asyncio
async def test_event_detail_404(apiclient):
    response = await apiclient.get(f'/events/{uuid.uuid4()}')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_event_list(apiclient):
    event = await Event.create(name='test')
    response = await apiclient.get('/events')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    event_data = data[0]
    assert event_data['name'] == event.name


@pytest.mark.asyncio
async def test_initiate_task(apiclient):
    response = await apiclient.post('/initiate/debug_task')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'debug_task'


@pytest.mark.asyncio
async def test_initiate_non_existing_task(apiclient):
    response = await apiclient.post('/initiate/abc_123')
    assert response.status_code == 404
    data = response.json()
    assert data == {'detail': 'Not Found'}


@pytest.mark.asyncio
async def test_initiate_task_pending_error(apiclient):
    event = await Event.create(name='test')
    await State.create(event=event)
    response = await apiclient.post('/initiate/debug_task')
    assert response.status_code == 400
    data = response.json()
    assert data == {'detail': 'is pending.'}


@pytest.mark.asyncio
async def test_restart_app(apiclient):
    response = await apiclient.post('/restart-app')
    assert response.status_code == 200
    data = response.json()
    assert data is None
    assert settings.restarter_file.exists()
    settings.restarter_file.unlink()


@pytest.mark.asyncio
async def test_force_restart_app(apiclient):
    event = await Event.create(name='test')
    await State.create(event=event)
    response = await apiclient.post('/force-restart-app')
    assert response.status_code == 200
    data = response.json()
    assert data is None
    assert settings.restarter_file.exists()
    settings.restarter_file.unlink()
    await event.refresh_from_db()
    assert event.finished_at is not None
