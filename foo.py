import asyncio
import aioredis


async def reader(ch):
    while (await ch.wait_message()):
        msg = await ch.get_json()
        print("Got Message:", msg)


async def main():
    sub = await aioredis.create_redis(
        'redis://localhost/1')
    res = await sub.subscribe('sensors')
    ch1 = res[0]

    tsk = await reader(ch1)


    await sub.unsubscribe('sensors')
    await tsk
    sub.close()


if __name__ == '__main__':
    asyncio.run(main())
