import pytest
import asyncio
from database import engine, Base  # Укажите корректный импорт ваших engine и Base

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Автоматически создает таблицы в тестовой БД перед стартом тестов."""
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    # Создаем таблицы в БД test_blog
    asyncio.run(create_tables())
    
    yield
    
    # Удаляем таблицы после прогона всех тестов
    asyncio.run(drop_tables())