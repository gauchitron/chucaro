from udpserver import settings
import aioredis


class RedisClient:
    """
    A redis client.
    """

    url = None
    client = None

    @classmethod
    async def create(cls, redis_url):
        """
        Returns a `RedisClient` instance.
        """
        self = cls()
        self.url = redis_url
        print("Redis client creating")
        self.client = await aioredis.create_redis_pool(redis_url)
        print("Redis client created")
        return self

    async def gracefully_close(self):
        """
        Gracefully close underlying connections
        """
        if self.client is None:
            raise Exception("No redis client instance exists, did you created it?.")

        self.client.close()
        await self.client.wait_closed()
