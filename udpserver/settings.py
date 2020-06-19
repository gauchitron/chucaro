import os

# UDP base settings
HOST = os.getenv("UDPSERVER_HOST", "127.0.0.1")
PORT = os.getenv("UDPSERVER_PORT", 5555)
UNPACK_DATA = False  # use `struct.unpack?`
PROTOCOL = os.getenv("UDPSERVER_PROTOCOL", "DummySensorProtocol")

# RESTApiSensorProtocol settings
API_URL = os.getenv("API_URL")

# RedisPublisherSensorProtocol settings
REDIS_URL = os.getenv("REDIS_URL", f"redis://localhost/1")
REDIS_SENSOR_CHANNEL = "sensors"  # Data will be pushed to this topic
