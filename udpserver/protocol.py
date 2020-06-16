from struct import unpack
from udpserver import settings

import aioredis
import asyncio


async def setup_redis():
    loop = asyncio.get_running_loop()
    pool = await aioredis.create_redis_pool(settings.REDIS_URL, loop=loop)

    async def close_redis():
        pool.close()
        await pool.wait_closed()

    return (pool, close_redis)


class DummySensorProtocol:
    """
    Dummy Sensor Protocol

    It'll only print received data.
    """

    def datagram_received(self, data, addr):
        print(f"From {addr}\nReceived {data}")

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        if exc is None:
            print("Connection closed or aborted by me.")


class RedisPublisherSensorProtocol:
    """
    Publish sensor data into Redis
    """

    # TODO: call `close_redis`
    async def clean_up(self):
        pass

    async def datagram_received(self, data, addr):
        redis, _ = await setup_redis()
        redis.publish_json(settings.REDIS_SENSOR_CHANNEL, dict(data=data, addr=addr))

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        if exc is None:
            print("Connection closed or aborted by me.")


class RESTSensorServerProtocol:
    """
    POST sensor data to a REST API
    """

    endpoint = settings.API_URL

    def connection_made(self, transport):
        self.transport = transport

    async def datagram_received(self, data, addr):
        hardware_id, temperature, moisture = unpack("<20shh", data)
        data = {
            "hardware_id": hardware_id,
            "temperature": temperature,
            "moisture": moisture,
        }
        print(f"Received {data} from {addr} with hardware_id={hardware_id}")

        import httpx

        async with httpx.AsyncClient() as client:
            await client.post(self.endpoint, data, json=True)

    def connection_lost(self, exc):
        if exc is None:
            print("Connection closed or aborted by me.")
