import re
from datetime import UTC, datetime

from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.manager import Manager
from tortoise.queryset import QuerySet
from tortoise.validators import MaxValueValidator, MinValueValidator, RegexValidator


class Event(Model):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(
        max_length=100, validators=[RegexValidator(r'^[A-Za-z_][A-Za-z0-9_]*$', re.IGNORECASE)])
    created_at = fields.DatetimeField(auto_now_add=True)
    finished_at = fields.DatetimeField(null=True, default=None)

    def __str__(self) -> str:
        return self.name

    async def finish(self) -> None:
        self.finished_at = datetime.now(tz=UTC)
        await self.save()


class StateManager(Manager):

    async def get_instance(self) -> 'State':
        instance = await self.select_related('event').first()
        if not instance:
            instance = await self._model.create(event=None)
        return instance

    def get_queryset(self) -> QuerySet['State']:
        return super().get_queryset().select_related('event')


class State(Model):
    id = fields.IntField(primary_key=True)
    event: fields.OneToOneRelation[Event] = fields.OneToOneField(
        Event, on_delete=fields.RESTRICT, null=True, default=None)
    singleton = fields.IntField(validators=[MinValueValidator(1), MaxValueValidator(1)], default=1, unique=True)
    start_date = fields.DatetimeField(null=True, default=None)

    objects = StateManager()

    def __str__(self) -> str:
        return f'{self.pk}'

    @property
    def is_pending(self) -> bool:
        return self.event and self.event.finished_at is None

    async def update_start_date(self) -> None:
        self.start_date = datetime.now(tz=UTC)
        await self.save()


StatePydantic = pydantic_model_creator(State, exclude=('event',))
EventPydantic = pydantic_model_creator(Event)
EventList = pydantic_queryset_creator(Event)
