import aioredis


async def get_pool_of_connections(redis_url:str):
    """
    Returns a pool of connections.
    """
    return await aioredis.create_redis_pool(redis_url)
