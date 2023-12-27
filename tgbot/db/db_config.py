import asyncpg
import os
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASS = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432


async def connect_to_db():
    conn = await asyncpg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASS
    )
    print("Database connected successfully")
    return conn

async def close(conn):
    conn.close()
