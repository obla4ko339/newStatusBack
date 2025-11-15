import asyncio
from tortoise import Tortoise
from src.core.db import TORTOISE_ORM
import asyncpg

async def apply_migration():
    # Подключаемся к БД
    await Tortoise.init(config=TORTOISE_ORM)
    
    conn = await asyncpg.connect(
        "postgres://postgres:postgres@postgres:5432/quiz_app"
    )
    
    # Создаем таблицу users
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS "users" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "username" VARCHAR(50) NOT NULL UNIQUE,
            "password_hash" VARCHAR(255) NOT NULL,
            "is_active" BOOL NOT NULL DEFAULT True,
            "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS "idx_users_usernam" ON "users" ("username");
    """)
    
    print("Migration applied successfully!")
    
    await conn.close()
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(apply_migration())
