import asyncio
from udpserver import settings
from udpserver.protocol import BolsonServerProtocol


async def get_bolson_datagram_endpoint(host, port):
    """A coroutine which creates a datagram endpoint using the BolsonServerProtocol.

    This method will try to establish the endpoint in the background.
    When successful, the coroutine returns a (transport, protocol) pair.
    """
    loop = asyncio.get_event_loop()
    return await loop.create_datagram_endpoint(
        lambda: BolsonServerProtocol(), local_addr=(host, port)
    )


def main():
    loop = asyncio.get_event_loop()
    bolson_proto_coro = get_bolson_datagram_endpoint(settings.HOST, settings.PORT)
    transport, _ = loop.run_until_complete(bolson_proto_coro)
    print(f"Bolson UDP server is running on {settings.HOST}:{settings.PORT}.")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("\nShutting down server...")
    transport.close()
    loop.close()


if __name__ == "__main__":
    main()
