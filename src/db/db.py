import asyncio
import time
import random
import uuid
from src.core.config import app_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError, DBAPIError
from src.models.base import Base
from src.core.config import db_echo_mode
from src.models.users import Users
from src.models.authorizations import Authorizations
from src.models.files import Files

engine = create_async_engine(app_settings.database_dsn, echo=db_echo_mode, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_model():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def ping_database():
    async with async_session() as session:
        try:
            start_time = time.time()
            await session.execute('SELECT 1')
            end_time = time.time()
            return end_time - start_time
        except DBAPIError:
            return None


async def find_user_by_name(name: str) -> Users:
    async with async_session() as session:
        query = select(Users).where(Users.name == name)
        user = await session.scalar(query)
        return user


async def find_user_by_token(token: str) -> Users:
    async with async_session() as session:
        query = select(Authorizations).where(Authorizations.auth_token == token)
        user = await session.scalar(query).user
        return user


async def add_auth_token(user: Users) -> str:
    async with async_session() as session:
        token = str(uuid.uuid4())
        while await session.scalar(select(Authorizations).where(Authorizations.auth_token == token)):
            token = str(uuid.uuid4())
        auth_token = Authorizations(auth_token=token, user=user)
        session.add(auth_token)
        await session.commit()
        return auth_token.auth_token


async def create_user(name, hash_password) -> Users:
    async with async_session() as session:
        user = Users(name=name, hash_password=hash_password)
        session.add(user)
        await session.commit()
        session.refresh(user)
        return user


async def get_files(token) -> list:
    async with async_session() as session:
        user = find_user_by_token(token)
        query = select(Files).where(Files.user == user)
        files = await session.scalar(query)
        return files


if __name__ == "__main__":
    asyncio.run(create_model())
