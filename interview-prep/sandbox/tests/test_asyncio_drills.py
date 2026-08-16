import asyncio
import threading

import pytest

from asyncio_drills import (
    AsyncRange,
    bounded_map,
    cancel_and_wait,
    completion_order,
    concurrent_map,
    queue_map,
    run_blocking,
    with_timeout,
)


def test_concurrent_map_preserves_input_order() -> None:
    async def scenario() -> None:
        release = asyncio.Event()
        started = 0

        async def worker(value: int) -> int:
            nonlocal started
            started += 1
            await release.wait()
            return value * 10

        task = asyncio.create_task(concurrent_map(worker, [3, 1, 2]))
        while started < 3:
            await asyncio.sleep(0)
        release.set()
        assert await task == [30, 10, 20]
        assert await concurrent_map(worker, []) == []

    asyncio.run(scenario())


def test_completion_order_returns_results_as_tasks_finish() -> None:
    async def scenario() -> None:
        gates = {value: asyncio.Event() for value in [1, 2, 3]}
        started = 0

        async def worker(value: int) -> int:
            nonlocal started
            started += 1
            await gates[value].wait()
            return value

        task = asyncio.create_task(completion_order(worker, [1, 2, 3]))
        while started < 3:
            await asyncio.sleep(0)
        for value in [3, 1, 2]:
            gates[value].set()
            await asyncio.sleep(0)
        assert await task == [3, 1, 2]

    asyncio.run(scenario())


def test_bounded_map_enforces_limit_and_preserves_order() -> None:
    async def scenario() -> None:
        running = 0
        peak = 0

        async def worker(value: int) -> int:
            nonlocal running, peak
            running += 1
            peak = max(peak, running)
            await asyncio.sleep(0)
            running -= 1
            return value * 2

        assert await bounded_map(worker, range(8), 3) == [
            0,
            2,
            4,
            6,
            8,
            10,
            12,
            14,
        ]
        assert peak == 3

        with pytest.raises(ValueError):
            await bounded_map(worker, [1], 0)

    asyncio.run(scenario())


def test_with_timeout_returns_result_or_fallback() -> None:
    async def scenario() -> None:
        async def immediate() -> str:
            return "finished"

        async def never() -> str:
            await asyncio.Event().wait()
            return "unreachable"

        assert await with_timeout(immediate(), 1, "fallback") == "finished"
        assert await with_timeout(never(), 0.01, "fallback") == "fallback"

    asyncio.run(scenario())


def test_with_timeout_does_not_hide_other_errors() -> None:
    async def scenario() -> None:
        async def broken() -> str:
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            await with_timeout(broken(), 1, "fallback")

    asyncio.run(scenario())


def test_cancel_and_wait_allows_cleanup_to_finish() -> None:
    async def scenario() -> None:
        started = asyncio.Event()
        cleaned_up = asyncio.Event()

        async def long_running() -> None:
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                cleaned_up.set()

        task = asyncio.create_task(long_running())
        await started.wait()
        await cancel_and_wait(task)
        assert task.cancelled()
        assert cleaned_up.is_set()

        finished = asyncio.create_task(asyncio.sleep(0))
        await finished
        await cancel_and_wait(finished)

    asyncio.run(scenario())


def test_queue_map_uses_workers_and_preserves_order() -> None:
    async def scenario() -> None:
        running = 0
        peak = 0

        async def worker(value: int) -> int:
            nonlocal running, peak
            running += 1
            peak = max(peak, running)
            await asyncio.sleep(0)
            running -= 1
            return value * value

        assert await queue_map(worker, [4, 1, 3, 2], 2) == [16, 1, 9, 4]
        assert peak == 2
        assert await queue_map(worker, [], 2) == []

        with pytest.raises(ValueError):
            await queue_map(worker, [1], 0)

    asyncio.run(scenario())


def test_async_range() -> None:
    async def collect(start: int, stop: int) -> list[int]:
        return [value async for value in AsyncRange(start, stop)]

    assert asyncio.run(collect(2, 5)) == [2, 3, 4]
    assert asyncio.run(collect(3, 3)) == []
    assert asyncio.run(collect(5, 3)) == []


def test_run_blocking_uses_another_thread() -> None:
    caller_thread = threading.get_ident()

    def blocking_add(left: int, right: int) -> tuple[int, int]:
        return left + right, threading.get_ident()

    result, worker_thread = asyncio.run(run_blocking(blocking_add, 2, 5))
    assert result == 7
    assert worker_thread != caller_thread
