import os

HOST = os.getenv("LANZA_HOST", "127.0.0.1")
PORT = os.getenv("LANZA_PORT", 5555)
API_URL = os.getenv("API_URL")
PROTOCOL = os.getenv("LANZA_PROTOCOL", "DummySensorProtocol")
REDIS_URL = os.getenv("REDIS_URL", f"redis://localhost/1")
REDIS_SENSOR_CHANNEL = "sensors"