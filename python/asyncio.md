# Asyncio

One of the like, three different libraries to write concurrent code with python

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

If you have a function which has not been marked as `async`, you can use `asyncio.to_thread()`
to delegate it to a separate thread. But because of the GIL this can only be used to make IO-bound
functions non-blocking.

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

Tasks can be used to concurrently schedule multiple coroutines. When your task is wrapped by `asyncio.create_task()`
the coroutine will be automatically scheduled to run soon.

```python
import asyncio


async def nested():
    return 42


async def main():
    task = asyncio.create_task(nested())
    await task


asyncio.run(main())
```

Running tasks can be canceled easily with `task.cancel()`, after which an `asyncio.CancelledError` will be raised (you can even `uncancel()` them too).
Tasks can be shielded from cancellation via `asyncio.shield()` if needed.

## Asyncio: Timeouts

Timeouts for tasks can be set with `asyncio.timeout()`. If a timeout is exceeded, the task will be cancelled and the
resulting `asyncio.CancelledError` will be converted into an `asyncio.TimeoutError`. After a timeout has been created
`Timeout.reschedule()` can be used to change it.

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

`timeout_at()` accepts absolute time when the task should stop.
`wait_for()` lets you create a task and set the timeout inline.

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

`asyncio.current_task()`
`asyncio.all_tasks()`
`asyncio.iscoroutine()`

## Further reading

* [asyncio docs](https://docs.python.org/3/library/asyncio.html)
