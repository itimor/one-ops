import asyncio
import time


async def say_after(what):
    print(what)


async def main():
    task1 = asyncio.create_task(say_after('hello'))

    task2 = asyncio.create_task(say_after('world'))

    await task1
    await task2


start = time.time()
asyncio.run(main())
end = time.time()
print(end - start)
