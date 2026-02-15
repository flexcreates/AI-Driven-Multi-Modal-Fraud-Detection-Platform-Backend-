import asyncio
from SRC.database.session import engine
from SRC.database.base import Base
# Import models so they are registered with Base
from SRC.models.user import User
from SRC.models.analysis import AnalysisRecord

async def init_async_db():
    async with engine.begin() as conn:
        # Create all tables
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_async_db())
