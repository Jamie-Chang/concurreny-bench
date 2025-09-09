import asyncio
from typing import Iterator
import random
import tracemalloc
from itertools import batched, islice


def urls() -> Iterator[str]:
    while True:
        yield "https://example.com"


async def process_url(url: str) -> None:
    await asyncio.sleep(random.uniform(0.1, 0.2))


async def main() -> None:
    tracemalloc.start()
    for batch in batched(islice(urls(), 100_000), 500):
        async with asyncio.TaskGroup() as tg:
            for url in batch:
                tg.create_task(process_url(url))

    _, peak_memory = tracemalloc.get_traced_memory()
    print(f"Peak memory usage: {peak_memory:_} bytes")
    tracemalloc.stop()


if __name__ == "__main__":
    asyncio.run(main())
