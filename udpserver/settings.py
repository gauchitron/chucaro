import os

# UDP base settings
HOST = os.getenv("UDPSERVER_HOST", "127.0.0.1")
PORT = os.getenv("UDPSERVER_PORT", 5555)
UNPACK_DATA = os.getenv("UDPSERVER_UNPACK_DATA", False)  # use `struct.unpack?`
PROTOCOL = os.getenv("UDPSERVER_PROTOCOL", "DummySensorProtocol")

# RESTApiSensorProtocol settings
API_URL = os.getenv("API_URL")

# RedisPublisherSensorProtocol settings
REDIS_URL = os.getenv("PROTOCOL_REDIS_PUBLISHER_URL", f"redis://localhost/1")
REDIS_SENSOR_CHANNEL = os.getenv("PROTOCOL_REDIS_PUBLISHER_CHANNEL_NAME", "gauchitron-dev")
