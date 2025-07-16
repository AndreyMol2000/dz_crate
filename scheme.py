import asyncio

from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine



class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "Students"
    
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    name = Column(String, index=True)
    faculty = Column(String, index=True)  
    kours = Column(String, index=True)
    score = Column(Integer, index=True)
    

async def create_db():
    PG_URL = "postgresql+asyncpg://postgres:132@localhost:5432/postgres"
    engine = create_async_engine(PG_URL)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_db())