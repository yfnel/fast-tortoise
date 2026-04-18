import pytest

from app.models import Event, State


@pytest.mark.asyncio
@pytest.mark.usefixtures('db')
async def test_empty_state_event():
    state = await State.objects.get_instance()
    assert str(state) == str(state.pk)
    assert state.event is None


@pytest.mark.asyncio
@pytest.mark.usefixtures('db')
async def test_state_event():
    event = await Event.create(name='test')
    await State.create(event=event)
    state = await State.objects.get()
    assert state.is_pending


@pytest.mark.asyncio
@pytest.mark.usefixtures('db')
async def test_state_start_date():
    event = await Event.create(name='test')
    state = await State.create(event=event)
    assert state.start_date is None
    await state.update_start_date()
    assert state.start_date is not None
