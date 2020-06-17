from udpserver import protocol, settings
import aioredis
import asyncio


async def get_redis_client():
    pool = await aioredis.create_redis_pool(settings.REDIS_URL)

    async def close_redis():
        pool.close()
        await pool.wait_closed()

    return pool, close_redis


async def get_protocol_instance(name=settings.PROTOCOL):
    """
    Protocol Factory. Returns a protocol instance.
    """
    protocol_class = getattr(protocol, name, None)
    if protocol_class is None:
        raise ValueError(f"Protocol {name} not found.")

    if protocol_class is protocol.RedisPublisherSensorProtocol:
        redis, close_redis = await get_redis_client()
        protocol_instance = protocol_class(redis_client=redis, on_cleanup=[close_redis])
        return protocol_instance

    return protocol_class()


async def get_sensors_datagram_endpoint(host, port):
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
    import pdb

    pdb.set_trace()
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
