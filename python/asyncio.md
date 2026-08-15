---
tags:
  - asyncio
  - programming-language
  - python
---
# Asyncio
One of the like, three different libraries to write concurrent code with python
## TL;DR
**Run and Spawn**
```python
import asyncio

async def work(n: int) -> int:
	await asyncio.sleep(0.01)
	return n * 2
	

async def main() -> None:
	r = await work(1)                           # sequential
	rs = await asyncio.gather(work(1), work(2)) # concurrent, ordered
	t = asyncio.create_task(work(3))            # start now, await later
	other_stuff()
	r3 await t
	
	
if __name__ == "__main__":
	asyncio.run(main())                         # entry point, once
```

**TaskGroup**
```python
async def main() -> None:
	async with asyncio.TaskGroup() as tg:
		t1 = tg.create_task(work(1))
		t2 = tg.create_task(work(2))
	print(t1.result(), t2.result()) # both done here; result is an int
```

**Bounded Concurrency**
```python
from collections.abc import Iterable, Sequence

async def fetch_all(urls: Sequence[str], limit: int = 10) -> list[str]:
	sem = asyncio.Semaphore(limit)
	
	async def one(url: str) -> str:
		async with sem:
			return await fetch(url)
			
	return await asyncio.gather(*(one(u) for u in urls))
```

**Producer / Consumer**
```python
async def producer(q: asyncio.Queue[int], items: Iterable[int]) -> None:
	for it in items:
		await q.put(it)


async def consumer(q: asyncio.Queue[int], out: list[int]) -> None:
	while True:
		item = await q.get()
		try:
			out.append(await work(item))
		finally:
			q.task_done()
			

async def main(items: Sequence[int], n_workers: int = 3) -> list[int]:
	q = asyncio.Queue(maxsize=100)
	out = []
	workers = [
		asyncio.create_task(consumer(q, out)) for _ in range(n_workers)
	]
	await producer(q, items)
	await q.join()  # all task_done() called
	for w in workers:
		w.cancel()
	return out
```

**Timeouts & Cancellation**
```python
async with asyncio.timeout(5):  # 3.11+
	await slow()
	
r = await asyncio.wait_for(slow(), timeout=5)  # older; raises TimeoutError
	
t = asyncio.create_task(slow())
t.cancel()
try:
	await t
except asyncio.CancelledError:
	pass
```

**Results as they finish**
```python
from colelctions.abc import Coroutine

tasks = [asyncio.create_task(work(i)) for i in range(5)]

for coro in asyncio.as_completed(tasks):
	print(await coro)
	
done: set[asyncio.Task[int]]
pending: set[asyncio.Task[int]]
done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
```

**Blocking code**
```python
def blocking_fn(arg: str) -> bytes: ...

result = asyncio.to_thread(blocking_fn, "x")
```

**Sync Primitives**
```python
lock: asyncio.Lock = asyncio.Lock()            # async with lock:
sem: asyncio.Semaphore = asyncio.Semaphore(10) # async with sem:
ev: asyncio.Event = asyncio.Event().           # await ev.wait(); ev.set()
```

**Async Iterator Protocol**
```python
from typing import Self

class Counter:
	def __init__(self, limit: int) -> None:
		self._limit = limit
		self._i = 0
		
	def __aiter__(self) -> Self:     # NOT async
		return self
		
	async def __anext__(self) -> int:
		if self._i >= self._limit:
			raise StopAsyncIteration # NOT StopIteration
			
		await asyncio.sleep(0.01)
		self._i += 1
		return self._i
```
...for return types use `AsyncIterator` from `collections`...
```python
from collections.abc import AsyncIterator

async def acounter(limit: int) -> AsyncIterator[int]:
	for i in range(limit):
		await asyncio.sleep(0.01)
		yield i
```
## Asyncio: Basic usage
Asyncio let's you stick the `async` keyword in from of any function and then call it
using `asyncio.run()`. This runs your function in a [Coroutine](https://peps.python.org/pep-0492/).
From there, you can `await` the result as you'd expect.

```python
import asyncio


async def main():
    print("Hello ...")
    await asyncio.sleep(1)
    print("... World!")


asyncio.run(main())
```
## Asyncio: `to_thread()`
If you have a function which has not been marked as `async`, you can use `asyncio.to_thread()` to delegate it to a separate thread. But because of the GIL this can only be used to make IO-bound functions non-blocking.

```python
import asyncio
import time


def some_blocking_io():
    time.sleep(1)


asyncio.to_thread(some_func)
```
## Asyncio: Sleeping
Within a coroutine, you can't use `time.sleep()` since it's blocking. But you can instead use `asyncio.sleep()`.
## Asyncio: Futures
Much like other languages, async results are represented by a [Future](https://docs.python.org/3/library/asyncio-future.html#asyncio.Future) object to represent the eventual result.

When a Future object is awaited, the coroutine will pause and wait until the Future is resolved.

If you have multiple futures that you need to wait for, you can use `asyncio.gather()`

```python
async def main():
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_other_python_coroutine(),
    )
```

Or, you can use a TaskGroup...
```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(some_coroutine())
        task2 = tg.create_task(another_coroutine())

    print("Both tasks are done!")
```
## Asyncio: Tasks
Tasks can be used to concurrently schedule multiple coroutines. When your task is wrapped by `asyncio.create_task()` the coroutine will be automatically scheduled to run soon.

```python
import asyncio


async def nested():
    return 42


async def main():
    task = asyncio.create_task(nested())
    await task


asyncio.run(main())
```

Running tasks can be canceled easily with `task.cancel()`, after which an `asyncio.CancelledError` will be raised (you can even `uncancel()` them too). Tasks can be shielded from cancellation via `asyncio.shield()` if needed.
## Asyncio: Timeouts
Timeouts for tasks can be set with `asyncio.timeout()`. If a timeout is exceeded, the task will be cancelled and the resulting `asyncio.CancelledError` will be converted into an `asyncio.TimeoutError`. After a timeout has been created `Timeout.reschedule()` can be used to change it.

```python
async def main():
    try:
        async with asyncio.timeout(10):
            await long_running_task()
    except TimeoutError:
        print("The long operation timed out, but we've handled it")
```

The ContextManager resulting from this sort of pattern can be inspected to see if the tasks finished on time.

```python
async def main():
    try:
        async with asyncio.timeout(None) as cm:
            new_deadline = get_running_loop().time() + 10
            cm.reschedule(new_deadline)

            await long_tunning_task()
    except TimeoutError:
        pass

    if cm.expired():
        print("Looks like we haven't finished on time :(")
```

Just like `asyncio.timeout()`, you can use `asyncio.timeout_at()`, or `asyncio.wait_for()` instead.
- `timeout_at()` accepts absolute time when the task should stop.
- `wait_for()` lets you create a task and set the timeout inline.

```python
async def eternity():
    await asyncio.sleep(3600)
    print("yay!")

async def main():
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except TimeoutError:
        print("timeout!")

asyncio.run(main())
```
## Asyncio: Introspection
Asyncio provides a few functions to help you get an idea of what tasks are in flight (and if you're running inside one).
- `asyncio.current_task()`
- `asyncio.all_tasks()`
- `asyncio.iscoroutine()`
## Further reading
* [asyncio docs](https://docs.python.org/3/library/asyncio.html)
