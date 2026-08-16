"""Small drills for practical operations with Python's ``asyncio`` module."""

from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from typing import Any, TypeVar


T = TypeVar("T")
R = TypeVar("R")


async def concurrent_map(
    worker: Callable[[T], Awaitable[R]], items: Iterable[T]
) -> list[R]:
    """Run ``worker`` concurrently for every item and preserve input order.

    Practice creating all the awaitables and passing them to ``asyncio.gather``.
    An empty iterable should produce an empty list.
    """
    raise NotImplementedError


async def completion_order(
    worker: Callable[[T], Awaitable[R]], items: Iterable[T]
) -> list[R]:
    """Run all work concurrently and return results as operations finish.

    Practice creating tasks and consuming them with ``asyncio.as_completed``.
    The returned order may differ from the input order.
    """
    raise NotImplementedError


async def bounded_map(
    worker: Callable[[T], Awaitable[R]], items: Iterable[T], limit: int
) -> list[R]:
    """Map ``worker`` concurrently while allowing at most ``limit`` in flight.

    Use an ``asyncio.Semaphore`` and preserve input order. Raise ``ValueError``
    when ``limit`` is not positive.
    """
    raise NotImplementedError


async def with_timeout(
    awaitable: Awaitable[T], seconds: float, fallback: T
) -> T:
    """Await an operation, returning ``fallback`` if its deadline expires.

    Practice ``asyncio.wait_for`` so this remains compatible with Python 3.10.
    Do not swallow exceptions other than ``TimeoutError``.
    """
    raise NotImplementedError


async def cancel_and_wait(task: "asyncio.Task[Any]") -> None:
    """Cancel ``task`` and wait until its cancellation cleanup has completed.

    A cancelled task raises ``asyncio.CancelledError`` when awaited; consume that
    exception here. Calling this with an already-finished task should be safe.
    """
    raise NotImplementedError


async def queue_map(
    worker: Callable[[T], Awaitable[R]], items: Iterable[T], worker_count: int
) -> list[R]:
    """Process items using ``worker_count`` consumers and an ``asyncio.Queue``.

    Use ``put``, ``get``, ``task_done``, and ``join``. Shut down the consumers
    cleanly and preserve input order. Raise ``ValueError`` for fewer than one
    worker.
    """
    raise NotImplementedError


class AsyncRange:
    """An async iterator yielding ``start`` through ``stop - 1``.

    Implement ``__aiter__`` and ``__anext__``. Raise ``StopAsyncIteration`` at
    the end. An empty or reversed range yields nothing.
    """

    def __init__(self, start: int, stop: int) -> None:
        raise NotImplementedError

    def __aiter__(self) -> AsyncIterator[int]:
        raise NotImplementedError

    async def __anext__(self) -> int:
        raise NotImplementedError


async def run_blocking(function: Callable[..., R], *args: Any) -> R:
    """Run a blocking callable in a worker thread using ``asyncio.to_thread``."""
    raise NotImplementedError
