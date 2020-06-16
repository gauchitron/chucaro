from struct import unpack
from udpserver import settings


class DummySensorProtocol:
    """
    Dummy Sensor Protocol

    It'll only print received data.
    """
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"From {addr}\nReceived {data}")

    def connection_lost(self, exc):
        if exc is None:
            print("Connection closed or aborted by me.")


class RedisPublisherSensorProtocol:
    """
    Publish sensor data into Redis
    """

class RESTSensorServerProtocol:
    """
    POST sensor data to a REST API
    """

    endpoint = settings.API_URL

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        hardware_id, temperature, moisture = unpack('<20shh', data)
        data = {
            "hardware_id": hardware_id,
            "temperature": temperature,
            "moisture": moisture
        }
        print(f"Received {data} from {addr} with hardware_id={hardware_id}")

        import requests
        requests.post(self.endpoint, data, json=True)

    def connection_lost(self, exc):
        if exc is None:
            print("Connection closed or aborted by me.")