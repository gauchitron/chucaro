from struct import unpack
from datetime import datetime
from udpserver import settings

import httpx


class BaseSensorProtocol:
    """
    Base class for sensor protocols.
    """

    def __init__(self, on_cleanup=None):
        """
        on_cleanup:     A list of `coroutines` to be excecuted on transport close.
        """
        self.on_cleanup = on_cleanup or []

    def datagram_received(self, data, addr):
        raise NotImplementedError

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        if exc is None:
            print("Connection closed or aborted by me.")


class DummySensorProtocol(BaseSensorProtocol):
    """
    Dummy Sensor Protocol

    It'll only print received data.
    """

    def datagram_received(self, data, addr):
        print(f"From {addr}\nReceived {data}")


class RedisPublisherSensorProtocol(BaseSensorProtocol):
    """
    Publish sensor data into Redis
    """

    def __init__(self, redis_client):
        """
        redis_client:   An aioredis pool
        """
        self.redis = redis_client
        on_cleanup = [self.close_redis()]
        super().__init__(on_cleanup)

    async def close_redis(self):
        self.redis.close()
        await self.redis.wait_closed()

    def datagram_received(self, data, addr):
        now = datetime.now().strftime("%H:%M:%S,%f")
        self.redis.publish_json(
            settings.REDIS_SENSOR_CHANNEL,
            dict(data=data.decode("UTF-8"), addr=addr, date=now),
        )


class RESTSensorServerProtocol(BaseSensorProtocol):
    """
    POST sensor data to a REST API
    """

    endpoint = settings.API_URL

    async def datagram_received(self, data, addr):
        hardware_id, temperature, moisture = unpack("<20shh", data)
        data = {
            "hardware_id": hardware_id,
            "temperature": temperature,
            "moisture": moisture,
        }
        print(f"Received {data} from {addr} with hardware_id={hardware_id}")

        async with httpx.AsyncClient() as client:
            await client.post(self.endpoint, data, json=True)
