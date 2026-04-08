from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import Model


class User(Model):
    username = fields.CharField(max_length=50, unique=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username

    class Meta:
        table = 'users'


UserPydantic = pydantic_model_creator(User)
UserList = pydantic_queryset_creator(User)
