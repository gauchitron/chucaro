"""This is a UDP client to test the UDP Server."""

import sys
import asyncio
from struct import pack
from udpserver import settings


class BolsonClientProtocol:
    status_ok = b"0"
    status_error = b"1"

    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Send:", self.message)
        self.transport.sendto(self.message)

    def datagram_received(self, data, addr):
        if data == self.status_ok:
            print(f"All is good, received status code: {data.decode()}")
        else:
            print(f"Server is fucked up, received: {data.decode()}")
        self.transport.close()

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    hardware_id, temperature, humidity = str(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    message = pack('<20shh', bytes(hardware_id.encode("ascii")), temperature, humidity)

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: BolsonClientProtocol(message, on_con_lost),
        remote_addr=(settings.HOST, settings.PORT),
    )

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())
