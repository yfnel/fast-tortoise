from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from tortoise.contrib.fastapi import RegisterTortoise

from config import settings
from models import User, UserList, UserPydantic


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # pragma: no cover
    async with RegisterTortoise(
        app, db_url='sqlite://db.sqlite3', modules={'app': ['models']}, generate_schemas=True):
        yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def root() -> dict[str, str]:
    return {
        'app_name': settings.app_name,
        'version': settings.version,
        'db': settings.db,
    }


class UserListParams(BaseModel):
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)


@app.get('/users', response_model=UserList)
async def user_list(params: Annotated[UserListParams, Query()]) -> list[User]:
    return await UserList.from_queryset(User.all().offset(params.offset).limit(params.limit))


@app.get('/users/{user_id}', response_model=UserPydantic)
async def user_detail(user_id: int) -> User:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return await UserPydantic.from_tortoise_orm(user)
