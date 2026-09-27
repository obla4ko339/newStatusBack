import redis.asyncio as aioredis

class RedisContainer:
    def __init__(self):
        self.client: aioredis.Redis = None  # type: ignore

    def init(self, url: str = "redis://cache:6379"):
        """Инициализирует подключение внутри холдера."""
        self.client = aioredis.from_url(url, decode_responses=True)

    async def close(self):
        """Закрывает пул соединений."""
        if self.client:
            await self.client.close()

# Экспортируем ОДИН экземпляр класса на весь проект
redis_container = RedisContainer()
