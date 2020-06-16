import asyncio
from udpserver import settings
from udpserver import protocol


def get_protocol_class():
    """
    Returns a protocol class.
    """
    protocol_class = getattr(protocol, settings.PROTOCOL, None)
    if protocol_class is None:
        raise ValueError(
            f"Defined protocol in settings {settings.PROTOCOL} was not found."
        )

    return protocol_class


async def get_sensors_datagram_endpoint(host, port):
    """
    A coroutine which creates a datagram endpoint using the BolsonServerProtocol.

    This method will try to establish the endpoint in the background.
    When successful, the coroutine returns a (transport, protocol) pair.
    """
    loop = asyncio.get_event_loop()
    return await loop.create_datagram_endpoint(
        lambda: get_protocol_class(), local_addr=(host, port)
    )


def main():
    loop = asyncio.get_event_loop()
    sensors_proto_coro = get_sensors_datagram_endpoint(settings.HOST, settings.PORT)
    transport, _ = loop.run_until_complete(sensors_proto_coro)
    print(f"Sensors UDP server is running on {settings.HOST}:{settings.PORT}.")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("\nShutting down server...")
    transport.close()
    loop.close()


if __name__ == "__main__":
    main()
