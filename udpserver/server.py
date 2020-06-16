from udpserver import protocol, settings
import asyncio


def get_protocol_instance():
    """
    Returns a protocol instance.
    """
    protocol_class = getattr(protocol, settings.PROTOCOL, None)
    if protocol_class is None:
        raise ValueError(
            f"Defined protocol in settings {settings.PROTOCOL} was not found."
        )

    return protocol_class()


async def get_sensors_datagram_endpoint(host, port):
    """
    A coroutine which creates a datagram endpoint using the BolsonServerProtocol.

    This method will try to establish the endpoint in the background.
    When successful, the coroutine returns a (transport, protocol) pair.
    """
    loop = asyncio.get_event_loop()
    return await loop.create_datagram_endpoint(
        lambda: get_protocol_instance(), local_addr=(host, port)
    )


async def protocol_shutdown(protocol):
    return await protocol.clean_up()


def main():
    loop = asyncio.get_event_loop()
    sensors_proto_coro = get_sensors_datagram_endpoint(settings.HOST, settings.PORT)
    transport, _ = loop.run_until_complete(sensors_proto_coro)
    print(f"Sensors UDP server is running on {settings.HOST}:{settings.PORT}.")
    print(f"Protocol was set to: {transport._protocol.__class__.__name__}")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("\nShutting down server...")
    loop.run_until_complete(protocol_shutdown(transport._protocol))
    transport.close()
    loop.close()


if __name__ == "__main__":
    main()
