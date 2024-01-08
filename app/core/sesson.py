from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:starcp@localhost:5432/expense_tracker"

async_engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)