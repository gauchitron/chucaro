from struct import unpack
from datetime import datetime
from udpserver import settings


class BaseSensorProtocol:
    """
    Base class for sensor protocols.
    """

    def __init__(self, on_cleanup=None):
        """
        on_cleanup:     A list of `coroutines` to be excecuted on transport close.
        """
        self.on_cleanup = on_cleanup or []

    def handle_sensor_data(self, data, addr):
        """
        Do whatever you want with sensor data.
        """
        raise NotImplementedError

    def parse_data(self, data):
        if settings.UNPACK_DATA:
            data = unpack("<20shh", data)
        return data

    def datagram_received(self, data, addr):
        data = self.parse_data(data)
        self.handle_sensor_data(data, addr)

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

    def handle_sensor_data(self, data, addr):
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
        on_cleanup = [self.close_redis()]  # A list of coroutines
        super().__init__(on_cleanup)

    async def close_redis(self):
        self.redis.close()
        await self.redis.wait_closed()

    def handle_sensor_data(self, data, addr):
        now = datetime.now().strftime("%H:%M:%S,%f")
        self.redis.publish_json(
            settings.REDIS_SENSOR_CHANNEL,
            dict(data=data.decode("UTF-8"), addr=addr, date=now),
        )


class RESTApiSensorProtocol(BaseSensorProtocol):
    """
    POST sensor data to a REST API
    """

    def __init__(self, endpoint):
        """
        endpoint:   API endpoint to POST data.
        """
        self.endpoint = endpoint
        super().__init__()

    async def handle_sensor_data(self, data, addr):
        import httpx

        async with httpx.AsyncClient() as client:
            await client.post(self.endpoint, data, json=True)


class InfluxDBSensorProtocol(BaseSensorProtocol):
    """
    Write data to InfluxDB 2.0
    """

    def __init__(self, influxdb_client):
        self.influxdb = influxdb_client
        super().__init__()

    def handle_sensor_data(self, data, addr):
        self.influxdb.write(bucket="test", record=data)
