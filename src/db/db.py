import asyncio
import time
from src.core.config import app_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import DBAPIError
from src.models.base import Base
from src.core.config import db_echo_mode
from src.models.users import Users
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


async def create_user(name, hash_password) -> Users:
    async with async_session() as session:
        user = Users(name=name, hash_password=hash_password)
        session.add(user)
        await session.commit()
        session.refresh(user)
        return user


async def add_file(name: str, path: str, size: int, user: Users):
    async with async_session() as session:
        new_file = Files(name=name, path=path, size=size, user=user, user_id=user.id, is_downloadable=True)
        session.add(new_file)
        await session.commit()
        session.refresh(new_file)
        return new_file


async def get_all_user_file(user: Users) -> list:
    async with async_session() as session:
        query = select(Files).where(Files.user == user)
        files = await session.execute(query)
        return files.fetchall()


async def get_file(s_data: str) -> Files:
    async with async_session() as session:
        if s_data.isdigit():
            query = select(Files).where(Files.id == int(s_data))
        else:
            query = select(Files).where(Files.path == s_data)
        file = await session.execute(query)
        file = file.fetchall()
        return file[0][0]


if __name__ == "__main__":
    asyncio.run(create_model())
