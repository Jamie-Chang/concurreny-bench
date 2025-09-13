import asyncio
from contextlib import contextmanager
from typing import Iterator
import random
import tracemalloc
from itertools import islice
import time


@contextmanager
def timer(message: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        print(message, time.perf_counter() - start, "s")



def urls() -> Iterator[str]:
    while True:
        yield "https://example.com"


async def process_url(url: str) -> None:
    await asyncio.sleep(random.uniform(0.1, 0.2))


async def main() -> None:
    tracemalloc.start()
    with timer("Semaphore with callback"):
        semaphore = asyncio.Semaphore(500)
        async with asyncio.TaskGroup() as tg:
            for url in islice(urls(), 100_000):
                await semaphore.acquire()
                tg.create_task(process_url(url)).add_done_callback(
                    lambda _: semaphore.release()
                )

    _, peak_memory = tracemalloc.get_traced_memory()
    print(f"Peak memory usage: {peak_memory:_} bytes")
    tracemalloc.stop()


if __name__ == "__main__":
    asyncio.run(main())
