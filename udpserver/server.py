from udpserver import protocol, settings
import asyncio


async def get_protocol_instance(name: str = settings.PROTOCOL):
    """
    Protocol Factory. Returns a protocol instance.
    """

    protocol_class = getattr(protocol, name, None)
    if protocol_class is None:
        raise ValueError(f"Protocol {name} not found.")

    protocol_instance = None

    if protocol_class is protocol.RedisPublisherSensorProtocol:
        from udpserver.storage.redis import get_pool_of_connections

        protocol_instance = protocol_class(
            redis_client=get_pool_of_connections(settings.REDIS_URL)
        )

    if protocol_class is protocol.RESTApiSensorProtocol:
        protocol_instance = protocol_class(endpoint=settings.API_URL)

    if protocol_class is protocol.InfluxDBSensorProtocol:
        import influxdb_client

        protocol_instance = protocol_class(endpoint=settings.API_URL)

    return protocol_instance or protocol_class()


async def get_sensors_datagram_endpoint(host: str, port: int):
    """
    A coroutine which creates a datagram endpoint using the BolsonServerProtocol.

    This method will try to establish the endpoint in the background.
    When successful, the coroutine returns a (transport, protocol) pair.
    """
    loop = asyncio.get_event_loop()
    protocol_instance = await get_protocol_instance()

    return await loop.create_datagram_endpoint(
        lambda: protocol_instance, local_addr=(host, port)
    )


async def exec_transport_protocol_cleanup(transport):
    """
    Execute a list of awaitables, if defined, in `transport._protocol.on_cleanup`.
    """
    return await asyncio.gather(*transport._protocol.on_cleanup)


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
    loop.run_until_complete(exec_transport_protocol_cleanup(transport))
    transport.close()
    loop.close()


if __name__ == "__main__":
    main()
