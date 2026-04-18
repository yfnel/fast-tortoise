import importlib
import uuid
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from tortoise.contrib.fastapi import RegisterTortoise

from app.models import Event, EventList, EventPydantic, State, StatePydantic
from app.utils import perform_restart
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # pragma: no cover
    async with RegisterTortoise(
        app, db_url=settings.db, modules={'app': ['app.models']}, generate_schemas=True):
        state = await State.objects.get_instance()
        await state.update_start_date()
        yield


async def get_state() -> State | HTTPException:
    state = await State.objects.get_instance()
    if state.is_pending:
        raise HTTPException(status_code=400, detail='is pending.')
    return state


async def get_task(task: str) -> Callable | HTTPException:
    try:
        task = importlib.import_module(f'tasks.{task}')
    except ModuleNotFoundError:
        raise HTTPException(status_code=404) from None
    if not hasattr(task, 'run'):  # pragma: no cover
        raise HTTPException(status_code=400, detail='Task must have "run" method.')
    return task.run


StateDep = Annotated[State, Depends(get_state)]
TaskDep = Annotated[Callable, Depends(get_task)]


app = FastAPI(lifespan=lifespan)


async def run_task(task: Callable, event: Event) -> None:
    try:
        await task()
    finally:
        await event.finish()


@app.get('/')
async def root() -> dict[str, str]:
    return {
        'app_name': settings.app_name,
        'version': settings.version,
        'db': settings.db,
        'base_dir': str(settings.base_dir),
    }


@app.get('/state', response_model=StatePydantic | None)
async def state_detail() -> State | None:
    state = await State.objects.get_instance()
    return await StatePydantic.from_tortoise_orm(state)


@app.get('/event', response_model=EventPydantic | None)
async def current_event_detail() -> State | None:
    state = await State.objects.all().select_related('event').first()
    if state is None or state.event is None:
        return None
    return await EventPydantic.from_tortoise_orm(state.event)


class EventListParams(BaseModel):
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)


@app.get('/events', response_model=EventList)
async def events_list(params: Annotated[EventListParams, Query()]) -> list[Event]:
    return await EventList.from_queryset(Event.all().offset(params.offset).limit(params.limit))


@app.get('/events/{event_id}', response_model=EventPydantic)
async def event_detail(event_id: uuid.UUID) -> Event:
    event = await Event.get_or_none(pk=event_id)
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')
    return await EventPydantic.from_tortoise_orm(event)


@app.post('/initiate/{task}', response_model=EventPydantic)
async def initiate(task: TaskDep, state: StateDep, bg_task: BackgroundTasks) -> Event:
    name = task.__module__.split('.')[-1]
    event = await Event.create(name=name)
    state.event = event
    await state.save()
    bg_task.add_task(run_task, task, event)
    return await EventPydantic.from_tortoise_orm(state.event)


@app.post('/restart-app')
async def restart_app(state: StateDep) -> None:  # noqa: ARG001
    await perform_restart()


@app.post('/force-restart-app')
async def force_restart_app() -> None:
    state = await State.objects.get_instance()
    if state.is_pending:
        await state.event.finish()
    await perform_restart()
