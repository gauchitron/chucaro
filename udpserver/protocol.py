import requests
from struct import unpack
import pickle

import settings

class BolsonServerProtocol:
    """
    Bolson Protocol.
    """

    status_ok = b"0"
    status_error = b"1"

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
        self.transport.sendto(self.status_ok, addr)
        requests.post(settings.API_URL, data, json=True)

    def connection_lost(self, exc):
        if exc is None:
            print("Connection closed or aborted by me.")
