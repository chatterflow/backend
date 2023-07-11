from fastapi import Depends
from src.core.database.configs import settings
from fastapi.security import OAuth2PasswordBearer
from src.core.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)


async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


async def check_database_connection():
    session: AsyncSession = Session()
    try:
        await session.connection()
        await session.close()
        return True
    except Exception as error:
        print(error)
        return False


async def token_verifier(db: Session = Depends(get_session), token=Depends(oauth_scheme)):
    uc = await UserRepository(db).verify_token(access_token=token)
    return uc
